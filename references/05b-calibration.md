# Stage 5.5 — Fit calibration ladder (EXPERIMENTAL — documented stub)

> **Status: experimental stub.** The workflow below is designed but not yet a polished,
> reliable step, because it depends on job sourcing (Stage 5), which is currently the weakest
> link (aggregators 403, postings go stale — see `references/05-coaching.md`). Run it manually /
> with user-pasted postings for now. A real implementation waits on the job-API adapters noted in
> `references/00-overview.md`.

## Why this exists

The first end-to-end run showed two problems the single fit score hid:
1. Users don't have a calibrated sense of what a "good fit" job even looks like for them.
2. A role that scores low on *literal* fit can be a strong *capability* fit — and the user often
   knows this ("I could actually do that") before the tool does.

The calibration ladder fixes both: it shows the user a **spread** of jobs at different fit levels
and learns from their reactions, and it makes the corpus better via a **rescore loop**.

## The ladder

1. **Pick a target direction** (from `data/goals.md`).
2. **Assemble ~4 postings across fit bands** — roughly a **3, 5, 7, and 9** on *capability* fit
   (from clearly-a-reach to clearly-in-range). Source via Stage 5 (WebSearch/WebFetch) where it
   works, otherwise **ask the user to paste** representative postings. Save each under
   `data/targets/<slug>/posting.md`.
3. **Score each** with the Stage 6 two-layer model (literal, capability, desire, screening risk).
4. **Show the spread and ask for reactions.** The point is disagreement: "Here's a 3, a 5, a 7, a
   9 — do these match your gut? Where am I miscalibrated?"

## The rescore loop (the payoff for the narrative interview)

When the user pushes back — *"this '4' is actually a decent fit, I've done X"* — that's signal, not
noise:
- Capture the new evidence: add the missing story to the corpus (Stage 3) and/or extend
  `x_cv.narrative` (Stage 2.5) with the growth-arc / differentiation / learning-agility that
  supports it — **evidence-backed**, per the honesty rules.
- **Rescore** the posting with the enriched corpus. Capability fit should move *because the
  evidence moved*, not because we relaxed honesty.
- Repeat until the user's gut and the scores agree. The result is a better-calibrated user **and**
  a richer corpus — both compounding across every future job.

## Honesty guardrail

Rescoring must reflect **new evidence**, never wishful thinking. If the user "could do it" but has
no analogous story, that's a genuine gap (capability stays modest, with a note on what would close
it) — not a score to inflate. Literal fit and screening risk are unaffected by story detail; only
capability fit can move, and only on real evidence.

## Output

No new file type; the ladder reuses `data/targets/<slug>/` scorecards. Optionally note calibration
takeaways (what the user considers a real fit) back into `data/goals.md`.

**Next:** normal Stage 6/7 on whichever calibrated targets the user chooses to pursue.
