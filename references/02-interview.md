# Stage 2 — Experience interview

**Goal:** surface the *real, specific, untold* detail behind the user's history — the stuff
that never makes it onto a resume — and capture it as structured stories. The parsed resume
(`data/inbox/_parsed.md`) is only a scaffold; a resume is a lossy summary, and the gold is in
what got compressed out.

This stage feeds stage 3 directly. In practice you interweave them: as you get a good story,
write it to the corpus (stage 3), then continue. Don't batch everything to the end — you'll
lose detail and the user will tire.

## How to run it

**Conversational, one theme at a time.** Walk role by role (most recent first is usually
easiest), then cover projects, education, and anything off-resume (side projects, volunteering,
informal leadership). Keep it human — this is an interview, not a form. Ask **one focused
question at a time** and follow the energy; if a thread is rich, stay on it.

**Calibrate to the person.** Match your language and expectations to their level and field. A
line cook, a nurse, and a staff engineer have very different "wins" — don't impose corporate
framing on someone it doesn't fit.

## Be exhaustive — capture everything, regardless of target

This interview should be **incredibly detailed**. The corpus is a *complete, neutral* record of
the person's whole working life — every role, project, skill, and credential, at full depth —
**independent of what job they're currently aiming at.** Do not skip or skim someone's finance
past, their side projects, or older work just because today's target looks like data science.
Relevance-weighting happens *only* at tailoring (stage 7), where irrelevant material simply
isn't selected; a finance role that's a footnote for a DS resume is still captured in full here,
because next month's target might be finance. When in doubt, capture it.

Two things resumes systematically miss — ask about them explicitly:
- **What's new since the resume was last updated** — skills learned, tools picked up, and
  projects shipped that never made it onto paper. Stale resumes are the norm; mine the gap.
- **The projects behind the bullets** — one resume line often hides three real stories.

## Pace it, and keep the user in control

A thorough interview is long by design, which risks fatigue. Manage it openly:

- **Let the user set depth per topic.** Offer, e.g., "Want to deep-dive this one or give me the
  quick version?" Some threads deserve 20 minutes; others, two.
- **Check in periodically** — after finishing a role or every several stories: *"We've covered
  X. Want to keep going, go deeper here, switch threads, or take a break? We can always pause and
  pick up later — the corpus is saved."* Watch for shorter, flatter answers as a fatigue signal
  and offer a break before quality drops.
- **It's resumable.** Everything captured is already in `corpus.json`, so stopping and resuming
  loses nothing. Say so, so the user doesn't feel they must finish in one sitting.

## Career direction (light touch here; full exploration in stage 4)

At intake you'll have taken a quick read on direction — sharpening the current track, exploring a
pivot, or undecided (see `references/01-intake.md`). Use that only to decide where to probe a
little extra, **not** to narrow what you capture. The real "what do you want next and why"
conversation is stage 4 (`references/04-goals-interview.md`); if the user starts going deep on
goals mid-interview, that's fine — note it and fold it into stage 4 rather than forcing it here.

## Ask exactly ONE question at a time (non-negotiable)

Never stack multiple questions in one turn. Ask **one** focused question, wait for the answer,
record it, then ask the next. Stacking questions makes people answer only the easiest one and
skim the rest — and on a big topic it's overwhelming. A months-long project is dozens of small
questions asked in sequence, not one paragraph of sub-questions.

Start broad and let the story unfold, e.g. for a big project: *"How did this project originate?"*
→ (answer) → *"What existed before it?"* → *"What was the first thing you built?"* → and so on.
Each question should build on the last answer, not ignore it.

## Keep a backlog of open questions (so nothing is lost)

Big topics raise more questions than you can ask at once, and interviews get paused. Maintain a
**running backlog** of unanswered questions so threads survive across turns and sessions:

- As STAR (below) tells you what a *complete* story needs, turn the missing pieces into a list of
  concrete pending questions for that topic — but **ask them one at a time**, refining as answers
  come in (drop ones that get answered incidentally; add new ones the answers surface).
- **Persist the backlog** in `corpus.json` under `x_cv.interview_backlog` (a map of
  `topic -> [open questions]`). Update it every turn: remove answered items, append new threads.
  This is the transient interview scratchpad; the finished stories still land as proper entries.
- When you circle back to a topic, read its backlog and continue where you left off.

## Commands the user can use (tell them these exist)

Give the user explicit control words, and honor them immediately:

- **"deeper"** — keep drilling into the current thread; you clearly have more to give.
- **"quick"** — I'll take the short version of this topic and move on.
- **"skip"** — drop the current question/topic entirely (log it as skipped in the backlog).
- **"switch"** — move to a different topic now (current backlog is saved for later).
- **"back"** — return to a previous topic/question.
- **"pause"** — stop for now; everything is saved and resumable.

State the command list once near the start, and remind the user lightly if they seem unsure.
Default behavior is a **deep-dive on everything** unless the user says "quick" or "skip."

## The STAR scaffold (the shape of a complete story)

Use **STAR** as the checklist of what a finished story needs — not as four questions to fire at
once. It tells you which pending questions to put in the backlog and work through one at a time:

1. **Situation / Task** — origin, what existed before, what they were responsible for, and scale
   (team size, timeframe, budget, volume).
2. **Challenge** — what made it hard; what was at stake if it went wrong.
3. **Action** — what they *specifically* did (redirect gently from "we" to "you" — the resume
   needs *their* contribution, not the team's); the key decisions and what they built.
4. **Result** — how it turned out; any real numbers (%, $, time saved, count, before/after).

If someone is terse or says "quick," degrade gracefully to **CAR** (Challenge, Action, Result) —
don't force all four slots. Blank is fine; **an invented number is not.**

## Competency coverage (so you don't just hear the same story twice)

Aim, across the whole interview, to gather stories that evidence a spread of these
competencies. Use the list as a mental checklist, not a script — after a few stories, steer
toward the gaps ("Tell me about a time you had to smooth over a conflict"):

`leadership · teamwork · problem-solving · communication · adaptability · initiative ·
execution · technical-depth`

A rough target is **8–10 solid stories** total, each tagged with the competencies it shows.
One story can cover several.

## Quantification without fabrication

Numbers make a resume, but they must be real. When a result has no number, *try to elicit
one* with concrete follow-ups: "Roughly how many per day?" "How much faster than before?"
"Compared to what?" If the user truly doesn't know, record the outcome qualitatively and set
`metric: null`. **Never supply a number yourself.** If you propose a phrasing that contains an
estimate, label it clearly and get the user to confirm or correct it.

## Also capture the off-resume material

Explicitly ask about things resumes tend to omit but that matter for career direction and
tailoring: certifications and licenses, tools/software, languages, side projects, volunteering,
informal leadership, notable praise or awards, and genuine interests. These become corpus
entries too.

## As you go

- After each good story, write it to the corpus (stage 3) with `provenance: user-stated` and a
  `confidence` reflecting how firm it felt.
- Reconcile any contradictions you flagged at intake (e.g. conflicting dates).
- Tell the user they can pause and resume anytime; the corpus persists.

**Next:** stage 3 (`references/03-knowledge-base.md`) — the schema and mechanics of writing
these to `data/kb/corpus.json` (you'll be doing this continuously during the interview).
