#!/usr/bin/env python3
"""
fetch_company_intel.py — company/market intel for the dashboard, from redistribution-clean sources.

STORES (fetch + keep): firmographics from Wikidata (CC0) + Wikipedia summary (CC BY-SA) and a salary
benchmark from BLS OEWS (US-gov public domain). POINTERS ONLY (URLs, never scraped values): company
ratings (Glassdoor/Indeed/Comparably/Levels) and awards — deep-link the user to the source. Glassdoor
has no legal API and forbids scraping; we never fetch/store its numbers. Stdlib only.

Usage:
  python fetch_company_intel.py "Anthropic" --title "data scientist"
  python fetch_company_intel.py "Whatnot" --soc 15-2051 --store data/_shared/companies.jsonl
Optional --bls-key uses the BLS v2 API (free key, higher quota) in one batched call.

Attribution (record in ATTRIBUTIONS.md): Wikidata CC0; Wikipedia CC BY-SA; BLS OEWS public domain.
Firmographics coverage is thin for small private companies; salary benchmark is OCCUPATION-level
(national), shown as market context, not a company-specific promise.
"""
import argparse, datetime, json, os, re, urllib.request, urllib.parse

UA = "corpus-vitae/1.0 (personal job-search; +https://github.com/corpus-vitae)"
DEFAULT_STORE = "data/_shared/companies.jsonl"

# minimal title -> SOC (2018) map for salary benchmarks; extend as needed
SOC_MAP = {
    "data scientist": "15-2051", "data science": "15-2051", "machine learning": "15-2051",
    "data engineer": "15-2051", "data analyst": "15-2041", "statistician": "15-2041",
    "software engineer": "15-1252", "software": "15-1252", "developer": "15-1252",
    "product manager": "11-2021", "analytics manager": "11-3021", "engineering manager": "11-9041",
    "financial analyst": "13-2051", "operations": "11-1021", "marketing": "13-1161",
}
# BLS OEWS national annual datatypes
DT = {"median": "13", "p10": "11", "p25": "12", "p75": "14", "p90": "15"}


def _get(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _json(url, headers=None, timeout=20):
    return json.loads(_get(url, headers, timeout))


def norm_company(name):
    return re.sub(r"[^a-z0-9]+", "", (name or "").lower())


def soc_for(title, soc):
    if soc:
        return soc
    t = (title or "").lower()
    for kw, code in SOC_MAP.items():
        if kw in t:
            return code
    return None


def wikidata(name):
    """Resolve a company on Wikidata → firmographics (labels resolved)."""
    s = _json("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbsearchentities", "search": name, "language": "en", "format": "json",
         "type": "item", "limit": 1}))
    if not s.get("search"):
        return {}
    qid = s["search"][0]["id"]
    ent = _json(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json")["entities"][qid]
    claims = ent.get("claims", {})

    def val(pid):
        try:
            return claims[pid][0]["mainsnak"]["datavalue"]["value"]
        except Exception:
            return None

    def qid_of(pid):
        v = val(pid)
        return v.get("id") if isinstance(v, dict) and "id" in v else None

    industry_q, hq_q = qid_of("P452"), qid_of("P159")
    labels = {}
    ids = [q for q in (industry_q, hq_q) if q]
    if ids:
        ld = _json("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
            {"action": "wbgetentities", "ids": "|".join(ids), "props": "labels",
             "languages": "en", "format": "json"}))
        for q in ids:
            labels[q] = ld.get("entities", {}).get(q, {}).get("labels", {}).get("en", {}).get("value", "")
    emp = val("P1128"); founded = val("P571"); site = val("P856")
    return {
        "wikidata_id": qid,
        "industry": labels.get(industry_q, ""),
        "sector": labels.get(industry_q, ""),
        "employees": (emp.get("amount", "").lstrip("+") if isinstance(emp, dict) else ""),
        "hq": labels.get(hq_q, ""),
        "founded": (founded.get("time", "")[1:5] if isinstance(founded, dict) else ""),
        "website": (site if isinstance(site, str) else ""),
        "wp_title": ent.get("sitelinks", {}).get("enwiki", {}).get("title", ""),
    }


def wikipedia_summary(title):
    if not title:
        return ""
    try:
        d = _json(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}")
        return d.get("extract", "")
    except Exception:
        return ""


def bls_series(soc, dt):
    return f"OEUN0000000000000{soc.replace('-', '')}{dt}"


def bls_oews(soc, key=None):
    if not soc:
        return {}
    # fetch order puts the most useful figures first so a partial result is still useful
    order = ["median", "p25", "p75", "p10", "p90"]
    series = {name: bls_series(soc, DT[name]) for name in order}
    out = {"soc": soc, "geo": "national", "source": "BLS OEWS"}
    if key:  # v2: one batched call for all series
        try:
            body = json.dumps({"seriesid": list(series.values()), "registrationkey": key}).encode()
            req = urllib.request.Request("https://api.bls.gov/publicAPI/v2/timeseries/data/",
                                         data=body, headers={"Content-Type": "application/json", "User-Agent": UA})
            res = json.loads(urllib.request.urlopen(req, timeout=30).read())
            got = {s["seriesID"]: s for s in res.get("Results", {}).get("series", [])}
            for name, sid in series.items():
                data = got.get(sid, {}).get("data", [])
                out[name] = data[0]["value"] if data else ""
        except Exception as e:
            out["error"] = str(e)
    else:      # v1 keyless: one series per call, each independently fault-tolerant
        for name, sid in series.items():
            try:
                d = _json(f"https://api.bls.gov/publicAPI/v1/timeseries/data/{sid}", timeout=30)
                data = d.get("Results", {}).get("series", [{}])[0].get("data", [])
                if data:
                    out[name] = data[0]["value"]
            except Exception:
                continue  # skip this datatype; keep the ones we got
    return out


def pointer_links(name):
    q = urllib.parse.quote_plus(name)
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return {
        "glassdoor": f"https://www.glassdoor.com/Search/results.htm?keyword={q}",
        "indeed": f"https://www.indeed.com/cmp/{slug}/reviews",
        "comparably": f"https://www.comparably.com/companies/{slug}",
        "levels": f"https://www.levels.fyi/companies/{slug}/salaries",
        "linkedin": f"https://www.linkedin.com/company/{slug}",
    }


def award_pointers(name):
    q = urllib.parse.quote_plus(f"{name} best places to work award")
    # WebSearch (by Claude) fills specifics; store a starting pointer + a slot for confirmed awards.
    return [{"name": "search: best-places / awards", "url": f"https://www.google.com/search?q={q}"}]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("company")
    ap.add_argument("--title", default="", help="role title → infer SOC for the salary benchmark")
    ap.add_argument("--soc", default="", help="explicit SOC code (overrides --title)")
    ap.add_argument("--bls-key", default=None)
    ap.add_argument("--store", default=DEFAULT_STORE)
    ap.add_argument("--print", action="store_true", help="print the snapshot instead of appending")
    a = ap.parse_args()

    firmo = wikidata(a.company)
    summary = wikipedia_summary(firmo.get("wp_title", "") or a.company)
    soc = soc_for(a.title, a.soc)
    salary = bls_oews(soc, a.bls_key) if soc else {}

    snap = {
        "company_key": norm_company(a.company), "name": a.company,
        "sector": firmo.get("sector", ""), "industry": firmo.get("industry", ""),
        "employees": firmo.get("employees", ""), "hq": firmo.get("hq", ""),
        "founded": firmo.get("founded", ""), "website": firmo.get("website", ""),
        "wikidata_id": firmo.get("wikidata_id", ""), "wikipedia_summary": summary,
        "salary_benchmark": salary, "rating_links": pointer_links(a.company),
        "award_pointers": award_pointers(a.company),
        "sources": {"firmographics": "Wikidata (CC0) + Wikipedia (CC BY-SA)",
                    "salary": "BLS OEWS (public domain)" if soc else ""},
        "fetched_at": datetime.date.today().isoformat(),
    }
    if a.print:
        print(json.dumps(snap, indent=2, ensure_ascii=False)); return
    os.makedirs(os.path.dirname(a.store) or ".", exist_ok=True)
    with open(a.store, "a") as f:
        f.write(json.dumps(snap, ensure_ascii=False) + "\n")
    print(f"appended intel for {a.company} → {a.store}"
          f"  (sector={snap['sector']!r}, employees={snap['employees']!r}, "
          f"salary median={salary.get('median','n/a')})")


if __name__ == "__main__":
    main()
