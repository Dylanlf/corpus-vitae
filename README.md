# corpus-vitae

A Claude skill that turns your real career history into honest, tailored, per-job résumés —
end to end, short of actually submitting.

*The name plays on **curriculum vitae**: **corpus** is both the NLP term for a body of
training text and the Latin for "body" — here, your **body of work**.*

## What this is (and what it isn't)

**This is not a five-minute résumé polish.** It's an intensive, guided **build** of a durable
*corpus* — a complete, evidence-backed record of your body of work: every role, project, and skill
(the facts), plus the growth-arc and differentiation behind them (the story). That deep interview is
the up-front cost, and it's real — expect a genuine conversation, not a form to fill.

**The payoff is flexibility.** Once the corpus exists, it's reused: generating an honest, tailored
résumé for any specific job — or pivoting to a whole new direction — becomes fast, because the hard
part (knowing and organizing everything true about you) is already done. The corpus is the asset; each
résumé is a cheap, disposable projection of it. The more you invest in the interview, the more the tool
pays back over an entire search.

> **Status: a spare-time project and a work in progress.** Built and tested by one person on their
> own history; expect rough edges and breaking changes. Some stages are experimental (e.g. the
> fit-calibration ladder), and every output needs your review. Not affiliated with or endorsed by any
> employer or by Anthropic. Use it as a helpful assistant, not an authority — you own every claim it
> helps you make.

## Why finding the jobs is the hard part (read this first)

The weakest, least reliable part of the pipeline is **sourcing live job postings** — and that's the
job market's design, not an oversight here:

- There is **no free, legal, bulk job-posting API.** The big aggregators (LinkedIn, Indeed, Glassdoor)
  forbid scraping and block automated fetches; company ATS listings (Greenhouse, Lever, …) go stale and
  vary per employer.
- So the skill sources where it legally and reliably can — **keyless public ATS APIs**, **LinkedIn's
  public guest endpoints**, and **USAJobs** — and its results can be **uneven or thin** for some
  searches (a title search may drift or return little).

**The always-reliable fallback is you pasting a posting.** If a search comes up short, paste the job
description (or point Claude at one page in your logged-in browser) and *everything downstream* —
scoring, gap analysis, tailoring, interview prep — works perfectly. Thin search results mean the
sourcing layer struggled, **not** that the tool is broken. Treat search as a convenience and paste as
the backbone.

## Guiding principle: relevant truth, never fabrication

Every claim must be true and defensible in a detailed interview. The honesty dial controls how
aggressively we *frame* real experience — never whether we tell the truth. Even at its most aggressive
setting, the skill never invents employers, dates, degrees, certifications, or metrics.

## The pipeline

A guided, wizard-by-default flow (Claude does all the file work — you just talk to it). Stages usually
run in order but you can jump around.

| # | Stage | What happens |
|---|-------|--------------|
| 0 | **Profile / bio** | Capture a local-only bio (contact, links, work eligibility, comp expectations) — feeds the résumé header and optional autofill. |
| 1 | **Intake** | Bring **any** career materials — résumé, cover letters, reviews, brag docs, certs, project write-ups, LinkedIn export — however's easiest (attach / paste / point to it), or skip if you have none. |
| 2 | **Experience interview** | Elicit the untold detail — STAR stories, real numbers, competency coverage. *(The deep part.)* |
| 2.5 | **Narrative interview** | The *story* layer: growth arc, learning agility, differentiation, operating principles. |
| 3 | **Knowledge base** | Build `corpus.json` — your durable, reusable facts & stories. |
| 4 | **Goals + value thesis** | What you want next and why; name the *value* you sell (not just a title). |
| 5 | **Coaching** | Turn the value thesis into role **archetypes** + a wide title search over real postings. |
| 6 | **Scoring + gaps** | Two-layer fit (literal vs. capability/true-need) + screening risk + requirement-by-requirement gaps. |
| 7 | **Tailoring** | A per-job résumé, governed by a 0–10 honesty/tailoring dial. |
| 7.5 | **Callability review** | Score the résumé's chance of passing the ATS + recruiter screen; flag red flags. |
| 8 | **Format / export** | An ATS-safe, text-layer **PDF** + **DOCX** (`scripts/render_resume.py`). |
| 9 | **Phone-screen prep** | Likely questions + honest, corpus-grounded answers. |
| 10 | **Application autofill** *(optional, opt-in)* | Fill one application form from your bio + résumé, then **stop for you to review and submit** — never submits for you. |

Plus a **job market DB + at-a-glance dashboard**: fetched jobs and company intel (Wikidata/BLS) land in
a local store; a generated `dashboard.html` ranks best-fits-today with salary, sector, and repost/ghost
signals (ratings/awards are deep links, never scraped).

**Submitting** applications, creating accounts, and contacting anyone remain **out of scope** — the
skill fills and hands off; you apply (see [references/00-overview.md](references/00-overview.md)).

## Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill entry point — the map of the stages and where to start. |
| `references/` | One playbook per stage (`00`–`12`); read the relevant one before running a stage. |
| `templates/` | Schema (`corpus.schema.md`) + example config/output templates (profile, preferences, title-search, scorecards). |
| `scripts/` | `setup.py` (one-shot renderer bootstrap) · `fetch_jobs.py` (sourcing) · `expand_titles.py` (title search) · `fetch_company_intel.py` (Wikidata/BLS) · `prescore.py` (heuristic fit) · `build_index.py` (JSONL→SQLite) · `build_dashboard.py` (HTML) · `render_resume.py` (PDF/DOCX) · `fill_plan.py` (autofill preview) · `requirements.txt`. |
| `data/<user>/` | **Your** personal inputs and outputs (per-user; supports several people on one machine) — **gitignored, never committed.** |
| `ATTRIBUTIONS.md` | Borrowed methods, the JSON Resume schema, O*NET (CC BY 4.0), and data-source licenses. |

## Design principle

The **machinery is public; your data is private.** Everything needed to run the skill lives in the repo
with zero PII. Personal inputs and generated résumés live only in local `data/<user>/`, which is
gitignored — so this repo can go public without leaking anyone's résumé.

## Data format

The corpus is a [JSON Resume](https://jsonresume.org/) document plus a documented `x_cv` extension
(STAR stories, provenance, confidence, competency tags, and the narrative layer). Tailored résumés are
standard JSON Resume, rendered to Markdown and exported to an ATS-safe, text-layer **PDF** + **DOCX** —
so they validate/render with the JSON Resume ecosystem and submit cleanly. Full spec:
[templates/corpus.schema.md](templates/corpus.schema.md).
