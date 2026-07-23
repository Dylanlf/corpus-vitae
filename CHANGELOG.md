# Changelog

All notable changes to corpus-vitae. Versions are the `version` in `SKILL.md` frontmatter.

## 1.7.0

Added — **two-tier scoring** so the dashboard ranks the whole store, not just hand-analyzed jobs:
- **`scripts/prescore.py`** — fast, offline **heuristic** fit for every ingested job (capability ≈
  corpus-skill × JD overlap; desire ≈ goals directions/avoid; screening-risk ≈ degree/years/location
  knockouts). Writes `method:heuristic` rows to `fit.jsonl`, skips jobs already fresh under the current
  corpus, and re-scores when `corpus.json` changes. Strictly a triage sort — shown as "rough/~" and
  never presented as the real capability score.
- **`build_index.py`** now carries `method` and **prefers an `analyzed` score over any heuristic**;
  **`build_dashboard.py`** marks heuristic rows "rough/~". The deep Stage-6 analysis overrides the
  heuristic for top-N targets.

## 1.6.0

Added — job market DB, per-user overlay & at-a-glance dashboard:
- **Files-as-canon + derived SQLite** data model. Shared `data/_shared/jobs.jsonl` (append-only
  ingestion log; `fetch_jobs.py` now appends here) + `companies.jsonl`; per-user
  `data/<user>/interactions.jsonl` (like/dislike/status/notes) + `fit.jsonl` (Stage-6 scores).
- **`scripts/build_index.py`** → rebuildable `data/<user>/index.db` (tables jobs/companies/
  interactions/fit); derives `first_ingested`/`last_seen`/`times_seen` and SimHash `dedup_group` +
  **repost/ghost-job flags** (`repost_of`, `repost_count`, `days_open`). Idempotent.
- **`scripts/fetch_company_intel.py`** → firmographics from **Wikidata** (CC0) + **Wikipedia** (CC
  BY-SA) + salary benchmark from **BLS OEWS** (public domain); ratings/awards as **deep-link
  pointers only** (never scraped — Glassdoor has no legal API).
- **`scripts/build_dashboard.py`** → local, self-contained, theme-aware `data/<user>/dashboard.html`:
  best-fits-today ranked by capability×desire, with salary (posting or market benchmark), sector/size,
  repost signal, rating/award links, and status. Read-only snapshot.
- **`chrome-single`** Stage-5 source: logged-in real-Chrome fetch of a single login-gated posting
  (one at a time, human-directed — not list-scraping). New references `10-market-db.md`,
  `11-dashboard.md`; `preferences.json` gains `bls_key` + `chrome-single`.

## 1.5.0

Added — sourcing depth (structure ported from `santifer/career-ops`, MIT; see ATTRIBUTIONS):
- **SmartRecruiters** provider (keyless, incl. full description via its detail endpoint), joining
  Greenhouse/Lever/Ashby/USAJobs in `scripts/fetch_jobs.py`, behind an extensible provider registry.
- **SimHash cross-listing dedup** — flags near-identical JDs reposted across companies; a
  `scan-history.tsv` **append-only ledger** warns when a saved posting duplicates a prior one.
- **Liveness check** on save (warns if the source URL is dead/expired).
- **`scan` mode + portals config** (`templates/portals.example.json`) — list roles across many
  tracked companies at once, deduped.

## 1.4.0

Added:
- **Flexible job sourcing (Stage 5).** A provider layer instead of ad-hoc scraping: default
  **`linkedin-claude-fetch`** (LinkedIn guest endpoints via WebFetch — keyless, bypasses the SPA),
  plus **`scripts/fetch_jobs.py`** (stdlib, no deps) for keyless public ATS APIs
  (**Greenhouse, Lever, Ashby**) and keyed **USAJobs**, normalizing to `posting.md`. Honest
  per-provider ToS/storage notes; user-paste remains the always-available fallback.
- **Per-user preferences (`data/<user>/preferences.json`).** Defaults loaded at session start
  (template: `templates/preferences.example.json`): `honesty_dial` 6, `build_credit` true,
  `show_dial` false, `ai_narrative` false, `audience` traditional, `job_source`
  linkedin-claude-fetch, `output_formats` [md,pdf,docx], optional USAJobs key. Any per-run
  instruction overrides.

## 1.3.0

Added:
- **Stage 9 — Phone-screen prep** (`references/09-interview-prep.md` + `templates/interview-prep.md`):
  likely recruiter + hiring-manager questions with honest, corpus-grounded best answers, derived from
  four sources — the JD, the gap analysis (tough/gap questions), the résumé's claims ("defend-the-
  metric" drills = the defend-it-in-an-interview test made literal), and the narrative/goals
  (behavioral + motivation). Includes questions to ask back and comp/logistics *framing* (no
  personalized salary-negotiation advice). Honesty rule: never script a claim the user can't truly
  defend — if prep surfaces one, fix the résumé, don't rehearse a spin.

## 1.2.0

Added — the "callability & real output formats" release:

- **Stage 7.5 — Callability review** (`references/07b-callability-review.md` + `templates/callability-scorecard.md`):
  an evidence-weighted 7-dimension callability scorecard + a ranked knockout/red-flag checklist, to
  estimate a résumé's chance of passing the ATS + recruiter screen before sending. Grounded in the
  Ladders eye-tracking scan, Kroft/NBER gap penalties, Chicago Booth tenure data, the HBS/Accenture
  "Hidden Workers" report (ATS ranks/buries, rarely auto-rejects — knockouts are the real gate), and a
  ~500k-user writing-clarity study (AI *assistance* helps, generic AI *voice* hurts).
- **Stage 8 — Format / export** (`references/08-formatting.md`): produce a single-column, ATS-safe,
  text-layer **PDF** and **DOCX** from the tailored résumé, with a copy-ready design spec (fonts, sizes,
  margins, section order, file naming). Supersedes v1's Markdown-only output.

## 1.1.0

Added — the "story & strategy" release:

- **Stage 2.5 — Narrative interview** (`references/02b-narrative-interview.md`): a distinct pass
  eliciting growth arc, learning agility, differentiation, operating principles, and motivation —
  the disposition/trajectory evidence that makes the honest case for stretch roles. Stored
  corpus-level in `x_cv.narrative`, evidence-backed. Informed by narrative career-construction
  methods (Savickas, Ibarra, Ganz, hero's journey, learning agility) — see `ATTRIBUTIONS.md`.
- **Two-layer fit** in Stage 6: separate **literal fit** (predicts screening risk) from
  **capability / true-need fit** (can you do the real job?), plus a **screening-risk** rating and
  **strategy routing** (when capability ≫ literal, bypass the filter via referral + cover narrative
  rather than keyword-optimizing).
- **Stage 5.5 — Fit calibration ladder** (`references/05b-calibration.md`, *experimental stub*):
  show jobs across fit bands (3/5/7/9) and run a rescore loop that enriches the corpus from user
  pushback.
- **Honest AI provenance** (Stage 7): internal build metadata in the résumé's JSON Resume `meta`
  object (dial number **never printed**), an optional neutral build-credit footer, and an opt-in,
  audience-gated **AI-use narrative** framing corpus-vitae as a product the user built.

## 1.0.0

- Initial 7-stage pipeline (intake → experience interview → knowledge base → goals → coaching →
  scoring + gaps → tailoring), JSON Resume + `x_cv` data model, the 0–10 honesty dial with a
  no-fabrication floor, and the public-machinery / private-`data/` split.
