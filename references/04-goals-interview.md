# Stage 4 — Goals interview

**Goal:** understand what the user wants *next* and *why*, grounded in who they actually are
(the corpus). Output a short, structured `data/goals.md` that stages 5–7 use to aim the search
and to score "desire." This is where we decide the *direction*, before we look at specific jobs.

Read `data/kb/corpus.json` first so your questions are informed — reference their real
experience, don't ask in a vacuum.

## Calibrate to the person (important)

Aim the conversation at trajectories that are *real* for this person from where they are now.
Someone whose history is cashiering is well-served by "shift lead → store manager →
district/ops" or a pivot into an adjacent field — not a cold pitch to be a public-company CEO.
Ambition is great and pivots are absolutely on the table; just keep options **reachable from
the current corpus** (possibly via a stepping-stone or some upskilling, which the gap analysis
in stage 6 will make concrete). Don't flatter, and don't limit — be a realistic, encouraging
coach.

## What to draw out

Cover these, conversationally (one thread at a time), and write the answers to `goals.md`:

1. **Motivation for change** — why now? What's pulling them (growth, pay, meaning, stability,
   people, flexibility) and what's pushing them (burnout, ceiling, layoff, boredom)?
2. **Work values** — what conditions make work good or bad for them. Use the six **O*NET Work
   Values** as prompts (attribution in `ATTRIBUTIONS.md`), in plain language:
   - **Achievement** — using your abilities, seeing results.
   - **Independence** — autonomy, making your own decisions.
   - **Recognition** — advancement, status, being valued.
   - **Relationships** — good colleagues, service to others, no conflict with values.
   - **Support** — supportive management, fair treatment.
   - **Working conditions** — pay, security, variety, comfortable environment.
   Ask them to rank or pick their top two or three; these become desire-scoring weights.
3. **Interests & energy** — which parts of past work energized vs. drained them? (What would
   they do more of / never again?)
4. **Constraints & dealbreakers** — location/remote, compensation floor, hours, travel,
   industries to avoid, timeline. Be concrete; these are hard filters in stage 6.
5. **Appetite for change** — lateral move, step up, or genuine pivot? How much retraining are
   they willing to do, and how fast do they need a role?

## Value thesis + desired role attributes (beats the "title trap")

Before you translate goals into job titles, name **what the user actually sells** — the underlying
function they create value with, independent of any title. This is the single most important output
of this stage for aiming the search, because targeting by literal title (e.g. "data scientist")
*silently* misses the roles they'd be best at: the same work is labeled inconsistently across orgs
("VP of Growth", "Head of Monetization", "Chief of Staff", "Head of Strategic Data Opportunities"),
so a title-filtered search never even surfaces them.

- **Value thesis (one sentence).** Draw it out and write it plainly, e.g. *"I find a revenue lever,
  model it, build it, and own the decision end-to-end."* Ground it in the corpus and `x_cv.narrative`
  (their differentiators, throughline, energizers). Ask the user to confirm/sharpen it — it must be
  *theirs*, not a flattering paraphrase.
- **Desired role attributes (not titles).** Capture what they want as **attributes** a role either has
  or doesn't — e.g. revenue/P&L ownership, autonomy, a 0→1 build mandate, strategic influence,
  cross-functional reach, small-team vs big-org. These become the real target definition; Stage 5
  turns them into a wide set of candidate titles, and Stage 6 scores roles against them (the
  "value-fit read"). A role can have a weird title and still be a perfect attribute match — that's
  exactly the kind of role we don't want to miss.

Note where their energizers/drainers cut against a path (e.g. a step-up-to-VP path may add the
persuasion/meeting load that drains them) — that tension is useful signal for Stage 6, not a
disqualifier.

## Synthesis: overlap + a few paths

Then reflect back a short synthesis, in your own words (do not brand it or reproduce any
proprietary diagram):

- **The overlap** — where their strengths (from the corpus), their interests, their values,
  and market demand seem to line up. Name 2–4 candidate directions.
- **Sketch 2–3 alternative paths** — e.g. a "double-down" path (deepen current track), an
  "adjacent pivot" path (transfer skills sideways), and optionally a "stretch" path (reachable
  with a clear stepping stone). Keep each to a few lines. This gives the user real choices to
  react to rather than a single prescription.

Invite the user to correct the synthesis — it's a draft for them to shape.

## Output: `data/goals.md`

Write a concise, human-readable file (this one is Markdown, not JSON) with sections:

```markdown
# Career goals

## Why change now
- push: ...
- pull: ...

## Top work values (ranked)
1. ...
2. ...
3. ...

## Energizers / drainers
- more of: ...
- less of: ...

## Constraints (hard filters)
- location/remote: ...
- comp floor: ...
- timeline: ...
- avoid: ...

## Appetite for change
- lateral | step-up | pivot; retraining tolerance: ...

## Value thesis
<one sentence: the underlying function the user sells, independent of title>

## Desired role attributes
- must-have: <e.g. revenue/P&L ownership, autonomy, 0→1 build mandate>
- nice-to-have: <e.g. small team, cross-functional reach>
- avoid: <e.g. heavy-consensus / meeting-driven cultures>

## Candidate directions
1. <direction> — why it fits
2. ...

## Alternative paths
- Double-down: ...
- Adjacent pivot: ...
- Stretch (with stepping stone): ...
```

**Next:** stage 5 (`references/05-coaching.md`).
