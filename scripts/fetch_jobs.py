#!/usr/bin/env python3
"""
fetch_jobs.py — flexible, keyless-first job sourcing for Stage 5.

Public ATS providers (no key): greenhouse, lever, ashby — fetched per company/board.
Keyed provider: usajobs (free key + email/User-Agent; US federal).
LinkedIn is intentionally NOT here — it's the DEFAULT source but done via "claude-fetch"
(Claude WebFetches the guest endpoints), which is more robust than scripting and keeps this
tool off LinkedIn's ToS gray area. See references/05-coaching.md.

Stdlib only (urllib) — no pip deps.

List roles at a company:
    python fetch_jobs.py greenhouse gitlab --list [--match "data scientist"]
Save one posting to our posting.md format:
    python fetch_jobs.py greenhouse gitlab --id 8503792002 --out data/<user>/targets/<slug>/posting.md
USAJobs (keyed):
    python fetch_jobs.py usajobs "data scientist" --list --key $USAJOBS_KEY --email you@example.com

ToS/storage note: public ATS boards (Greenhouse/Lever/Ashby) are keyless embeds — fetch per
company, cache lightly, attribute the employer; don't bulk-harvest. USAJobs is public-domain and
freely storable. Keep it small-batch and personal.
"""
import argparse, html, json, re, sys, urllib.request, urllib.parse, datetime

UA = "corpus-vitae/1.0 (personal job search; +https://github.com/corpus-vitae)"


def _get(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _get_json(url, headers=None):
    return json.loads(_get(url, headers))


def _strip_html(s):
    if not s:
        return ""
    s = html.unescape(s)  # decode &lt;div&gt; -> <div> BEFORE stripping tags
    s = re.sub(r"(?i)<\s*br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</\s*(p|div|li|h[1-6])\s*>", "\n", s)
    s = re.sub(r"(?i)<\s*li[^>]*>", "• ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)  # any entities exposed after tag removal
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# each provider returns a list of dicts: id,title,company,location,url,employment_type,department,comp,body
def greenhouse(company, **kw):
    data = _get_json(f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true")
    out = []
    for j in data.get("jobs", []):
        out.append({
            "id": str(j.get("id", "")), "title": j.get("title", ""), "company": company,
            "location": (j.get("location") or {}).get("name", ""), "url": j.get("absolute_url", ""),
            "employment_type": "", "department": ", ".join(d.get("name", "") for d in j.get("departments", []) or []),
            "comp": "", "body": _strip_html(j.get("content", "")),
        })
    return out


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
        out.append({
            "id": j.get("id", ""), "title": j.get("text", ""), "company": company,
            "location": cat.get("location", ""), "url": j.get("hostedUrl", ""),
            "employment_type": cat.get("commitment", ""), "department": cat.get("team", ""),
            "comp": "", "body": body.strip(),
        })
    return out


def ashby(board, **kw):
    data = _get_json(f"https://api.ashbyhq.com/posting-api/job-board/{board}?includeCompensation=true")
    out = []
    for j in data.get("jobs", []):
        comp = ""
        cc = j.get("compensation") or {}
        if isinstance(cc, dict):
            comp = cc.get("compensationTierSummary", "") or ""
        body = j.get("descriptionPlain", "") or _strip_html(j.get("descriptionHtml", ""))
        out.append({
            "id": j.get("id", ""), "title": j.get("title", ""), "company": board,
            "location": j.get("location", ""), "url": j.get("jobUrl", ""),
            "employment_type": j.get("employmentType", ""), "department": j.get("departmentName", ""),
            "comp": comp, "body": body.strip(),
        })
    return out


def usajobs(keyword, key=None, email=None, **kw):
    if not key or not email:
        sys.exit("usajobs needs --key <API key> and --email <registered email>. "
                 "Get a free key at https://developer.usajobs.gov/apirequest/")
    url = "https://data.usajobs.gov/api/search?" + urllib.parse.urlencode({"Keyword": keyword, "ResultsPerPage": 25})
    data = _get_json(url, headers={"Host": "data.usajobs.gov", "User-Agent": email, "Authorization-Key": key})
    out = []
    for item in data.get("SearchResult", {}).get("SearchResultItems", []):
        d = item.get("MatchedObjectDescriptor", {})
        pay = (d.get("PositionRemuneration") or [{}])[0]
        out.append({
            "id": d.get("PositionID", ""), "title": d.get("PositionTitle", ""),
            "company": (d.get("OrganizationName", "")), "location": ", ".join(l.get("LocationName", "") for l in d.get("PositionLocation", []) or []),
            "url": d.get("PositionURI", ""), "employment_type": ", ".join(d.get("PositionSchedule", [{}])[0].get("Name", "") for _ in [0]) if d.get("PositionSchedule") else "",
            "department": d.get("DepartmentName", ""), "comp": f"{pay.get('MinimumRange','')}-{pay.get('MaximumRange','')} {pay.get('RateIntervalCode','')}".strip(),
            "body": _strip_html((d.get("UserArea", {}).get("Details", {}) or {}).get("JobSummary", "")),
        })
    return out


PROVIDERS = {"greenhouse": greenhouse, "lever": lever, "ashby": ashby, "usajobs": usajobs}


def to_posting_md(job, provider):
    today = datetime.date.today().isoformat()
    return (f"# {job['title']} — {job['company']}\n\n"
            f"- source_url: {job.get('url','')}\n"
            f"- employer: {job['company']}\n"
            f"- location: {job.get('location','')}\n"
            f"- date_seen: {today}\n"
            f"- salary: {job.get('comp','') or 'not listed'}\n"
            f"- employment_type: {job.get('employment_type','')}\n"
            f"- department: {job.get('department','')}\n"
            f"- provider: {provider}\n\n"
            f"## Full text\n{job.get('body','')}\n")


def main():
    ap = argparse.ArgumentParser(description="Fetch job postings from public ATS providers.")
    ap.add_argument("provider", choices=list(PROVIDERS))
    ap.add_argument("target", help="company/board slug (greenhouse/lever/ashby) or keyword (usajobs)")
    ap.add_argument("--list", action="store_true", help="print matching roles (title | location | id | url)")
    ap.add_argument("--match", default="", help="case-insensitive title filter")
    ap.add_argument("--id", default=None, help="select one posting by id and write --out")
    ap.add_argument("--out", default=None, help="write the selected posting to this posting.md path")
    ap.add_argument("--key", default=None); ap.add_argument("--email", default=None)
    args = ap.parse_args()

    jobs = PROVIDERS[args.provider](args.target, key=args.key, email=args.email)
    if args.match:
        m = args.match.lower(); jobs = [j for j in jobs if m in j["title"].lower()]

    if args.id:
        sel = next((j for j in jobs if str(j["id"]) == str(args.id)), None)
        if not sel:
            sys.exit(f"id {args.id} not found among {len(jobs)} postings (try --list).")
        md = to_posting_md(sel, args.provider)
        if args.out:
            open(args.out, "w").write(md); print("wrote:", args.out)
        else:
            print(md)
        return

    # default: list
    if not jobs:
        print(f"No postings found for {args.provider}:{args.target} "
              f"(company may not use this ATS, or the slug differs)."); return
    print(f"{len(jobs)} posting(s):")
    for j in jobs:
        print(f"  - {j['title']}  |  {j.get('location','')}  |  id={j['id']}  |  {j.get('url','')}")


if __name__ == "__main__":
    main()
