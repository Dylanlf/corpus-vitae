# PLANNING — decisions & what's still open

The core design questions have been answered and promoted into the skill itself. The
authoritative design now lives in [`SKILL.md`](SKILL.md) and
[`references/00-overview.md`](references/00-overview.md). This file records the decisions and
the questions that remain genuinely open (i.e. future work).

## Decisions made (v1)

- **Purpose:** a guided pipeline from raw history → honest, tailored, per-job resumes. Stops
  short of applying.
- **Shape:** one skill, 7 stages (intake → experience interview → knowledge base → goals
  interview → coaching → scoring/gaps → tailoring), run as a conversation, not a rigid wizard.
- **Data model:** [JSON Resume](https://jsonresume.org/) + a documented `x_cv` extension;
  spec in [`templates/corpus.schema.md`](templates/corpus.schema.md).
- **Storage:** all personal data local and gitignored under `data/`; machinery is PII-free.
- **Job postings (v1):** live `WebSearch`/`WebFetch`; no stored corpus.
- **Output:** Markdown resumes (standard JSON Resume underneath).
- **Honesty:** relevant truth, never fabrication; a 0–10 tailoring dial that governs framing
  intensity, never truthfulness. Details in `references/00-overview.md` and `07-tailoring.md`.
- **Licensing:** MIT; borrowed methods encoded in our own words and recorded in
  [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md).

## Still open / future work

- **The "apply" phase** — submissions, tracking, follow-ups. Deliberately out of scope for v1.
- ~~**Structured job APIs** — USAJobs, Greenhouse/Lever/Ashby public JSON~~ **DONE**
  (`scripts/fetch_jobs.py` + Stage-5 provider layer, default `linkedin-claude-fetch`); paid
  storable corpora still open if bulk data is ever needed.
- **Skills taxonomy** — O*NET (CC BY 4.0) / SkillNER for stronger matching.
- ~~**More output formats** — docx, PDF~~ **DONE** (Stage 8 via `scripts/render_resume.py`); HTML still open.
- **Distribution** — if published for others: contribution model and how users supply their
  own `data/`. Keep "Claude" out of any public product name.
