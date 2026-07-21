# corpus-vitae

A Claude skill for going from an old resume to tailored applications, end to end.

*The name plays on **curriculum vitae**: **corpus** is both the NLP term for a body
of training text and the Latin for "body" — here, your **body of work**.*

**Status:** bare-bones scaffold. Design, APIs, formats, and data schemas are all
still to be decided in a dedicated planning session — nothing here is final.

## Idea

A tool that helps you turn your real history into honest, tailored job-application
materials. The exact steps, their ordering, and what it produces are **all still
open** — see [PLANNING.md](PLANNING.md).

As a *strawman only* (not a decision — something to react to), an early sketch imagined:
intake an old resume → interview to elicit facts & stories → build a reusable
knowledge base → analyze/rank a target job → tailor a resume → assemble application
materials. Expect this to be reordered, split, merged, or replaced during planning.

## Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill entry point / instructions (stub for now). |
| `references/` | Reference docs (structure TBD). |
| `scripts/` | Helper scripts (e.g. resume parsing). |
| `templates/` | Resume / output templates. |
| `data/` | **Your** personal inputs — **gitignored, never committed.** |

## Design principle

The **machinery is public; your data is private.** Everything a user needs to run the
skill lives in the repo with zero PII. Personal inputs live only in local `data/`,
which is gitignored — so this repo can go public without leaking anyone's resume.
