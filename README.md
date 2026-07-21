# career-forge *(working name — TBD)*

A Claude skill for going from an old resume to tailored applications, end to end.

**Status:** bare-bones scaffold. Design, APIs, formats, and data schemas are all
still to be decided in a dedicated planning session — nothing here is final.

## Idea

A reusable pipeline that helps you:

1. **Intake** — ingest an existing resume (PDF / docx) into structured text.
2. **Interview** — a guided "Claude interview" that elicits your facts, achievements, and stories.
3. **Knowledge base** — a durable store of those facts/stories, reusable across every application.
4. **Job analysis** — parse a target job posting and rank its requirements / desired features.
5. **Tailoring** — match the knowledge base to a ranked job to generate a custom resume.
6. **Apply** — assemble application materials (scope TBD; generate-first, no auto-submit for now).

## Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill entry point / instructions (stub for now). |
| `references/` | Per-stage reference docs for the pipeline above. |
| `scripts/` | Helper scripts (e.g. resume parsing). |
| `templates/` | Resume / output templates. |
| `data/` | **Your** personal inputs — **gitignored, never committed.** |

## Design principle

The **machinery is public; your data is private.** Everything a user needs to run the
skill lives in the repo with zero PII. Personal inputs live only in local `data/`,
which is gitignored — so this repo can go public without leaking anyone's resume.
