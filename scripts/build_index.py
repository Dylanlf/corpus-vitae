#!/usr/bin/env python3
"""
build_index.py — build the derived, rebuildable SQLite index from the canonical JSONL files.

Reads (source of truth; append-only, human-readable):
  data/_shared/jobs.jsonl        (job ingestion events)
  data/_shared/companies.jsonl   (company intel snapshots)
  data/<user>/interactions.jsonl (like/dislike/hide/status events)
  data/<user>/fit.jsonl          (per-user fit scores)
Writes (derived; gitignored; NEVER the source of truth):
  data/<user>/index.db           (tables: jobs, companies, interactions, fit)

Delete index.db and rerun → identical result. Derives temporal signal (first_ingested/last_seen/
times_seen) and SimHash cross-listing clusters (dedup_group + repost flags). Stdlib only.

Usage:  python build_index.py --user dylan
        python build_index.py --shared data/_shared --user-dir data/dylan --out data/dylan/index.db
"""
import argparse, datetime, json, os, re, sqlite3


def load_jsonl(path):
    if not path or not os.path.exists(path):
        return []
    out = []
    for line in open(path):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def norm_company(name):
    return re.sub(r"[^a-z0-9]+", "", (name or "").lower())


def hamming(a, b):
    return bin(int(a) ^ int(b)).count("1")


def days_between(a, b):
    try:
        da = datetime.date.fromisoformat(a[:10]); db = datetime.date.fromisoformat(b[:10])
        return (db - da).days
    except Exception:
        return None


def collapse_jobs(events):
    """events: list of ingestion records for possibly-repeated job_keys → per-job_key latest + temporal."""
    by_key = {}
    for e in events:
        k = e.get("job_key")
        if not k:
            continue
        g = by_key.setdefault(k, {"events": []})
        g["events"].append(e)
    jobs = {}
    for k, g in by_key.items():
        evs = sorted(g["events"], key=lambda x: x.get("ingested_at", ""))
        latest = evs[-1]
        jobs[k] = dict(latest)
        jobs[k]["first_ingested"] = evs[0].get("ingested_at", "")
        jobs[k]["last_seen"] = evs[-1].get("ingested_at", "")
        jobs[k]["times_seen"] = len(evs)
    return jobs


def cluster_and_repost(jobs):
    """SimHash union-find over jobs → dedup_group + repost flags (initial = earliest first_ingested)."""
    keys = list(jobs)
    parent = {k: k for k in keys}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for i in range(len(keys)):
        si = jobs[keys[i]].get("simhash")
        if si is None:
            continue
        for j in range(i + 1, len(keys)):
            sj = jobs[keys[j]].get("simhash")
            if sj is not None and hamming(si, sj) <= 3:
                union(keys[i], keys[j])

    groups = {}
    for k in keys:
        groups.setdefault(find(k), []).append(k)
    for members in groups.values():
        # initial = earliest first_ingested (posted_date used as tiebreaker when present)
        initial = min(members, key=lambda k: (jobs[k].get("posted_date") or jobs[k].get("first_ingested", "")))
        latest_seen = max(jobs[k].get("last_seen", "") for k in members)
        open_days = days_between(jobs[initial].get("first_ingested", ""), latest_seen)
        for k in members:
            jobs[k]["dedup_group"] = initial
            jobs[k]["is_repost"] = 0 if k == initial else 1
            jobs[k]["repost_of"] = "" if k == initial else initial
            jobs[k]["repost_count"] = len(members) - 1
            jobs[k]["days_open"] = open_days if open_days is not None else ""
    return jobs


def latest_by(records, key_fields, ts_field="ts"):
    """Keep the latest record per tuple(key_fields)."""
    best = {}
    for r in records:
        key = tuple(r.get(f, "") for f in key_fields)
        if key not in best or r.get(ts_field, "") >= best[key].get(ts_field, ""):
            best[key] = r
    return best


def build(shared, user_dir, out):
    jobs = collapse_jobs(load_jsonl(os.path.join(shared, "jobs.jsonl")))
    jobs = cluster_and_repost(jobs)
    companies = latest_by(load_jsonl(os.path.join(shared, "companies.jsonl")), ["company_key"], "fetched_at")
    # interactions: latest per (job_key, dimension) — dimension: 'rating' events vs 'status' events
    inter_events = load_jsonl(os.path.join(user_dir, "interactions.jsonl"))
    ratings = latest_by([e for e in inter_events if e.get("event") in ("like", "dislike", "hide")], ["job_key"], "ts")
    statuses = latest_by([e for e in inter_events if e.get("event") == "status"], ["job_key"], "ts")
    notes = latest_by([e for e in inter_events if e.get("note")], ["job_key"], "ts")
    # fit: prefer an analyzed score over any heuristic; else latest by ts
    fit_rows = load_jsonl(os.path.join(user_dir, "fit.jsonl"))
    fit = {}
    for r in fit_rows:
        k = r.get("job_key")
        if not k:
            continue
        cur = fit.get(k)
        if cur is None:
            fit[(k,)] = r; fit[k] = r; continue
        cur_analyzed = cur.get("method") == "analyzed"
        new_analyzed = r.get("method") == "analyzed"
        if (new_analyzed and not cur_analyzed) or \
           (new_analyzed == cur_analyzed and r.get("ts", "") >= cur.get("ts", "")):
            fit[(k,)] = r; fit[k] = r
    fit = {kk: v for kk, v in fit.items() if isinstance(kk, tuple)}

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    if os.path.exists(out):
        os.remove(out)  # idempotent: rebuild from scratch
    db = sqlite3.connect(out)
    db.executescript("""
      CREATE TABLE jobs(job_key TEXT PRIMARY KEY, source TEXT, company TEXT, company_key TEXT,
        title TEXT, location TEXT, url TEXT, salary_raw TEXT, employment_type TEXT, department TEXT,
        posted_date TEXT, first_ingested TEXT, last_seen TEXT, times_seen INT, simhash TEXT,
        dedup_group TEXT, is_repost INT, repost_of TEXT, repost_count INT, days_open TEXT, body TEXT);
      CREATE TABLE companies(company_key TEXT PRIMARY KEY, name TEXT, sector TEXT, industry TEXT,
        employees TEXT, hq TEXT, founded TEXT, website TEXT, wikipedia_summary TEXT,
        salary_benchmark TEXT, rating_links TEXT, award_pointers TEXT, fetched_at TEXT);
      CREATE TABLE interactions(job_key TEXT PRIMARY KEY, rating TEXT, status TEXT, note TEXT, updated TEXT);
      CREATE TABLE fit(job_key TEXT PRIMARY KEY, literal_fit REAL, capability_fit REAL, desire REAL,
        screening_risk TEXT, method TEXT, matched_skills INT, corpus_hash TEXT, ts TEXT);
    """)
    for k, j in jobs.items():
        db.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            k, j.get("source", ""), j.get("company", ""), norm_company(j.get("company", "")),
            j.get("title", ""), j.get("location", ""), j.get("url", ""), j.get("salary_raw", ""),
            j.get("employment_type", ""), j.get("department", ""), j.get("posted_date", ""),
            j.get("first_ingested", ""), j.get("last_seen", ""), j.get("times_seen", 1),
            str(j.get("simhash", "")), j.get("dedup_group", ""), j.get("is_repost", 0),
            j.get("repost_of", ""), j.get("repost_count", 0), str(j.get("days_open", "")), j.get("body", "")))
    for ck, c in companies.items():
        db.execute("INSERT OR REPLACE INTO companies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            c.get("company_key", ck[0] if isinstance(ck, tuple) else ck), c.get("name", ""),
            c.get("sector", ""), c.get("industry", ""), str(c.get("employees", "")), c.get("hq", ""),
            str(c.get("founded", "")), c.get("website", ""), c.get("wikipedia_summary", ""),
            json.dumps(c.get("salary_benchmark", {})), json.dumps(c.get("rating_links", {})),
            json.dumps(c.get("award_pointers", [])), c.get("fetched_at", "")))
    for (jk,), r in ratings.items():
        db.execute("INSERT INTO interactions(job_key, rating, updated) VALUES (?,?,?) "
                   "ON CONFLICT(job_key) DO UPDATE SET rating=excluded.rating, updated=excluded.updated",
                   (jk, r.get("event", ""), r.get("ts", "")))
    for (jk,), r in statuses.items():
        db.execute("INSERT INTO interactions(job_key, status, updated) VALUES (?,?,?) "
                   "ON CONFLICT(job_key) DO UPDATE SET status=excluded.status, updated=excluded.updated",
                   (jk, r.get("status", ""), r.get("ts", "")))
    for (jk,), r in notes.items():
        db.execute("INSERT INTO interactions(job_key, note, updated) VALUES (?,?,?) "
                   "ON CONFLICT(job_key) DO UPDATE SET note=excluded.note",
                   (jk, r.get("note", ""), r.get("ts", "")))
    for (jk,), r in fit.items():
        db.execute("INSERT OR REPLACE INTO fit VALUES (?,?,?,?,?,?,?,?,?)", (
            jk, r.get("literal_fit"), r.get("capability_fit"), r.get("desire"),
            r.get("screening_risk", ""), r.get("method", ""), r.get("matched_skills"),
            r.get("corpus_hash", ""), r.get("ts", "")))
    db.commit()
    counts = {t: db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("jobs", "companies", "interactions", "fit")}
    reposts = db.execute("SELECT COUNT(*) FROM jobs WHERE is_repost=1").fetchone()[0]
    db.close()
    print(f"built {out}: {counts}; reposts flagged: {reposts}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=None, help="user name → data/<user> and data/_shared")
    ap.add_argument("--shared", default=None); ap.add_argument("--user-dir", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    shared = a.shared or "data/_shared"
    user_dir = a.user_dir or (f"data/{a.user}" if a.user else None)
    if not user_dir:
        ap.error("provide --user NAME or --user-dir PATH")
    out = a.out or os.path.join(user_dir, "index.db")
    build(shared, user_dir, out)


if __name__ == "__main__":
    main()
