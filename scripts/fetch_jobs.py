#!/usr/bin/env python3
"""
fetch_jobs.py — flexible, keyless-first job sourcing for Stage 5.

Keyless public ATS providers: greenhouse, lever, ashby, smartrecruiters.
Keyed: usajobs (free key + email; US federal).
LinkedIn is NOT here — it's the DEFAULT source but done via "claude-fetch" (Claude WebFetches the
guest endpoints), which is more robust than scripting. See references/05-coaching.md.

Structure (registry + normalize + SimHash dedup + liveness + scan-history ledger + portals config)
is a Python port of ideas from santifer/career-ops (MIT) — see ATTRIBUTIONS.md. Stdlib only.

List roles at a company:
    python fetch_jobs.py greenhouse gitlab --list [--match "data scientist"]
Save one posting (fetches full body; logs to scan-history; warns on dup/expired):
    python fetch_jobs.py smartrecruiters Visa --id 744000133907678 --out data/<user>/targets/<slug>/posting.md
Scan many tracked companies from a portals config (deduped):
    python fetch_jobs.py scan --portals data/<user>/portals.json [--match "director"]
USAJobs (keyed):
    python fetch_jobs.py usajobs "data scientist" --list --key $USAJOBS_KEY --email you@example.com

ToS/storage: public ATS boards are keyless embeds — fetch per company, cache lightly, attribute the
employer, don't bulk-harvest. USAJobs is public-domain/storable. Keep it small-batch and personal.
"""
import argparse, datetime, hashlib, html, json, os, re, sys, urllib.request, urllib.parse

UA = "corpus-vitae/1.0 (personal job search; +https://github.com/corpus-vitae)"


def _get(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _get_json(url, headers=None):
    return json.loads(_get(url, headers))


def _label(x):
    return (x.get("label") or x.get("name") or "") if isinstance(x, dict) else (x or "")


def _strip_html(s):
    if not s:
        return ""
    s = html.unescape(s)
    s = re.sub(r"(?i)<\s*br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</\s*(p|div|li|h[1-6])\s*>", "\n", s)
    s = re.sub(r"(?i)<\s*li[^>]*>", "• ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# ---------- providers: list(company) -> [normalized dict]; optional detail(company,id)->{body,url} ----------
def greenhouse(company, **kw):
    data = _get_json(f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true")
    return [{"id": str(j.get("id", "")), "title": j.get("title", ""), "company": company,
             "location": (j.get("location") or {}).get("name", ""), "url": j.get("absolute_url", ""),
             "employment_type": "", "department": ", ".join(d.get("name", "") for d in j.get("departments", []) or []),
             "comp": "", "body": _strip_html(j.get("content", ""))} for j in data.get("jobs", [])]


def lever(company, **kw):
    data = _get_json(f"https://api.lever.co/v0/postings/{company}?mode=json")
    if isinstance(data, dict) and data.get("ok") is False:
        return []
    out = []
    for j in data:
        cat = j.get("categories", {}) or {}
        body = j.get("descriptionPlain", "") or _strip_html(j.get("description", ""))
        for lst in j.get("lists", []) or []:
            body += f"\n\n{lst.get('text','')}\n" + _strip_html(lst.get("content", ""))
        out.append({"id": j.get("id", ""), "title": j.get("text", ""), "company": company,
                    "location": cat.get("location", ""), "url": j.get("hostedUrl", ""),
                    "employment_type": cat.get("commitment", ""), "department": cat.get("team", ""),
                    "comp": "", "body": body.strip()})
    return out


def ashby(board, **kw):
    data = _get_json(f"https://api.ashbyhq.com/posting-api/job-board/{board}?includeCompensation=true")
    out = []
    for j in data.get("jobs", []):
        cc = j.get("compensation") or {}
        out.append({"id": j.get("id", ""), "title": j.get("title", ""), "company": board,
                    "location": j.get("location", ""), "url": j.get("jobUrl", ""),
                    "employment_type": j.get("employmentType", ""), "department": j.get("departmentName", ""),
                    "comp": cc.get("compensationTierSummary", "") if isinstance(cc, dict) else "",
                    "body": j.get("descriptionPlain", "") or _strip_html(j.get("descriptionHtml", ""))})
    return out


def smartrecruiters(company, **kw):
    data = _get_json(f"https://api.smartrecruiters.com/v1/companies/{company}/postings?limit=100")
    out = []
    for j in data.get("content", []):
        loc = j.get("location", {}) or {}
        out.append({"id": str(j.get("id", "")), "title": j.get("name", ""), "company": company,
                    "location": loc.get("fullLocation") or ", ".join(x for x in (loc.get("city"), loc.get("country")) if x),
                    "url": f"https://jobs.smartrecruiters.com/{company}/{j.get('id','')}",
                    "employment_type": _label(j.get("typeOfEmployment")), "department": _label(j.get("department")),
                    "comp": "", "body": ""})  # body via detail
    return out


def smartrecruiters_detail(company, jid):
    d = _get_json(f"https://api.smartrecruiters.com/v1/companies/{company}/postings/{jid}")
    secs = (d.get("jobAd", {}) or {}).get("sections", {}) or {}
    order = ["jobDescription", "qualifications", "additionalInformation", "companyDescription"]
    body = "\n\n".join(_strip_html((secs.get(k, {}) or {}).get("text", "")) for k in order if secs.get(k))
    return {"body": body.strip(), "url": d.get("postingUrl") or d.get("applyUrl", "")}


def usajobs(keyword, key=None, email=None, **kw):
    if not key or not email:
        sys.exit("usajobs needs --key <API key> and --email <registered email>. "
                 "Free key: https://developer.usajobs.gov/apirequest/")
    url = "https://data.usajobs.gov/api/search?" + urllib.parse.urlencode({"Keyword": keyword, "ResultsPerPage": 25})
    data = _get_json(url, headers={"Host": "data.usajobs.gov", "User-Agent": email, "Authorization-Key": key})
    out = []
    for item in data.get("SearchResult", {}).get("SearchResultItems", []):
        d = item.get("MatchedObjectDescriptor", {})
        pay = (d.get("PositionRemuneration") or [{}])[0]
        out.append({"id": d.get("PositionID", ""), "title": d.get("PositionTitle", ""),
                    "company": d.get("OrganizationName", ""),
                    "location": ", ".join(l.get("LocationName", "") for l in d.get("PositionLocation", []) or []),
                    "url": d.get("PositionURI", ""), "employment_type": "",
                    "department": d.get("DepartmentName", ""),
                    "comp": f"{pay.get('MinimumRange','')}-{pay.get('MaximumRange','')} {pay.get('RateIntervalCode','')}".strip(),
                    "body": _strip_html((d.get("UserArea", {}).get("Details", {}) or {}).get("JobSummary", ""))})
    return out


PROVIDERS = {"greenhouse": greenhouse, "lever": lever, "ashby": ashby,
             "smartrecruiters": smartrecruiters, "usajobs": usajobs}
DETAIL = {"smartrecruiters": smartrecruiters_detail}
# To add a provider: write list(company)->[dict] (+ optional detail), register above. Endpoint
# patterns for more keyless ATS (Workable/Recruitee/etc.) are known — add once verified per slug.


# ---------------- SimHash cross-listing dedup (ported idea: career-ops) ----------------
def simhash(text, bits=64):
    toks = re.findall(r"[a-z0-9]{3,}", (text or "").lower())
    if not toks:
        return 0
    v = [0] * bits
    for t in set(toks):  # set → shingle-ish; weight by presence
        h = int.from_bytes(hashlib.blake2b(t.encode(), digest_size=8).digest(), "big")
        for i in range(bits):
            v[i] += 1 if (h >> i) & 1 else -1
    return sum(1 << i for i in range(bits) if v[i] > 0)


def hamming(a, b):
    return bin(a ^ b).count("1")


def _alive(url):
    if not url:
        return None
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=12) as r:
                return r.status < 400
        except Exception:
            continue
    return False


def _ledger(out_path, ledger_override):
    if ledger_override:
        return ledger_override
    d = os.path.dirname(os.path.abspath(out_path))          # .../targets/<slug>
    return os.path.normpath(os.path.join(d, os.pardir, "scan-history.tsv"))  # .../targets/scan-history.tsv


def _ledger_check_append(ledger, provider, job, sh):
    dup = None
    if os.path.exists(ledger):
        for line in open(ledger):
            p = line.rstrip("\n").split("\t")
            if len(p) >= 6 and p[5].isdigit() and hamming(sh, int(p[5])) <= 3:
                dup = p[4]; break
    new = not os.path.exists(ledger)
    with open(ledger, "a") as f:
        if new:
            f.write("date\tprovider\tcompany\tid\ttitle\tsimhash\turl\n")
        f.write(f"{datetime.date.today().isoformat()}\t{provider}\t{job['company']}\t{job['id']}\t"
                f"{job['title']}\t{sh}\t{job.get('url','')}\n")
    return dup


DEFAULT_STORE = "data/_shared/jobs.jsonl"


def append_store(store, provider, jobs):
    """Append fetched jobs to the shared append-only ingestion log (data/_shared/jobs.jsonl)."""
    if not store or not jobs:
        return 0
    os.makedirs(os.path.dirname(store) or ".", exist_ok=True)
    today = datetime.date.today().isoformat()
    with open(store, "a") as f:
        for j in jobs:
            rec = {"job_key": f"{provider}:{j.get('id','')}", "source": provider,
                   "source_id": str(j.get("id", "")), "company": j.get("company", ""),
                   "title": j.get("title", ""), "location": j.get("location", ""),
                   "url": j.get("url", ""), "apply_url": j.get("url", ""), "salary_raw": j.get("comp", ""),
                   "employment_type": j.get("employment_type", ""), "department": j.get("department", ""),
                   "posted_date": j.get("posted_date", ""), "ingested_at": today,
                   "simhash": simhash(j.get("title", "") + " " + j.get("body", "")[:2000]),
                   "body": j.get("body", "")}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return len(jobs)


def to_posting_md(job, provider):
    return (f"# {job['title']} — {job['company']}\n\n"
            f"- source_url: {job.get('url','')}\n"
            f"- apply_url: {job.get('url','')}\n"
            f"- employer: {job['company']}\n"
            f"- location: {job.get('location','')}\n"
            f"- date_seen: {datetime.date.today().isoformat()}\n"
            f"- salary: {job.get('comp','') or 'not listed'}\n"
            f"- employment_type: {job.get('employment_type','')}\n"
            f"- department: {job.get('department','')}\n"
            f"- provider: {provider}\n\n"
            f"## Full text\n{job.get('body','')}\n")


def run_scan(portals_path, match, store=None):
    cfg = json.load(open(portals_path))
    seen, rows, ingested = [], [], 0
    for co in cfg.get("tracked_companies", []):
        prov, slug = co.get("provider"), co.get("slug")
        if prov not in PROVIDERS:
            print(f"  ! skip {prov}:{slug} (unknown provider)"); continue
        try:
            jobs = PROVIDERS[prov](slug)
        except Exception as e:
            print(f"  ! {prov}:{slug} failed: {e}"); continue
        m = (co.get("match") or match or "").lower()
        matched = [j for j in jobs if not m or m in j["title"].lower()]
        ingested += append_store(store, prov, matched)  # ingest into the shared log
        for j in matched:
            sh = simhash(j["title"] + " " + j.get("body", "")[:2000])
            dup = any(hamming(sh, s) <= 3 for s in seen)
            seen.append(sh)
            rows.append((dup, prov, slug, j))
    uniq = sum(1 for r in rows if not r[0])
    print(f"{uniq} unique / {len(rows)} total posting(s)" + (f"; ingested {ingested} to {store}" if store else "") + ":")
    for dup, prov, slug, j in rows:
        print(f"  {'DUP ' if dup else '    '}[{prov}:{slug}] {j['title']}  |  {j.get('location','')}  |  id={j['id']}")


def main():
    ap = argparse.ArgumentParser(description="Flexible keyless-first job sourcing (Stage 5).")
    ap.add_argument("provider", choices=list(PROVIDERS) + ["scan"])
    ap.add_argument("target", nargs="?", help="company/board slug (or keyword for usajobs)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--match", default="")
    ap.add_argument("--id", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--ledger", default=None, help="scan-history.tsv path (default: targets/scan-history.tsv)")
    ap.add_argument("--portals", default=None, help="scan mode: JSON config with tracked_companies")
    ap.add_argument("--store", default=DEFAULT_STORE, help=f"shared jobs log (default {DEFAULT_STORE})")
    ap.add_argument("--no-store", action="store_true", help="don't append to the shared jobs log")
    ap.add_argument("--key", default=None); ap.add_argument("--email", default=None)
    args = ap.parse_args()
    store = None if args.no_store else args.store

    if args.provider == "scan":
        if not args.portals:
            sys.exit("scan needs --portals <config.json> (see templates/portals.example.json)")
        return run_scan(args.portals, args.match, store)

    if not args.target:
        sys.exit(f"{args.provider} needs a company/board slug (or keyword for usajobs).")

    jobs = PROVIDERS[args.provider](args.target, key=args.key, email=args.email)
    if args.match:
        m = args.match.lower(); jobs = [j for j in jobs if m in j["title"].lower()]

    if args.id:
        sel = next((j for j in jobs if str(j["id"]) == str(args.id)), None)
        if not sel:
            sys.exit(f"id {args.id} not found among {len(jobs)} postings (try --list).")
        if not sel.get("body") and args.provider in DETAIL:
            d = DETAIL[args.provider](args.target, args.id)
            sel["body"] = d.get("body", ""); sel["url"] = sel.get("url") or d.get("url", "")
        append_store(store, args.provider, [sel])  # ingest the selected job into the shared log
        md = to_posting_md(sel, args.provider)
        if args.out:
            sh = simhash(sel["title"] + " " + sel.get("body", "")[:2000])
            dup = _ledger_check_append(_ledger(args.out, args.ledger), args.provider, sel, sh)
            if dup:
                print(f"⚠️  possible cross-listing/duplicate of previously-seen: {dup!r}")
            if _alive(sel.get("url", "")) is False:
                print("⚠️  source_url did not respond OK — posting may be expired.")
            open(args.out, "w").write(md); print("wrote:", args.out)
        else:
            print(md)
        return

    if not jobs:
        print(f"No postings for {args.provider}:{args.target} (company may not use this ATS, or the slug differs)."); return
    print(f"{len(jobs)} posting(s):")
    for j in jobs:
        print(f"  - {j['title']}  |  {j.get('location','')}  |  id={j['id']}  |  {j.get('url','')}")


if __name__ == "__main__":
    main()
