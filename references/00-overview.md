# 00 — Overview: how corpus-vitae fits together

This is the orientation doc. Read it once to understand the philosophy and the data flow;
then work from the per-stage references (`01`–`07`).

## What this skill is

A guided, conversational pipeline that turns a person's real history into honest, tailored,
per-job resumes. It is deliberately **human-in-the-loop**: the user reviews and owns every
artifact. The skill never acts outward (no applying, sending, or posting).

## The two assets

1. **The corpus** (`data/<user>/kb/corpus.json`) — the durable, reusable knowledge base of
   everything true about the user. Built once (stages 1–3), then reused for every job. This
   is the crown jewel; protect its integrity.
2. **Per-job artifacts** (`data/<user>/targets/<slug>/`) — ephemeral, one folder per job under
   consideration: the saved posting, a scorecard, a gap analysis, and the tailored resume.

> **Per-user namespacing:** one machine can serve several people, so all personal data lives under
> `data/<user>/`. Resolve the active user at session start (see `SKILL.md` → "Multiple users").
> Paths in these docs written as `data/…` mean `data/<active-user>/…`.

## Two interview layers: facts and story

The corpus captures two different kinds of evidence, in two passes:
- **Experience interview (Stage 2 → 3):** the *facts* — what the person did (STAR stories, metrics).
- **Narrative interview (Stage 2.5):** the *story* — growth arc, learning agility, differentiation,
  operating principles, motivation. Stored corpus-level in `x_cv.narrative`, evidence-backed.

The narrative layer is what makes the honest case for **stretch roles** (where someone can grow
into a job they don't literally match), and it's what the two-layer fit analysis (stage 6) and the
cover/portfolio narrative (stage 7) draw on. It's the skill's signature capability — largely absent
from other résumé tools, which stop at facts + tailoring.

## Design principles

- **Machinery public, data private.** Everything in the repo is PII-free and safe to
  open-source. All personal data lives only in `data/<user>/`, which is gitignored. Never write
  personal data anywhere outside the active user's `data/<user>/` directory.
- **Relevant truth, never fabrication.** See the honesty section below — this is the spine
  of the whole tool.
- **The corpus is the single source of truth.** Downstream stages *select from* and
  *reframe* corpus entries; they never introduce facts that aren't in the corpus. If a
  stage needs a fact that isn't there, it goes back and asks the user, then adds it to the
  corpus (with provenance) before using it.
- **Conversation, not wizard.** Stages are a map, not rails. Meet the user where they are.
- **Progressive disclosure.** `SKILL.md` is the map; each stage's playbook lives in its own
  reference file and is read only when that stage runs.

## The honesty philosophy (applies to every stage, enforced at stage 7)

Tailoring is the art of showing the *most relevant true version* of someone. The line:

- **Allowed:** selecting which real experiences to feature, reordering, emphasizing,
  adopting the posting's vocabulary for things the user genuinely did, formalizing casual
  phrasing, quantifying real outcomes, and — at high dial settings — "reasonable rounding"
  (e.g. informal→formal title, generous-but-defensible scope).
- **Forbidden at every dial setting, including 10:** inventing employers, dates, degrees,
  certifications, job titles implying a role never held, or metrics/numbers the user never
  provided.
- **The governing test:** *Could the user defend this claim in a detailed interview without
  dodging, deflecting, or inventing context?* If not, cut or soften it.
- **Traceability:** every generated claim must trace to a corpus entry. The `x_cv`
  `provenance` and `confidence` fields exist so this is checkable. When you want a number
  the user didn't give, **ask; don't invent.**

This protects the user: fabrications surface in reference checks and interviews, and cost
people offers and jobs. Honesty is also the more sustainable strategy.

## Data flow

```
data/inbox/ (old resume)
   │  stage 1: parse
   ▼
data/inbox/_parsed.md ──► stage 2: STAR interview ──► stage 3: write corpus
                                                            │
                                                            ▼
                                                   data/kb/corpus.json  ◄── the hub
                                                     │        │      │
                          stage 4: goals ───────────┘        │      └────────────┐
                          data/goals.md                      │                   │
                             │                               │                   │
                             ▼                               ▼                   ▼
                    stage 5: coaching + web         stage 6: score+gaps   stage 7: tailor
                    data/targets/<slug>/posting.md  scorecard.md          resume.json
                                                    gap-analysis.md       resume.md
```

## Canonical data model

The corpus is a **JSON Resume** document extended with an `x_cv` block. A tailored resume is
a **standard** (extension-stripped) JSON Resume subset rendered to Markdown so any JSON
Resume validator/renderer works on the output. The authoritative spec, field list, and copy
-paste templates live in `templates/corpus.schema.md` — read that before writing to the
corpus (stage 3) or generating a resume (stage 7).

## Job-posting sourcing (v1)

v1 uses **live `WebSearch` → `WebFetch`** only. We do **not** build a stored job corpus.
Save only the specific postings the user is targeting, into `data/targets/<slug>/posting.md`,
recording the source URL and employer. Postings are treated as reference material for one
user's own job search.

## Future-work seams (documented, not built in v1)

Keep these in mind so v1 choices don't paint us into a corner, but do **not** build them now:

- **Structured job APIs — BUILT** (`scripts/fetch_jobs.py` + the Stage-5 provider layer):
  keyless **Greenhouse / Lever / Ashby / SmartRecruiters** and keyed **USAJobs**, plus
  **`linkedin-claude-fetch`** (guest endpoints via WebFetch) as the default — with SimHash
  cross-listing dedup, a scan-history ledger, liveness checks, and a `scan` mode over a portals
  config (structure ported from career-ops, MIT). Still future: paid storable corpora
  (JobDataFeeds/Techmap, Fantastic.jobs) only if bulk data is ever needed.
  - **Do not build a stored corpus on Adzuna / JSearch / Careerjet** — their ToS forbid
    persistence.
- **Skills/occupation taxonomy** for stronger matching: **O*NET** full DB (CC BY 4.0) to
  normalize skills; **SkillNER** (MIT) for offline extraction (heavy spaCy dependency).
- **Additional output formats:** docx (ATS), PDF, HTML — would reuse the `docx`/`pdf` skills.
- **Job tracker** (xlsx) and the entire **apply** phase (submissions, follow-ups, status).

## Attribution & licensing

The repo is MIT and intended to go public. We encode well-known *methods* in our own words
(methods aren't copyrightable) and record every borrowed idea, plus the JSON Resume schema
and O*NET data (CC BY 4.0, attribution required), in `ATTRIBUTIONS.md`. We copy no code or
verbatim text from other projects, and treat AGPL projects (open-resume, resume-lm) as
inspiration only.
