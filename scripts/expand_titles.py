#!/usr/bin/env python3
"""
expand_titles.py — beat the "title trap" (v1.8).

Searching by one literal title (e.g. "data scientist") silently misses the roles a person is
actually best at, because orgs label the same work inconsistently ("VP of Growth",
"Head of Monetization", "Chief of Staff", "Head of Strategic Data Opportunities"). The fix is to
search by the user's *value thesis*: derive a few role ARCHETYPES, pick seed titles, and let the
LLM (Claude, in-conversation) expand each seed into a wide neighbor set of adjacent titles across
company stages — the "radius search". Titles become search *hints* (recall); the JD body + the
Stage-6 capability fit decide what to keep (precision).

This script is the DETERMINISTIC driver around that expansion — it never calls an API/LLM itself:
  * default mode  — read the Claude-authored title-search config → dedup/normalize the union of
                    titles → write a ready-to-run SEARCH PLAN (LinkedIn guest search URLs +
                    usajobs commands) grouped by archetype.
  * --attribute   — tag each already-fetched job in the shared store to the archetype whose title
                    best matches the job title, so coaching + the dashboard can group by archetype.

Input config (data/<user>/title-search.json), authored by Claude in Stages 4-5:
  {
    "value_thesis": "find a revenue lever, model it, build it, own the decision end-to-end",
    "location": {"geoId": "103644278", "label": "United States"},
    "archetypes": [
      {"name": "Revenue-Lever Owner",
       "seed_titles": ["VP of Growth", "Head of Monetization"],
       "expanded_titles": ["VP of Growth", "Head of Monetization", "Director of Growth",
                           "Head of Revenue Operations", "GM, Growth", ...]},
      ...
    ]
  }

Usage:
  python scripts/expand_titles.py --user dylan
  python scripts/expand_titles.py --user dylan --attribute
  python scripts/expand_titles.py --config data/dylan/title-search.json --user-dir data/dylan
"""
import argparse
import datetime
import json
import os
import re
from urllib.parse import quote_plus

US_GEOID = "103644278"  # LinkedIn geoId for "United States" (see references/05-coaching.md)


def load_json(path):
    with open(path) as f:
        return json.load(f)


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


def norm(title):
    """Normalize a title for display (collapse whitespace, strip)."""
    return re.sub(r"\s+", " ", (title or "").strip())


def dedup_key(title):
    """Case-insensitive key so 'VP of Growth' and 'vp of growth' collapse."""
    return norm(title).lower()


def archetype_titles(arch):
    """Expanded titles for an archetype, falling back to its seed titles."""
    titles = arch.get("expanded_titles") or arch.get("seed_titles") or []
    seen, out = set(), []
    for t in titles:
        t = norm(t)
        if t and dedup_key(t) not in seen:
            seen.add(dedup_key(t))
            out.append(t)
    return out


def linkedin_url(title, geoid):
    return ("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
            f"?keywords={quote_plus(title)}&geoId={geoid}&start=0")


def usajobs_cmd(title):
    return f'python scripts/fetch_jobs.py usajobs "{title}" --list'


def build_plan(config, out_path):
    geoid = (config.get("location") or {}).get("geoId") or US_GEOID
    label = (config.get("location") or {}).get("label") or "United States"
    archetypes = config.get("archetypes") or []

    # dedup across archetypes: first archetype that names a title "owns" it in the plan
    seen = set()
    groups = []  # [(archetype_name, [titles])]
    total_titles = 0
    for arch in archetypes:
        name = arch.get("name") or "(unnamed archetype)"
        titles = []
        for t in archetype_titles(arch):
            k = dedup_key(t)
            if k in seen:
                continue
            seen.add(k)
            titles.append(t)
        if titles:
            groups.append((name, titles))
            total_titles += len(titles)

    lines = []
    lines.append("# Title search plan")
    lines.append("")
    lines.append(f"**Value thesis:** {config.get('value_thesis', '(not set)')}")
    lines.append("")
    lines.append(f"**Location:** {label} (geoId `{geoid}`)")
    lines.append("")
    lines.append(f"**{len(groups)} archetype(s) · {total_titles} unique title(s)** after dedup.")
    lines.append("")
    lines.append("> Titles are search *hints* for RECALL — cast wide. The JD body + the Stage-6")
    lines.append("> capability/value-fit read decide what to keep (PRECISION). Expect the best")
    lines.append("> strategic roles to have low *literal* fit and high *value* fit.")
    lines.append("")
    lines.append("Run the LinkedIn guest search via `WebFetch` (the `linkedin-claude-fetch`")
    lines.append("provider); page with `&start=25`, `&start=50`, ... The usajobs command needs a")
    lines.append("free key/email (see `preferences.json`). Both ingest into `data/_shared/jobs.jsonl`.")
    lines.append("")

    for name, titles in groups:
        lines.append(f"## {name}")
        lines.append("")
        for t in titles:
            lines.append(f"- **{t}**")
            lines.append(f"  - LinkedIn: {linkedin_url(t, geoid)}")
            lines.append(f"  - usajobs:  `{usajobs_cmd(t)}`")
        lines.append("")

    with open(out_path, "w") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    return len(groups), total_titles


def archetype_terms(config):
    """Ordered [(archetype_name, [match terms])]. Prefers an archetype's explicit `match_keywords`
    (short signal phrases like "quant", "monetization" — the robust choice for real title variety),
    falling back to its full expanded titles when no keywords are given. First archetype wins ties."""
    out = []
    for arch in config.get("archetypes") or []:
        name = arch.get("name") or "(unnamed archetype)"
        terms = arch.get("match_keywords") or archetype_titles(arch)
        terms = [norm(t) for t in terms if norm(t)]
        out.append((name, terms))
    return out


def attribute_jobs(config, jobs_path, out_path):
    arches = archetype_terms(config)

    # collapse jobs.jsonl -> latest record per job_key
    jobs = {}
    for e in load_jsonl(jobs_path):
        k = e.get("job_key")
        if k and (k not in jobs or e.get("ingested_at", "") >= jobs[k].get("ingested_at", "")):
            jobs[k] = e

    rows, matched, unmatched = [], 0, 0
    ts = datetime.date.today().isoformat()
    for k, job in jobs.items():
        jt = norm(job.get("title", "")).lower()
        # score each archetype by how many of its terms hit the job title; most hits wins (ties → first)
        best = None  # (score, archetype_name, matched_term)
        for name, terms in arches:
            hits = [t for t in terms if re.search(r"\b" + re.escape(t.lower()) + r"\b", jt)]
            if hits and (best is None or len(hits) > best[0]):
                best = (len(hits), name, max(hits, key=len))
        if best:
            rows.append({"job_key": k, "archetype": best[1], "matched_title": best[2], "ts": ts})
            matched += 1
        else:
            unmatched += 1

    # rewrite (idempotent) rather than append
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return matched, unmatched, len(jobs)


def main():
    ap = argparse.ArgumentParser(description="Expand seed titles into a search plan / attribute jobs.")
    ap.add_argument("--user", default=None)
    ap.add_argument("--user-dir", default=None)
    ap.add_argument("--shared", default="data/_shared")
    ap.add_argument("--config", default=None, help="title-search.json (default: <user-dir>/title-search.json)")
    ap.add_argument("--attribute", action="store_true", help="tag jobs.jsonl to archetypes instead of building a plan")
    a = ap.parse_args()

    user_dir = a.user_dir or (f"data/{a.user}" if a.user else None)
    if not user_dir:
        ap.error("provide --user NAME or --user-dir PATH")
    config_path = a.config or os.path.join(user_dir, "title-search.json")
    if not os.path.exists(config_path):
        ap.error(f"no title-search config at {config_path} — author it in Stages 4-5 first "
                 f"(template: templates/title-search.example.json)")
    config = load_json(config_path)
    os.makedirs(user_dir, exist_ok=True)

    if a.attribute:
        jobs_path = os.path.join(a.shared, "jobs.jsonl")
        out_path = os.path.join(user_dir, "job-archetype.jsonl")
        matched, unmatched, total = attribute_jobs(config, jobs_path, out_path)
        print(f"attributed {matched}/{total} job(s) to archetypes → {out_path} "
              f"({unmatched} unmatched)")
    else:
        out_path = os.path.join(user_dir, "title-search-plan.md")
        groups, titles = build_plan(config, out_path)
        print(f"search plan → {out_path}  [{groups} archetype(s), {titles} unique title(s)]")


if __name__ == "__main__":
    main()
