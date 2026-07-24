# 00 — Overview: how corpus-vitae fits together

This is the orientation doc. Read it once to understand the philosophy and the data flow; then work
from the per-stage references (`01`–`12`).

## What this skill is — and what it isn't

A guided, conversational pipeline that turns a person's real history into honest, tailored, per-job
résumés. It is deliberately **human-in-the-loop**: the user reviews and owns every artifact, and the
skill never acts outward on its own — it can *fill* an application form on request (stage 10), but it
never submits, sends, posts, or creates accounts.

**It is not a quick résumé polish.** The core of the tool is an intensive **build** of a durable
corpus — the deep experience + narrative interviews (stages 2–2.5) and the goals work (stage 4) are the
real cost, and they take genuine time. The payoff is **flexibility**: once the corpus exists, producing
an honest, tailored résumé for any job — or pivoting to a whole new direction — is fast and repeatable,
because everything true about the user is already captured and organized. Invest in the interview once;
reap it across the entire search. **Set this expectation with the user early** so they opt in knowingly.

## The assets

1. **The corpus** (`data/<user>/kb/corpus.json`) — the durable, reusable knowledge base of everything
   true about the user (facts *and* story). Built once (stages 1–3, enriched at 2.5 and 4), then reused
   for every job. This is the crown jewel; protect its integrity.
2. **The profile** (`data/<user>/profile.json`) — a small, local-only bio (contact, links, work
   eligibility, comp expectations, optional EEO). Feeds the résumé header and the optional autofill;
   sensitive fields never go on the résumé.
3. **Per-job artifacts** (`data/<user>/targets/<slug>/`) — ephemeral, one folder per job under
   consideration: the saved posting, a scorecard, a gap analysis, the tailored résumé + exports, and
   (optionally) a fill plan.

> **Per-user namespacing:** one machine can serve several people (a household sharing a computer, not
> isolated accounts), so all personal data lives under `data/<user>/`. Confirm who you're talking to at
> session start — see `SKILL.md` → "Multiple users on one machine". Paths written `data/…` mean
> `data/<active-user>/…`. `data/_shared/` is the shared job store, **not** a user.

## Two interview layers: facts and story

- **Experience interview (Stage 2 → 3):** the *facts* — what the person did (STAR stories, metrics).
- **Narrative interview (Stage 2.5):** the *story* — growth arc, learning agility, differentiation,
  operating principles, motivation. Stored corpus-level in `x_cv.narrative`, evidence-backed.

The narrative layer is what makes the honest case for **stretch roles** (where someone can grow into a
job they don't literally match); it feeds the two-layer fit analysis (stage 6) and the cover/portfolio
narrative (stage 7). It's the skill's signature capability — largely absent from other résumé tools,
which stop at facts + tailoring.

## Value-thesis search (stages 4–5)

Targeting by literal job title silently misses the roles a person is actually best at (the same work
wears different labels across orgs). So stage 4 names a one-sentence **value thesis** — what the user
really sells — plus desired role attributes, and stage 5 expands that into a few role **archetypes** and
a wide title search. Titles are search *hints* (recall); the JD body + stage-6 capability fit decide
what to keep (precision). See `04`/`05`/`06`.

## Job sourcing is the hard part — and why

Sourcing live postings is the least reliable stage, and that's a property of the market, not a bug here:

- There is **no free, legal, bulk job-posting API.** The big aggregators (LinkedIn, Indeed, Glassdoor)
  forbid scraping and block automated fetches; company ATS listings go stale and vary per employer.
- The skill sources where it legally and reliably can: **keyless public ATS APIs** (Greenhouse / Lever /
  Ashby / SmartRecruiters), **LinkedIn's public guest endpoints** (`linkedin-claude-fetch`, the
  default), **USAJobs** (keyed), and a logged-in single-page Chrome fetch (`chrome-single`). Results can
  be **uneven or thin** for some searches.
- **The backbone is user-paste.** If a search comes up short, have the user paste a posting (or point at
  one page in their logged-in browser); *everything downstream* — scoring, gaps, tailoring, prep — works
  perfectly on a pasted posting. Treat thin results as a sourcing limitation, not a failure, and lean on
  paste. Details: `05-coaching.md`.

## Job market DB & dashboard (subsystem)

Sourcing appends every fetched job to `data/_shared/jobs.jsonl` (including the company `apply_url`),
company intel to `data/_shared/companies.jsonl`, and each user has `interactions.jsonl`
(like/dislike/status) + `fit.jsonl` (stage-6 scores). `scripts/build_index.py` compiles these into a
**rebuildable** `data/<user>/index.db` (files are canon; SQLite is a derived index), and
`scripts/build_dashboard.py` renders a local `dashboard.html` of best-fits-today. Company intel comes
only from redistribution-clean sources (Wikidata / Wikipedia / BLS); ratings and awards are deep-link
pointers, never scraped. Details: `10-market-db.md`, `11-dashboard.md`.

## Design principles

- **Machinery public, data private.** Everything in the repo is PII-free and safe to open-source. All
  personal data lives only in `data/<user>/`, which is gitignored. Never write personal data outside the
  active user's directory.
- **Relevant truth, never fabrication.** See the honesty section below — this is the spine of the tool.
- **The corpus is the single source of truth.** Downstream stages *select from* and *reframe* corpus
  entries; they never introduce facts that aren't in the corpus. If a stage needs a fact that isn't
  there, go back and ask the user, then add it (with provenance) before using it.
- **Guided by default; flexible when needed.** Lead the user like a wizard — one step at a time, and
  *you* do all the file work (the user never edits JSON). Let a confident user jump around. Stages are a
  map, not rails.
- **Progressive disclosure.** `SKILL.md` is the map; each stage's playbook lives in its own reference
  file and is read only when that stage runs.

## The honesty philosophy (applies to every stage, enforced at stage 7)

Tailoring is the art of showing the *most relevant true version* of someone. The line:

- **Allowed:** selecting which real experiences to feature, reordering, emphasizing, adopting the
  posting's vocabulary for things the user genuinely did, formalizing casual phrasing, quantifying real
  outcomes, and — at high dial settings — "reasonable rounding" (e.g. informal→formal title,
  generous-but-defensible scope).
- **Forbidden at every dial setting, including 10:** inventing employers, dates, degrees,
  certifications, job titles implying a role never held, or metrics/numbers the user never provided.
- **The governing test:** *Could the user defend this claim in a detailed interview without dodging,
  deflecting, or inventing context?* If not, cut or soften it.
- **Traceability:** every generated claim must trace to a corpus entry. The `x_cv` `provenance` and
  `confidence` fields exist so this is checkable. When you want a number the user didn't give,
  **ask; don't invent.**

This protects the user: fabrications surface in reference checks and interviews, and cost people offers
and jobs. Honesty is also the more sustainable strategy.

## Data flow

```
data/<user>/profile.json   ◄── stage 0: local-only bio (contact, links, eligibility, comp)
data/<user>/inbox/ (old résumé — optional; attach / paste / skip)
   │  stage 1: parse
   ▼
_parsed.md ─► stage 2 + 2.5: experience & narrative interview ─► stage 3: write corpus
                                                                        │
                                                                        ▼
                                                      data/<user>/kb/corpus.json  ◄── the hub
                                                         │             │            │
                 stage 4: goals + value thesis ──────────┘             │            │
                 data/<user>/goals.md                                  │            │
                    │                                                  │            │
                    ▼                                                  ▼            ▼
           stage 5: coaching (archetype title search)        stage 6: score+gaps   stage 7: tailor
           data/<user>/targets/<slug>/posting.md              scorecard.md         resume.json/.md
                    │                                          gap-analysis.md        │
                    │                                                                 ▼
                    │                          stage 7.5 callability · 8 export (PDF/DOCX) ·
                    │                          9 phone-screen prep · 10 autofill (opt-in, never submits)
                    └─► fetched jobs also append to data/_shared/jobs.jsonl → index.db → dashboard.html
```

## Canonical data model

The corpus is a **JSON Resume** document extended with an `x_cv` block. A tailored résumé is a
**standard** (extension-stripped) JSON Resume subset rendered to Markdown, so any JSON Resume
validator/renderer works on the output. The authoritative spec, field list, and copy-paste templates
live in `templates/corpus.schema.md` — read that before writing to the corpus (stage 3) or generating a
résumé (stage 7).

## Future-work seams (documented, some now built)

- **Structured job APIs — BUILT** (`scripts/fetch_jobs.py` + the Stage-5 provider layer): keyless
  Greenhouse / Lever / Ashby / SmartRecruiters and keyed USAJobs, plus `linkedin-claude-fetch` (guest
  endpoints) as default, with SimHash dedup, a scan-history ledger, liveness checks, and a `scan` mode.
  Still future: paid storable corpora (JobDataFeeds/Techmap, Fantastic.jobs) only if bulk data is ever
  needed. **Do not** build a stored corpus on Adzuna / JSearch / Careerjet — their ToS forbid persistence.
- **Application autofill — BUILT** as the opt-in Stage 10 (`references/12-autofill.md`): fills one form,
  never submits. Still future: Workday-grade robustness/coverage; **submission, tracking, and follow-ups
  remain deliberately out of scope.**
- **Skills/occupation taxonomy** for stronger matching: **O*NET** full DB (CC BY 4.0) to normalize
  skills; **SkillNER** (MIT) for offline extraction (heavy spaCy dependency).
- **Job tracker** (xlsx).
- **Fit-calibration ladder** (stage 5.5) is currently an experimental stub (`references/05b-calibration.md`).

## Attribution & licensing

The repo is MIT and intended to be public. We encode well-known *methods* in our own words (methods
aren't copyrightable) and record every borrowed idea, plus the JSON Resume schema and O*NET / Wikidata /
Wikipedia / BLS data licenses, in `ATTRIBUTIONS.md`. We copy no code or verbatim text from other
projects, and treat AGPL projects (open-resume, resume-lm) as inspiration only.
