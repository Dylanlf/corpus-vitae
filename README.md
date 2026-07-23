# corpus-vitae

A Claude skill for going from an old resume to honest, tailored, per-job applications —
end to end (short of actually applying).

*The name plays on **curriculum vitae**: **corpus** is both the NLP term for a body of
training text and the Latin for "body" — here, your **body of work**.*

> **Status: a spare-time project and a work in progress.** Built and tested by one person on
> their own history; expect rough edges and breaking changes. Some stages are experimental
> stubs (e.g. the fit-calibration ladder), live job-sourcing is best-effort, and outputs always
> need your review. Not affiliated with or endorsed by any employer or by Anthropic. Use it as a
> helpful assistant, not an authority — you own every claim it helps you make.

## Idea

Turn your real history into honest, tailored job-application materials. The skill runs a
guided, conversational pipeline and keeps a durable knowledge base ("corpus") of everything
true about you, then reuses it to produce a "perfect but honest" resume for each job.

## Pipeline (7 stages)

1. **Intake** — read an old resume you drop in `data/inbox/`.
2. **Experience interview** — elicit the untold detail (STAR + competency coverage).
3. **Knowledge base** — build `data/kb/corpus.json`, your reusable facts & stories.
4. **Goals interview** — what you want next and why, calibrated to your level.
5. **Coaching** — best-fit titles/directions, grounded in real job postings.
6. **Scoring + gaps** — score each target on fit × desire; requirement-by-requirement gaps.
7. **Tailoring** — a per-job resume, governed by a 0–10 honesty/tailoring dial.
7.5. **Callability review** — score the résumé's chance of passing the ATS + recruiter screen; flag red flags.
8. **Format / export** — an ATS-safe, text-layer **PDF** and **DOCX** (`scripts/render_resume.py`).
9. **Phone-screen prep** — likely questions + honest, corpus-grounded answers.

Plus a **job market DB + at-a-glance dashboard**: fetched jobs and company intel (Wikidata/BLS) land in
a local store; a generated `dashboard.html` ranks best-fits-today with salary, sector, and repost/ghost
signals (ratings/awards are deep links, never scraped).

Applying to jobs is **out of scope** (see future work in
[references/00-overview.md](references/00-overview.md)).

## Guiding principle: relevant truth, never fabrication

Every claim must be true and defensible in a detailed interview. The honesty dial controls
how aggressively we *frame* real experience — never whether we tell the truth. Even at its
most aggressive setting, the skill never invents employers, dates, degrees, certifications,
or metrics.

## Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill entry point — the map of the 7 stages and where to start. |
| `references/` | One playbook per stage (`00`–`07`); read the relevant one before running a stage. |
| `templates/` | Schema (`corpus.schema.md`) and output templates. |
| `scripts/` | `fetch_jobs.py` (job sourcing) · `fetch_company_intel.py` (Wikidata/BLS intel) · `build_index.py` (JSONL→SQLite) · `build_dashboard.py` (HTML) · `render_resume.py` (PDF/DOCX) · `requirements.txt`. |
| `data/<user>/` | **Your** personal inputs and outputs (per-user; supports multiple people on one machine) — **gitignored, never committed.** |
| `ATTRIBUTIONS.md` | Borrowed methods, the JSON Resume schema, and O*NET (CC BY 4.0). |

## Design principle

The **machinery is public; your data is private.** Everything needed to run the skill lives
in the repo with zero PII. Personal inputs and generated resumes live only in local `data/`,
which is gitignored — so this repo can go public without leaking anyone's resume.

## Data format

The knowledge base is a [JSON Resume](https://jsonresume.org/) document plus a documented
`x_cv` extension (STAR stories, provenance, confidence, competency tags). Tailored resumes
are standard JSON Resume, rendered to Markdown and exported to an ATS-safe, text-layer **PDF** and
**DOCX** (`scripts/render_resume.py`) — so they validate/render with the JSON Resume ecosystem and
submit cleanly. Full spec: [templates/corpus.schema.md](templates/corpus.schema.md).
