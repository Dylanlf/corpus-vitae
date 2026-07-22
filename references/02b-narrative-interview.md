# Stage 2.5 — Narrative interview (the story layer)

**Goal:** capture *disposition and trajectory* — the growth arc, learning agility, differentiation,
operating principles, and motivation that the facts only *imply*. This is what actually persuades
for senior and **stretch** roles: it's the evidence that someone can grow into a job they don't yet
literally match. It's the skill's signature capability, and it's the thing generic résumé tools miss.

Run this **after** the experience interview (Stage 2), because the best narrative answers point back
at concrete stories already in the corpus. But it's a distinct pass with distinct questions and its
own storage (`x_cv.narrative`).

## Why a separate layer

- **Experience interview → evidence of output.** "Built X, moved metric Y." (Stage 2)
- **Narrative interview → evidence of disposition.** What the facts *reveal* about how the person
  operates, grows, and would handle the unknown. (This stage)

For a candidate who lacks a credential but can demonstrably grow into a role, this layer *is* the
case. Example: "hired with only Excel + math, no SQL/Python → became owner of pipelines, ads,
matching → Director of DS reporting to the CEO" is a learning-agility argument no bullet makes.

## Intellectual basis (encoded in our own words; see `ATTRIBUTIONS.md`)

Informed by narrative career-construction counseling (Savickas' Career Construction Theory / Life
Design — the free "My Career Story" workbook is a good phrasing model), Ibarra's working-identity /
signature-story research, Ganz's public-narrative "story of self" (challenge → choice → outcome →
lesson), the public-domain hero's-journey arc, and the learning-agility literature (Lombardo &
Eichinger; De Meuse). We use the *methods and constructs* only — never proprietary assessment items
(e.g. Korn Ferry viaEDGE, CliftonStrengths themes, Working Genius types) or trademarked names.
Treat learning agility as a useful lens, **not** settled science.

## How to run it

Same discipline as Stage 2: **one question at a time**, honor the command words (`deeper`, `quick`,
`skip`, `switch`, `back`, `pause`), and keep a backlog in `x_cv.interview_backlog` under a
`narrative-*` topic key. Default is a deep-dive. These questions are more reflective than Stage 2's,
so give the person room — and **always push for the concrete moment/evidence** behind an abstract
claim, or it's just self-flattery.

## The question framework (~11 questions, 5 themes)

Ask in your own words; adapt order to the conversation. One at a time.

**A. Growth arc / trajectory** *(Savickas "script"; Ibarra; Ganz; hero's journey)*
1. What's the throughline that connects where you started to where you're headed?
2. Tell me about a real turning point — what changed, what did you choose, and who did you become
   because of it?
3. What "possible self" are you growing into right now, and how are you testing it?

**B. Learning agility** *(learning-agility dimensions — as a lens)*
4. Describe a time there was no playbook. How did you figure out what to do, and what did you learn?
5. Tell me about being wrong or failing — what did you take from it, and how do you know it stuck?
6. When you're dropped into something unfamiliar, how do you get up to speed and start delivering?

**C. Differentiation** *(Ibarra signature story; evidence from the brag-doc/corpus)*
7. What do you do differently from most people in your field — and what's the evidence?
8. What's a problem you're unusually good at that others find hard?

**D. Operating principles / philosophy** *(Savickas "self-advice/motto")*
9. What's a rule or principle you keep coming back to in how you work? Where did it come from?
10. What kind of work genuinely energizes vs. drains you — and what does that say about where you
    add the most value?

**E. Motivation / drivers** *(Savickas "role models" & "preoccupation"; Ganz "why act")*
11. Whom did you admire growing up, and what about them still shows up in how you operate today?
    - Probe: what's the deeper "why" behind the direction you're pushing toward now?

## Storage: `x_cv.narrative` (corpus-level)

Write to `data/kb/corpus.json` under top-level `x_cv.narrative` (not tied to one role):

```json
"narrative": {
  "growth_arc": "1-3 sentence arc, e.g. hired with X, grew into Y, now Z.",
  "learning_agility": ["evidence-backed examples of learning fast in the unfamiliar"],
  "differentiators": ["what they do better than peers, each with a pointer to evidence"],
  "operating_principles": ["reusable rules/heuristics + origin"],
  "motivation": "what drives them and why",
  "evidence_links": ["ids of corpus stories that back the above"]
}
```

**Honesty guardrail (critical):** every narrative element must be **evidence-backed** — link it to
concrete corpus stories (`evidence_links`). A growth-arc or differentiator with no underlying story
is opinion, not evidence; either get the story (and add it to the corpus) or don't assert it. This
is the same "defend-it-in-an-interview" test applied to narrative claims.

## Where it feeds

- **`basics.summary`** — the narrative gives the résumé a true, distinctive positioning line.
- **Capability / true-need fit (Stage 6)** — learning-agility + differentiation evidence is what
  justifies a high *capability* score even when *literal* fit is low.
- **AI-use / portfolio narrative (Stage 7, Enhancement C)** — building corpus-vitae is itself a
  growth/AI story; capture it here if relevant.
- **Cover narrative** — the growth arc + differentiation is the "why me" for stretch roles.

**Next:** Stage 3 to make sure any new stories surfaced here are also captured as proper entries,
then onward to goals/coaching/scoring.
