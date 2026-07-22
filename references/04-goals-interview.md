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

## Candidate directions
1. <direction> — why it fits
2. ...

## Alternative paths
- Double-down: ...
- Adjacent pivot: ...
- Stretch (with stepping stone): ...
```

**Next:** stage 5 (`references/05-coaching.md`).
