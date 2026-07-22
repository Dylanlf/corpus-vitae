# Attributions

corpus-vitae is MIT-licensed. It encodes several well-known career/resume *methods* in its
own words. Under US copyright law, methods, processes, and facts are not copyrightable — only
their specific expression (exact wording, published worksheets, particular diagrams) is. We
therefore describe these methods in our own words and do **not** reproduce any source's
verbatim text, worksheets, question banks, or trademarked branding. Where a data schema or
dataset is reused, its license and attribution requirement are listed below.

## Methods / frameworks (encoded in our own words)

- **STAR / CAR** behavioral-story structures — generic, widely used; no trademark concern.
  Used as the experience-interview scaffold (`references/02-interview.md`).
- **Competency mapping + the "brag document" practice** — general professional practice
  (the term "brag document" was popularized by Julia Evans, jvns.ca; we use the idea, not her
  text). Shapes interview coverage and the living knowledge base.
- **Google "XYZ" bullet formula** ("accomplished X, as measured by Y, by doing Z") — a short
  method attributed to Laszlo Bock; formulas/methods aren't copyrightable. Used for resume
  bullets (`references/07-tailoring.md`).
- **"Defend-it-in-an-interview" honesty test** — a plainly-stated ethical heuristic, restated
  in our own words. The Stage-7 guardrail.
- **Scoring-rubric & ghost-job/legitimacy-check ideas** — inspired by the MIT-licensed
  `santifer/career-ops` project. We borrow the *idea* of a multi-dimension rubric plus a
  posting-legitimacy check; we wrote our own rubric and copied no code or prompt text.

## Narrative-interview methods (Stage 2.5 — encoded in our own words)

The narrative/story interview is *informed by* established narrative career-counseling methods and
constructs. Methods and constructs are freely usable; we wrote our own questions and copy no
proprietary assessment items or trademarked names.

- **Career Construction Theory / Career Construction Interview & "My Career Story"** — Mark Savickas
  (and Hartung). The narrative career-counseling backbone; the CCI question *structure* is a
  published, reusable method. https://www.marksavickas.com/ · "My Career Story" workbook (free).
- **Working Identity / career "signature story"** — Herminia Ibarra. Concepts (possible selves,
  experiment→learn→narrate) used as ideas; book text not reproduced.
- **Public Narrative ("Story of Self/Us/Now")** — Marshall Ganz. Challenge→choice→outcome→lesson
  structure (worksheets are CC-licensed for non-commercial educational use; we reuse the structure,
  not verbatim text).
- **Hero's Journey** — Joseph Campbell. Public-domain scholarship; the arc used as narrative shape.
- **Learning agility** — Lombardo & Eichinger; De Meuse et al. Cited as an evidence-informed *lens*
  (mental/people/change/results agility + self-awareness), **not** settled science. The Korn Ferry
  viaEDGE / Learning Agility **assessment items are proprietary** and are not used.
- **Off-limits (concept awareness only; no items/marks reproduced):** CliftonStrengths®/
  StrengthsFinder® (Gallup), The 6 Types of Working Genius® (Table Group), StoryBrand®/SB7®
  (Donald Miller). We ask about strengths/energy/story in our own words and never use these marks.

## Concept-only (no verbatim text, no branding, no reproduced diagrams)

These informed our thinking but are trademarked and/or contain copyrighted worksheets. We use
only the underlying, uncopyrightable ideas and never their names as feature names:

- "Designing Your Life" (Burnett & Evans) — the Odyssey-Plan *concept* of sketching alternate
  multi-year paths, in our own words. Not branded as such in the tool.
- "What Color Is Your Parachute?" / the Flower Exercise (Bolles) — the transferable-skills
  inventory concept only.
- Schein's Career Anchors, Holland's Self-Directed Search — typologies referenced as ideas;
  their published questionnaires are not reproduced.
- The four-circle "ikigai" Venn diagram (Marc Winn, 2014) — not reproduced and not presented
  as traditional Japanese philosophy.

## Data schemas & datasets reused

- **JSON Resume schema** — https://jsonresume.org/ — MIT-licensed. Adopted as the canonical
  data format for the corpus and tailored resumes. See `templates/corpus.schema.md`.
- **O*NET** (U.S. Department of Labor / O*NET OnLine) — https://www.onetonline.org/ —
  content licensed **CC BY 4.0**. If/when O*NET Work Values or occupation/skill data are used
  (stage 4 and future matching), attribution is required, e.g.:
  > This product uses O*NET data, which is provided by the U.S. Department of Labor,
  > Employment and Training Administration, and is used under the CC BY 4.0 license.

## Projects reviewed for design inspiration (no code or text reused)

Studied to understand the landscape; nothing was copied. AGPL projects are treated as
inspiration only to avoid copyleft entanglement with this MIT repo.

- `varunr89/resume-tailoring-skill` (MIT), `santifer/career-ops` (MIT),
  `Paramchoudhary/ResumeSkills` (MIT), `srbhr/Resume-Matcher` (Apache-2.0) — permissive;
  reviewed for flow/rubric ideas.
- `xitanggg/open-resume` (AGPL-3.0), `olyaiy/resume-lm` (AGPL-3.0) — inspiration only.
