# Stage 5 — Coaching (titles, directions, and real postings)

**Goal:** turn the directions from stage 4 into concrete **job titles** and a shortlist of
**real job postings** to aim at — coaching the user with actual market examples and iterating
on their feedback. Output is one folder per target job under `data/targets/<slug>/` containing
the saved `posting.md`.

Read `data/kb/corpus.json` and `data/goals.md` first.

## 1. From value thesis → archetypes → a wide title set (beat the "title trap")

Don't start from a single obvious title — that *silently* misses the roles the user is best at,
because the same work wears different labels across orgs ("VP of Growth" ≈ "Head of Monetization"
≈ "Chief of Staff" ≈ "Head of Strategic Data Opportunities"). Start from the **value thesis** and
**desired role attributes** in `goals.md` and work outward:

1. **Derive 3–5 role archetypes** from the value thesis — clusters of roles that all deliver that
   function (e.g. *Revenue-Lever Owner*, *0→1 Data/Growth Leader*, *Founder's Right-Hand / BizOps*).
   Give each a one-line "why this fits you" grounded in real corpus / `x_cv.narrative` entries, and
   note the move type (lateral / step-up / pivot).
2. **Pick 2–3 seed titles per archetype** — the clearest real-world labels (e.g. "VP of Growth",
   "Head of Monetization").
3. **Expand each seed into a wide neighbor set** — the "radius search": list the titles *semantically
   adjacent* to each seed **across company stages** (startup → scaleup → enterprise), including ones
   neither of you would think to filter for. You (Claude) are the expansion engine — use your
   internalized sense of the title space and cast wide, because recall is the whole point here and
   precision comes later from the JD read.
4. **Write it to `data/<user>/title-search.json`** (template: `templates/title-search.example.json`):
   value thesis, location `geoId`, and each archetype with its `seed_titles` + `expanded_titles`.
5. **Converge with the user first.** Present the **archetypes** (not the raw title list) and **ask
   which resonate**; drop/add archetypes on their feedback before sourcing. Don't boil the ocean —
   ~3–5 archetypes.

**Guiding principle: titles are search *hints*, not the filter.** They fill the funnel (recall);
what a role *actually owns* — read from the JD body and scored in Stage 6 — decides what to keep
(precision). Expect the best strategic roles to have **low literal fit but high value fit**, and a
pure title-radius to drift (e.g. "VP Growth" neighbors skew toward performance-marketing) — the JD
read is what corrects it.

### Build the search plan
```
python scripts/expand_titles.py --user <user>
```
Dedups the union of titles and writes `data/<user>/title-search-plan.md` — a ready-to-run set of
LinkedIn guest search URLs + `usajobs` commands, grouped by archetype. Run those via the sourcing
layer below (LinkedIn guest through `WebFetch`; usajobs through `fetch_jobs.py`); everything ingests
into `data/_shared/jobs.jsonl` as usual. After fetching, attribute results back to archetypes:
```
python scripts/expand_titles.py --user <user> --attribute
```
→ `data/<user>/job-archetype.jsonl` (`{job_key, archetype, matched_title}`), so coaching and the
dashboard can group by archetype. Attribution matches on each archetype's optional `match_keywords`
(short **function** signals like `quant` — *not* sector words like `fintech`, which would mis-tag a
fintech CMO), falling back to the expanded titles. Off-thesis drift (e.g. LinkedIn returning "VP
Marketing" for a "VP of Growth" search) correctly stays **unmatched** — that's the funnel working,
not a bug; the JD read in Stage 6 is the real precision gate.

## 2. Source real postings from the web

Find **real, current-or-recent** postings (recency isn't required, representativeness is), using
the flexible sourcing layer below. The default source is set in the user's preferences
(`job_source`, default `linkedin-claude-fetch`); switch per target as needed.

### Sourcing providers (flexible — pick per target)

Prefer **structured/keyless** sources; fall back to the user. Respect `goals.md` constraints
(location/remote, comp, industries) when choosing what to surface.

1. **`linkedin-claude-fetch` (default).** LinkedIn's **guest** endpoints are fetchable via
   `WebFetch` (built for logged-out users — no key, no login wall, and they bypass the SPA):
   - search list → `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=<kw>&geoId=103644278&start=0` (geoId 103644278 = US; page via `start`)
   - one posting → `https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}`
   Small-batch/personal only (ToS gray area; don't bulk-harvest). This is "claude-fetch": Claude
   reads the guest response directly.
1b. **`chrome-single` — logged-in real Chrome, ONE page.** For a single company/role of interest whose
   posting is login-gated or blocks `WebFetch` (a full LinkedIn posting, an authenticated careers
   portal), drive the user's **real Chrome** (`mcp__claude-in-chrome`) to open and read that one page.
   Honest discipline: a single, human-directed fetch of a page the user chose, via their own session —
   equivalent to them browsing to it — **not** list-scraping. One at a time; behave like normal
   browsing. Requires the Chrome extension connected; fall back to guest-fetch / paste if absent.
2. **Public ATS APIs via `scripts/fetch_jobs.py` (keyless, storable-per-ToS, most reliable):**
   - providers: **greenhouse · lever · ashby · smartrecruiters** (keyless). Add more by registering
     a `list(company)->[dict]` fn (endpoint patterns for Workable/Recruitee/etc. are known — verify
     a real slug first; no broken adapters).
   - `python scripts/fetch_jobs.py <provider> <company> --list [--match "director data"]`
   - then `... <provider> <company> --id <id> --out data/<user>/targets/<slug>/posting.md`
     (fetches the full body, appends to `targets/scan-history.tsv`, warns on a **SimHash
     cross-listing duplicate** or an **expired** posting).
   - **Scan many tracked companies** from a config: `python scripts/fetch_jobs.py scan --portals
     data/<user>/portals.json [--match ...]` → deduped listing across companies (template:
     `templates/portals.example.json`).
   Great for "jobs at company X"; a company may not be on a given ATS. (Structure ported from
   career-ops, MIT — see `ATTRIBUTIONS.md`.)
3. **`usajobs` (keyed, US-federal, freely storable):**
   `python scripts/fetch_jobs.py usajobs "<keyword>" --list --key <KEY> --email <email>` (free key
   at developer.usajobs.gov). Key can live in the user's preferences/env.
4. **`WebSearch` + `WebFetch`** for discovery and for company career pages not on the above.
5. **User paste (always-available fallback).** When automated fetch fails or a posting is behind a
   login, ask the user to paste the text or name company+role. A single real, complete posting
   beats ten half-scraped ones — this is normal, not a failure.

**Ingestion:** `fetch_jobs.py` (scan / `--id`) also appends fetched jobs to the shared market store
`data/_shared/jobs.jsonl`, which powers the index + dashboard (`references/10-market-db.md`).

**Fetching gotchas (still true):** aggregators (Indeed/Glassdoor/startup.jobs) and `jobs.lever.co`
HTML 403 `WebFetch`; `boards.greenhouse.io` 301-redirects to `job-boards.greenhouse.io` and job
IDs go stale — which is exactly why the keyless **JSON APIs** (via `fetch_jobs.py`) and the LinkedIn
**guest** endpoints are preferred over scraping rendered pages. **Search-result blurbs are not the
posting** — never save a paraphrase as if it were the real requirements.

### Save each posting

For each posting the user wants to consider, create `data/targets/<slug>/` (slug =
`company-role`, kebab-case) and write `posting.md`:

```markdown
# <Job title> — <Company>

- source_url: <url>
- employer: <company>
- location: <location / remote>
- date_seen: 2026-07-21
- salary: <if listed, else "not listed">

## Requirements
<verbatim-ish key requirements from the posting>

## Responsibilities
<key responsibilities>

## Full text
<the substantive posting text as fetched>
```

Record the `source_url` and `employer` honestly; we treat postings as reference material for
this user's own search. Don't build a bulk stored corpus of scraped jobs (that's a licensing
question deferred to future work — see `references/00-overview.md`).

## 3. Coach and iterate

Walk the user through what you found:

- Point out patterns across postings for a title — the recurring must-have requirements, the
  common nice-to-haves, typical seniority language, and salary ranges where visible.
- Be honest about apparent fit: "Three of these five want a cert you don't have yet — worth
  getting, or should we aim at the other two?" This previews the gap analysis (stage 6).
- **Ask for feedback and refine.** Drop titles that don't land, add ones they surface, adjust
  seniority. Loop until you have a shortlist of postings the user actually wants to pursue.

## Notes on quality & honesty

- If postings look like **ghost jobs** (evergreen reposts, vague company, no real contact),
  flag it — stage 6 scores legitimacy formally, but call it out when you notice.
- Don't over-promise. Coaching means honest guidance about where they're competitive and where
  they'd be stretching, not cheerleading every option.

**Next:** stage 6 (`references/06-scoring.md`) — score and gap-analyze the shortlist.
