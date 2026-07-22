# Changelog

All notable changes to corpus-vitae. Versions are the `version` in `SKILL.md` frontmatter.

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
