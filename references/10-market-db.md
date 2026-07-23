# Job market DB — data model & build

A local, queryable store of jobs + company intel + your interactions, so a pile of postings becomes a
searchable job-search cockpit. **Files are canon; SQLite is a rebuildable index.** All under gitignored
`data/`. Feeds the dashboard (`references/11-dashboard.md`).

## Generic vs per-user
- **Generic / shared** (`data/_shared/`, fetched once, same for everyone): `jobs.jsonl`, `companies.jsonl`.
- **Per-user** (`data/<user>/`, depends on you): `interactions.jsonl`, `fit.jsonl`, and the derived
  `index.db` + `dashboard.html`.
- **Hand-curated stays files** (unchanged): `corpus.json`, `goals.md`, `preferences.json`, `portals.json`.

## Canonical files (append-only, human-readable JSONL)
- `data/_shared/jobs.jsonl` — one line per *fetch event*. `fetch_jobs.py` appends here (scan ingests
  all matches; `--id` ingests the one). Re-fetching later adds a line → temporal signal. Key fields:
  `job_key ("<source>:<source_id>"), company, title, location, url, salary_raw, ingested_at, simhash, body`.
- `data/_shared/companies.jsonl` — one intel snapshot per company (`fetch_company_intel.py`). **Stored**
  firmographics + salary benchmark; **pointer-only** rating/award URLs (never scraped values).
- `data/<user>/interactions.jsonl` — append-only events: `{job_key, event: like|dislike|hide|status,
  status?, note?, ts}`. Latest per (job_key, dimension) wins. Add events via the skill/CLI (append a line).
- `data/<user>/fit.jsonl` — per-user fit cache from Stage 6: `{job_key, literal_fit, capability_fit,
  desire, screening_risk, corpus_hash, ts}`. Stale when `corpus_hash` != current corpus → recompute.

## Identity, dedup, temporal (derived in the index)
- **Job identity:** `job_key = "<source>:<source_id>"`.
- **Dedup / cross-listing:** `build_index.py` clusters jobs by **SimHash** (Hamming ≤ 3) into a
  `dedup_group`; the earliest is the **initial**, later ones are `is_repost=1` with `repost_of`,
  `repost_count`, `days_open`. Surfaces "reposted 4× · open 90+ days" — a ghost-job/hard-to-fill signal
  (feeds Stage-6 legitimacy). Honest caveat: `posted_date` is unreliable across sources, so
  `first_ingested` is a floor, not the true original post date.
- **Temporal:** per `job_key`, the index derives `first_ingested`, `last_seen`, `times_seen`.

## Build the index (rebuildable; never the source of truth)
```
python scripts/build_index.py --user <user>
```
Reads the four JSONL files → `data/<user>/index.db` (tables `jobs, companies, interactions, fit`).
Idempotent: delete `index.db` and rebuild → identical. If it ever disagrees with the JSONL, the JSONL wins.

## Company intel (honest sources)
```
python scripts/fetch_company_intel.py "<Company>" --title "<role>"   # → appends companies.jsonl
```
- **STORE** (redistribution-clean): **Wikidata** (CC0 — sector, employees, HQ, founded, website),
  **Wikipedia** REST summary (CC BY-SA → attribution), **BLS OEWS** salary benchmark (public domain;
  keyless v1, or a free `bls_key` in `preferences.json` for the batched v2). Salary is **occupation-
  level, national** (SOC via `--soc`/`--title`) — market context, not a company-specific promise.
- **POINTER ONLY** (URLs, never scraped/stored values): Glassdoor / Indeed / Comparably / Levels
  ratings, and awards (WebSearch → deep-link). Glassdoor has no legal API and forbids scraping.
- Coverage is thin for small private companies (Wikidata gap) — say so; don't fabricate.

Attribution recorded in `ATTRIBUTIONS.md` (Wikidata CC0, Wikipedia CC BY-SA, BLS public domain; the
files-canon + derived-SQLite pattern is from career-ops, MIT).

**Next:** `references/11-dashboard.md` to render the at-a-glance view.
