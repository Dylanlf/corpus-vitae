# Stage 3 — Knowledge base (the corpus)

**Goal:** capture everything true about the user as a durable, reusable, structured file —
`data/kb/corpus.json`. This is the crown jewel: built once, reused for every job. Every
downstream stage reads from it, and stage 7 may assert *only* what lives here.

Read `templates/corpus.schema.md` first — it's the authoritative schema (JSON Resume + the
`x_cv` extension) with a full worked example. This page is the *how-to*.

## What the corpus is (and isn't)

- **Is:** an atomic, categorized store of facts and stories — one entry per role, project,
  credential, skill cluster, or story. Rich metadata (STAR, provenance, confidence,
  competencies) hangs off each via `x_cv`.
- **Isn't:** a resume. Never order, trim, or spin entries here for a particular job — that's
  stage 7, and it works on a *copy*. The corpus stays complete and neutral.

## Mechanics

1. **Ensure the file exists.** `mkdir -p data/kb`. If `corpus.json` is absent, initialize it
   from the example skeleton in `templates/corpus.schema.md` (fill `basics` from intake).
2. **Edit safely.** Read the file, parse JSON, add/update entries, write valid JSON back.
   Never leave it malformed — downstream stages parse it.
3. **Populate `basics`** from intake (name, contact, a neutral one-line label/summary).
4. **Add entries as the interview produces them:**
   - A job → a `work` item with `id`, `name`, `position`, dates, `summary`, `highlights`, and
     an `x_cv` block (STAR, metric-or-null, competencies, provenance, confidence, tags).
   - A project / side project → a `projects` item (same `x_cv` treatment).
   - Degree/school → `education`; license/cert → `certificates`; award/recognition → `awards`;
     volunteering → `volunteer`; languages → `languages`; genuine hobbies → `interests`.
   - Skills → `skills` entries (group into clusters with `keywords`, e.g. "POS systems").
   - A strong story not tied to one role → `x_cv.stories[]`, optionally `link`ed to an entry.
5. **Give every substantive entry a stable `id`** (kebab-case) so stages 6–7 can reference it.

## Provenance & confidence discipline (this is what makes honesty checkable)

- `on-old-resume` — came from the parsed resume. `user-stated` — the user told you in the
  interview. `verifiable` — the user has documentation/evidence.
- `confidence` (0–1) — your read on how firm and defensible the claim is. A vividly recalled,
  documented win is ~0.9; a fuzzy "I think it was around…" is ~0.5 and should be flagged for
  the user to firm up.
- **`metric` is real numbers only.** No number → `null`. This single rule prevents most
  résumé fabrication downstream.

## Keeping it healthy

- **Dedupe:** if the same accomplishment shows up under two roles, keep one canonical entry.
- **Contradictions:** when intake and interview disagree (e.g. dates), resolve with the user
  and store the corrected value; don't keep both silently.
- **Review pass:** when the interview winds down, show the user a compact summary of the corpus
  (roles, counts of stories, skills, credentials) and invite edits. The user owns this file.

## Definition of done for stages 1–3

A valid `data/kb/corpus.json` that:
- has `basics` filled;
- covers each real role/project with at least a `summary` and, where possible, a STAR story;
- has ~8–10 competency-tagged stories spread across the competency list;
- carries provenance + confidence on every `x_cv` entry, and `metric: null` wherever no real
  number exists.

**Next:** stage 4 (`references/04-goals-interview.md`).
