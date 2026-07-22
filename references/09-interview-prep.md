# Stage 9 — Phone-screen prep (likely questions + honest best answers)

**Goal:** prepare the user for the phone screen(s) for a specific target — the likely questions and
strong, *honest*, corpus-grounded answers, including the tough ones they'll actually get. Output
`data/<user>/targets/<slug>/interview-prep.md`. Run after tailoring + callability, once the user
decides to pursue.

This stage is where the honesty engine pays off twice: (1) it uses the **"defend-it-in-an-interview"**
test literally — every résumé claim becomes a "walk me through that" drill; (2) the **gap analysis**
becomes the list of tough questions to rehearse *honestly* rather than bluff.

## Phone-screen reality
Most first-round screens are one or both of:
- **Recruiter screen** (~20–30 min): fit, motivation, logistics, comp, red-flag probing, "walk me
  through your background," "why this role/company." Not deeply technical.
- **Hiring-manager screen** (~30–45 min): role-specific depth, behavioral (STAR), "tell me about a
  time…", plus the same motivation/level questions.
Prep for both; label which is which.

## Derive likely questions from FOUR sources (this is the method)
1. **The JD** (`posting.md`) → "Tell me about your experience with <required/responsibility>."
   Prioritize the must-haves and the headline responsibilities.
2. **The gap analysis** (`gap-analysis.md`) → the **tough questions**. Every gap and do-not-claim
   item is something a good interviewer probes: missing credential, a level mismatch, a
   nice-to-have they lack. Rehearse an **honest** answer for each (see below).
3. **The résumé** (`resume.md`) → **defend-the-claim drills**: for every quantified or strong claim,
   "how did you get that number / what exactly did you do?" If the user can't defend it cleanly, the
   claim was too aggressive — fix the résumé, don't coach a dodge.
4. **Narrative + goals** (`x_cv.narrative`, `goals.md`) → behavioral/motivation: "why leave," "why
   us," growth-arc and failure stories, "what are you looking for."

## Writing honest best answers
- **Ground every answer in a real corpus entry/story** — cite the id. Prefer **STAR** for
  behavioral answers (pull from `x_cv.stories`).
- **Tough/gap questions get honest framing, never a bluff.** Formula: *acknowledge briefly →
  reframe to the true adjacent strength (with evidence) → show trajectory/eagerness.* E.g. for "have
  you managed a data-science team?" when they've tech-led + mentored: own the honest scope, cite the
  people they hired/trained, and express readiness to grow — do not claim a team they didn't run.
- **Defend-the-claim answers** must match what's actually in the corpus, including caveats (an
  *estimate* is presented as an estimate; a threshold-dependent metric names the threshold).
- **Level/over-qualified question** (if flagged): coach an honest "why this level" narrative from
  `goals.md`, not a story that hides the mismatch.
- Keep answers tight (screens are fast): a 20–40 second spoken answer, not an essay.

## Also prepare
- **Questions to ask them** — 4–6, tuned to the user's `energizers_drainers` and open fit questions
  (team, autonomy, how decisions get made, tooling/AI culture, what success looks like, why the role
  is open). Good questions double as fit-checks for the user.
- **Comp handling** — how to field "what are your expectations": anchor on the posting's published
  band if any, defer specifics politely early, don't low-anchor. Give framing and phrasing only;
  **do not give personalized financial/salary-negotiation advice or specific numbers** — that's the
  user's call (and out of this tool's lane).
- **Logistics** — location/remote, start timeline, work authorization if relevant.

## Honesty guardrails
- Never script a claim the user can't truthfully defend. If prep surfaces one, that's a signal to
  fix the résumé/corpus, not to rehearse a spin.
- Prep is practice for telling *their* true story well — confidence and framing, not fabrication.

## Aim for broad coverage (so the screen doesn't surprise the user)
Don't stop at a handful. Cover every category below (a real prep set is ~25–40 questions):
- **Recruiter:** background walk-through, why-leave, why-this-company/role, comp, logistics.
- **Role depth (from JD):** each must-have + headline responsibility; architecture/prioritization
  judgment; how they communicate results.
- **Management & leadership** (whenever the role manages people): team structure/growth, coaching,
  underperformance, IC-vs-manager balance, influencing up.
- **Tough / gap:** one per real gap and per do-not-claim item, plus any level/over-qualified probe.
- **Defend-your-claims:** one per quantified/strong résumé claim.
- **Behavioral (STAR):** leadership, teamwork, conflict/communication, failure, ambiguity.
- **Company-specific:** their product/domain, a "what metric would you look at first," and any
  domain intersections the JD names (e.g. trust & safety).
- **Curveballs:** strengths/weakness, "not on your résumé," "why you over X," "what would your
  manager/CEO say."
Flag (⛳) any answer that needs a real specific only the user can supply, rather than inventing one.

## Output: `interview-prep.md`
Use `templates/interview-prep.md`. Mark each Q with its source (JD / gap / claim / behavioral) and
each answer with the backing corpus id.

**This is the last prep stage.** Applying, scheduling, and attending remain the user's — out of scope.
