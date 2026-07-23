# Stage 6 — Scoring + gap analysis

**Goal:** for each shortlisted posting, produce (a) a two-axis score that ranks it, (b) a
legitimacy read, and (c) a requirement-by-requirement **gap analysis**. These tell the user
where to spend effort and feed the honest tailoring in stage 7.

Per target folder `data/targets/<slug>/`, read `posting.md`, plus `data/kb/corpus.json` and
`data/goals.md`. Write `scorecard.md` and `gap-analysis.md` using
`templates/job-scorecard.md`.

## The scores (keep them separate — they drive different advice)

A job can be one you can *do* but won't clear the résumé screen for, or one you're a paper-perfect
match for but don't want. Collapsing that into one number hides the real situation. Score four
things 0–10 (desire, screening-risk low/med/high), each with a one-paragraph rationale citing
specific evidence (corpus ids, posting requirements, goals). **Never hide reasoning behind a number.**

### 1. Literal fit (0–10)
How well the corpus supports the posting's **stated** must-haves *today*. Anchor to the gap
analysis: mostly-met = high; several missing must-haves = low. Be honest, not generous. This score
predicts **screening risk** (ATS + recruiter auto-filter), so it matters even when it's unflattering.

### 2. Capability / true-need fit (0–10)
First **decode what the role actually needs to succeed** — the underlying job behind the stated
requirements (often "turn ambiguous problems into actionable, well-engineered, business-usable
insight," dressed up as a specific degree/tool list). Then score demonstrated **capability +
learning-agility evidence** (from `x_cv.narrative` and the corpus) against *that* true need.
This is where a stretch candidate who can grow into the role scores high even when literal fit is low.

- **Honesty guardrails:** every capability claim needs **concrete analogous evidence** (a real
  corpus story) — no "could probably do it." And **"true need" is an inference that can be wrong**:
  sometimes a research-heavy team really does require the credential/DL depth. Label it as an
  inference and note that risk; don't assume the charitable read.

### 3. Desire (0–10)
How well the role matches `goals.md` — ranked work values, energizers, constraints. A hard-constraint
violation (below comp floor, wrong location) caps desire low regardless of appeal; say so explicitly.

### 4. Screening risk (low / med / high)
How likely an ATS/recruiter auto-screens the candidate out before a human weighs capability. Driven
mostly by literal fit on hard-gated must-haves (degree, named tools, years). High risk + high
capability is the key signal for strategy routing below.

## Strategy routing (what the scores tell the user to *do*)

- **Capability ≫ literal, screening risk high** → don't burn effort keyword-optimizing a résumé
  that will get auto-screened. **Bypass the filter:** warm intro / referral, hiring-manager outreach,
  and a **cover narrative** leading with the growth-arc + differentiation (from `x_cv.narrative`).
  Say this plainly — it's often the honest, higher-EV move.
- **Literal and capability both high** → standard tailored application; strong shot.
- **Capability low** → be honest it's a reach on substance, not just screening; suggest the gap-
  closing steps or a better-fit target.
- **Desire low** → note it regardless of fit; don't push a role the user doesn't want.

## Legitimacy / ghost-job check

A quick, honest read so the user doesn't pour effort into a mirage. Flag signs of a
low-quality or non-real posting: evergreen/duplicate reposts, vague or missing company
identity, no salary and no real contact, unrealistic "wear every hat" requirement lists, or
pressure/too-good-to-be-true framing. Rate `legitimacy: solid | mixed | suspect` with a
one-line reason. This is a caution flag, not a hard gate — the user decides.

## Gap analysis (the useful part)

Go through the posting's requirements one by one. For each, classify against the corpus:

- **Met** — a corpus entry clearly supports it. Cite the entry `id`.
- **Partial** — related/transferable experience, but not a direct match. Say what's there and
  what's short.
- **Missing** — nothing in the corpus supports it.

Separate **must-haves** from **nice-to-haves** (read the posting's own emphasis: "required"
vs "preferred", repetition, ordering).

Then summarize:
- **Strengths to lead with** — the strongest Met items; these drive the tailored resume.
- **Gaps that matter** — Missing/Partial must-haves. For each, give **honest, concrete
  advice**: is it closeable quickly (a short course, a cert, a small project to build
  evidence), is it a stepping-stone role away, or is it a genuine stretch? This is real career
  guidance, not just resume input.
- **Do-not-claim list** — anything Missing that the resume must therefore *not* assert. This is
  the honesty boundary handed to stage 7.

## Ranking

Once the shortlist is scored, present a compact ranked view (literal fit, capability fit, desire,
screening risk, legitimacy, one-line gist + recommended strategy) and discuss with the user. The
user can override the ordering — their priorities win.
Typically you'd then tailor resumes (stage 7) for the ones they choose to pursue.

## Persist fit for the dashboard
When you score a target that exists in the market store, append the result to `data/<user>/fit.jsonl`:
`{job_key, literal_fit, capability_fit, desire, screening_risk, corpus_hash, ts}` (`corpus_hash` =
a hash of `corpus.json` so the index can flag stale scores). This feeds the index + at-a-glance
dashboard (`references/10-market-db.md`, `11-dashboard.md`).

**Next:** stage 7 (`references/07-tailoring.md`).
