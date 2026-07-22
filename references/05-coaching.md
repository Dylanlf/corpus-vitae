# Stage 5 — Coaching (titles, directions, and real postings)

**Goal:** turn the directions from stage 4 into concrete **job titles** and a shortlist of
**real job postings** to aim at — coaching the user with actual market examples and iterating
on their feedback. Output is one folder per target job under `data/targets/<slug>/` containing
the saved `posting.md`.

Read `data/kb/corpus.json` and `data/goals.md` first.

## 1. Propose titles and directions

From the corpus (what they can do) and goals (what they want), propose a spread of **specific
job titles** — not vague fields. For each, give a one-line "why this fits you" grounded in
real corpus entries, and note the type of move (lateral / step-up / pivot).

- Include the **obvious** titles for their background, a few **adjacent** ones they may not
  have considered (transferable-skills plays), and clearly label any **stretch** titles.
- Titles vary by company/industry for the same work — offer the common synonyms (e.g.
  "Operations Coordinator" ≈ "Ops Associate" ≈ "Program Coordinator") so searches are broad.
- Present the set and **ask the user which resonate** before you go fetch postings. Don't
  boil the ocean; converge on ~3–6 title/direction bets with them.

## 2. Source real postings from the web

For the agreed titles, find **real, current-or-recent** postings (the user asked for real,
possibly older, examples — recency isn't required, representativeness is).

- Use **`WebSearch`** to find listings (try title + location/remote + seniority; try a few
  synonyms). Then **`WebFetch`** the promising ones to pull the actual posting text.
- Prefer postings that are representative of the target, not outliers. A handful of good ones
  per direction beats a giant pile.
- Respect the user's constraints from `goals.md` (location/remote, comp, industries to avoid)
  when choosing what to surface.

### Fetching reality (learned the hard way — follow this order)

Full-posting fetching is unreliable; plan for it instead of fighting it:

- **Aggregators block bots.** Indeed, Glassdoor, LinkedIn, startup.jobs, and **Lever**
  (`jobs.lever.co`) typically return **403** to `WebFetch`. Don't rely on them for full text.
- **Greenhouse is the most fetchable**, but: the `boards.greenhouse.io` host **301-redirects**
  to `job-boards.greenhouse.io` (follow it), individual job IDs **go stale/404** or resolve to
  the board **index** (only titles/locations, no body). Best bet is the **public JSON API**
  (no key): `https://boards-api.greenhouse.io/v1/boards/{company}/jobs/{id}` — try this before
  scraping HTML. (Future work: proper adapters for Greenhouse/Lever/Ashby JSON and USAJobs — see
  `references/00-overview.md`.)
- **Search-result blurbs are not the posting.** They're the search engine's paraphrase; never
  save them into a target as if they were the real requirements.
- **The reliable fallback is the user.** When fetching fails (it often will), just **ask the
  user to paste the posting text**, or to name a company + role so you can try that company's
  careers page/ATS directly. This is normal, not a failure — most users have specific targets in
  mind. A single real, complete, user-provided posting beats ten half-scraped ones.

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
