# PLANNING — open questions for corpus-vitae

**Status: nothing here is decided.** This file is a set of *questions*, not a plan.
It deliberately makes **no assumptions** about what steps exist, what order they run
in, what the tool outputs, or how it's built. The 6-stage flow sketched in the
[README](README.md) is one *possible* framing to react to — treat it as a strawman
to challenge, not a decision. Answer, reorder, split, merge, or throw out anything
below.

Use this as the agenda for the dedicated planning session.

---

## 1. Purpose & scope
- What is the single core job this tool does? (One sentence, if possible.)
- What is explicitly **out** of scope, at least for v1?
- Is this primarily *for you*, or a polished thing others clone and run? Does that change with time?
- What does "done enough to use" look like? What does "successful" look like later?

## 2. Who & when
- Who uses it (just you / friends / public)? What's their technical level?
- At what moments does someone reach for it? (Starting a fresh search? Per job? Refreshing a stale resume?)
- How often — one-shot, or an ongoing thing they return to?

## 3. The process itself (no assumed steps or order)
- What are the *actual* pieces of work involved in going from "raw history" to "submitted-worthy materials"?
- Which of those must be steps in the tool vs. things done outside it?
- Is it a linear pipeline at all, or more of a loop / a set of independent tools / a conversation?
- What can be skipped, reordered, or repeated? What depends on what?
- Where does a human (you) have to be in the loop, and where shouldn't automation act alone?

## 4. Inputs
- What does the tool start from? (Old resume? LinkedIn? Notes? Nothing — pure interview?)
- Which input formats matter (PDF, docx, plain text, URLs, pasted job posts)?
- What's the minimum a user must provide before it's useful?

## 5. Outputs (no assumed format)
- What artifacts should it actually produce? (Resume? Cover letter? A reusable knowledge base? A match/fit analysis? A tracker? Something else?)
- What format(s) for each — Markdown, HTML, PDF, docx, JSON, a mix? Who consumes each format?
- Are outputs one-and-done, or living documents that get regenerated as inputs change?

## 6. Honesty & the "relevant truth" principle
- How does the tool stay honest — surfacing *true, relevant* experience rather than inflating?
- What guardrails prevent fabrication or overstatement?
- How is "relevance to this job" decided and made transparent/editable?

## 7. Data: storage, schema, privacy
- What personal data does it hold (facts, stories, history, job targets), and in what shape?
- Storage format & location (flat files? structured JSON/YAML? a DB? all local?).
- How does the public-machinery / private-data separation hold up as the design grows?
- Retention, portability, and "delete everything" — do these matter?

## 8. The "apply" question (kept open on purpose)
- How far does the tool go? Generate materials only → hand to user? Track applications? Draft submissions? Anything more?
- Where is the hard line for automated, outward-facing, or irreversible actions?

## 9. Tech, APIs & connections
- What external services (if any) — job boards, LinkedIn, ATS portals, file converters, search?
- What are their auth, rate-limit, ToS, and reliability constraints? Which are worth the dependency?
- What can be done with local tooling / no external calls?
- Language & runtime for any scripts (Python? Node? shell?).

## 10. Claude skill architecture
- What lives in `SKILL.md` vs. `references/` vs. `scripts/` vs. `templates/`?
- Is it one skill or several composable ones?
- How do the existing pdf/docx/xlsx skills fit in (reuse vs. reimplement)?
- What's the smallest first slice worth building to learn the most?

## 11. Distribution & licensing (later)
- If/when public: license? contribution model? How do others supply their own `data/`?
- Naming/trademark note carried over: keep "Claude" out of the public-facing product name to avoid implying official endorsement.

## 12. Unknowns / risks / things to revisit
- What don't we know yet that could reshape the whole design?
- Biggest risks (brittleness, privacy, ToS on scraping job data, scope creep)?
- Assumptions to explicitly test before committing to them.

---

*When decisions get made, promote them out of this file into real docs (README,
SKILL.md, design notes) and delete the corresponding open question here.*
