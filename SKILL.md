---
name: corpus-vitae
description: >-
  Turn a person's real work history into honest, tailored, per-job resumes. Runs a
  guided pipeline: read an old resume, interview the user to elicit facts & stories,
  build a reusable knowledge base (a JSON Resume "corpus"), interview about career
  goals, coach on job titles/directions using real job postings, score and gap-analyze
  target jobs, then generate a "perfect but honest" tailored resume per job with a 0–10
  tailoring dial. Use this whenever the user wants to build a resume, tailor a resume to
  a specific job, figure out what jobs to apply for, capture their career history, prep
  for a career change, or turn accomplishments into resume material — even if they don't
  say the word "resume." Does NOT apply to jobs on the user's behalf (out of scope).
version: 1.8.0
---

# corpus-vitae

Take someone from raw career history to honest, tailored, per-job resumes. The engine is
public and carries zero personal data; everything about a specific user lives only in the
gitignored `data/` directory.

> **Status: spare-time project, work in progress.** Some stages are experimental, outputs need
> the user's review, and it's not affiliated with any employer or Anthropic. Be a helpful
> assistant, not an authority — the user owns every claim.

## Core principle: relevant truth, never fabrication

Every claim this skill produces must be **true and defensible in a detailed interview**.
Tailoring means *selecting, emphasizing, and reframing* real experience for a specific job
— never inventing employers, titles, dates, degrees, certifications, or metrics. The
honesty dial (stage 7) controls how aggressively we frame, never whether we tell the truth.
When you're tempted to add a number or claim the user didn't give you, **ask them — don't
invent it.**

## The pipeline (7 stages)

The stages usually run in order, but this is a **conversation, not a rigid wizard** — the
user can jump in anywhere, skip, repeat, or come back later. Always tell the user which
stage you're in and what the next one is. The knowledge base (stage 3) is the durable
center everything else reads from and writes to.

Two cross-cutting rules:
- **The corpus is comprehensive.** Capture the user's *entire* history at full depth —
  every role, project, skill, credential — regardless of the job they're currently targeting.
  Relevance-weighting happens only at tailoring (stage 7); a finance role that's a footnote on
  a data-science resume is still captured in full, because the next target might be finance.
- **Career direction is handled explicitly:** a quick read at intake (stage 1) to orient
  where to probe, then the full "what do you want next and why" conversation at stage 4 — not
  as an ad-hoc aside.

Paths below use `data/<user>/…`; see **Multiple users** below for how the active user is resolved.

| # | Stage | Reads | Writes | Reference |
|---|-------|-------|--------|-----------|
| 1 | Intake | `data/<user>/inbox/*` | `data/<user>/inbox/_parsed.md` | `references/01-intake.md` |
| 2 | Experience interview | parsed resume + user | (feeds stage 3) | `references/02-interview.md` |
| 2.5 | Narrative interview | corpus + user | `x_cv.narrative` | `references/02b-narrative-interview.md` |
| 3 | Knowledge base | interview | `data/<user>/kb/corpus.json` | `references/03-knowledge-base.md` |
| 4 | Goals interview | corpus + user | `data/<user>/goals.md` | `references/04-goals-interview.md` |
| 5 | Coaching | corpus + goals + web | `data/<user>/targets/<slug>/posting.md` | `references/05-coaching.md` |
| 5.5 | Fit calibration *(experimental)* | corpus + goals + postings | (rescore loop) | `references/05b-calibration.md` |
| 6 | Scoring + gaps | corpus + goals + posting | `.../scorecard.md`, `.../gap-analysis.md` | `references/06-scoring.md` |
| 7 | Tailoring | corpus + posting + gaps | `.../resume.json`, `.../resume.md` | `references/07-tailoring.md` |
| 7.5 | Callability review | résumé + posting | `.../callability.md` | `references/07b-callability-review.md` |
| 8 | Format / export | `.../resume.json`/`.md` | `.../<Name>-Resume.pdf`/`.docx` | `references/08-formatting.md` |
| 9 | Phone-screen prep | résumé + posting + gaps + narrative | `.../interview-prep.md` | `references/09-interview-prep.md` |
| — | Job market DB *(subsystem)* | jobs + company intel + interactions | `data/_shared/*.jsonl`, `data/<user>/index.db` | `references/10-market-db.md` |
| — | At-a-glance dashboard *(subsystem)* | `index.db` | `data/<user>/dashboard.html` | `references/11-dashboard.md` |

**Stage 2.5 (Narrative interview)** is the skill's signature layer: it captures *disposition and
trajectory* (growth arc, learning agility, differentiation, operating principles) — the evidence
that someone can grow into a stretch role. Facts live in stages 2–3; the *story* lives here.

**Value-thesis search (stages 4–5)** beats the "title trap": stage 4 names *what the user sells* (a
one-sentence value thesis + desired role attributes, not a title), and stage 5 expands that into 3–5
role **archetypes** and a wide set of candidate titles (`scripts/expand_titles.py` →
`data/<user>/title-search.json`) so the search surfaces great-fit roles with unconventional titles
("Head of Monetization", "Chief of Staff") instead of filtering on "data scientist." Titles are
search *hints*; the stage-6 capability/value-fit read decides what to keep.

**Read the stage's reference file before running that stage.** Each reference is the
detailed playbook for its stage; this file is only the map.

## Multiple users (per-user data)

One machine can serve several people. All personal data is namespaced under **`data/<user>/`**
(e.g. `data/dylan/kb/corpus.json`). **Resolve the active user at the start of every session,
before touching any `data/…` path:**

- If exactly one directory exists under `data/`, use it.
- If several exist, **ask which user** this session is for.
- If none exist, ask the user's name/handle and create `data/<user>/` (kebab-case).

Throughout this file and the reference docs, a path written `data/…` means
`data/<active-user>/…`. Never read or write another user's directory in the same session, and
never mix two people's data in one corpus.

## Where to start

- **First time / "help me with my resume" / "what jobs should I go for":** resolve the active
  user (above), then start at stage 1. If `data/<user>/inbox/` is empty, ask them to drop an old
  resume there (any of pdf, docx, txt, md). If they have no resume, skip to stage 2 and build the
  corpus purely from the interview.
- **Corpus already exists (`data/<user>/kb/corpus.json`):** skip intake/interview unless the user
  wants to add more; go to whichever stage they need (often 5–7).
- **"Tailor my resume to this job":** if a corpus exists, go to stage 5/6/7 with that
  posting; if not, you need at least a minimal corpus first (stages 1–3).

Confirm the starting point with the user rather than assuming.

## Data model in one line

The knowledge base is a **[JSON Resume](https://jsonresume.org/) document** (standard
sections) plus a documented **`x_cv` extension** holding the richer facts-&-stories
metadata (STAR structure, provenance, confidence, competency tags). A tailored resume is a
**standard** JSON Resume subset derived from it, rendered to Markdown. Full spec and
templates in `templates/corpus.schema.md`. See `references/00-overview.md` for the design
rationale, honesty philosophy, and future-work seams.

## Reused capabilities (don't reimplement)

- **`pdf` / `docx` skills** — read resumes at intake (stage 1).
- **`WebSearch` / `WebFetch`** — source real job postings (stage 5).
- Borrowed *methods* (encoded in our own words; see `ATTRIBUTIONS.md`): STAR interview
  scaffold, competency map, the Google "XYZ" bullet formula, and the
  "defend-it-in-an-interview" honesty test.

## User preferences (`data/<user>/preferences.json`)

Each user has a preferences file holding their **defaults**. **Load it at session start** (right
after resolving the active user); if absent, create it from `templates/preferences.example.json`.
Any explicit per-run instruction from the user overrides these. Fields:

- `honesty_dial` (default **6**) — Stage-7 tailoring intensity (framing only, never fabrication).
- `build_credit` (default **true**) — include the neutral "Drafted with corpus-vitae" footer.
- `show_dial` (default **false**) — keep the dial number internal (`resume.json` `meta`), never printed.
- `ai_narrative` (default **false**, opt-in) — the corpus-vitae "I build with AI" project/cover element.
- `audience` (default **traditional**; or `ai-forward`) — gates how prominently `ai_narrative` shows.
- `job_source` (default **`linkedin-claude-fetch`**) — Stage-5 default source: `linkedin-claude-fetch`
  | `chrome-single` (logged-in Chrome, one page) | `greenhouse`/`lever`/`ashby`/`smartrecruiters` |
  `usajobs` | `paste` (see `05-coaching.md`).
- `output_formats` (default **md, pdf, docx**) — Stage-8 formats to generate.
- `usajobs` — optional free API key + email for the USAJobs source.

## Out of scope for v1

Applying to jobs, submitting forms, contacting anyone, or tracking applications. The skill
hands the finished resume to the user and stops. Other formats (docx/PDF/HTML), a job
tracker, and structured job-board APIs are noted as future work in `references/00-overview.md`.
