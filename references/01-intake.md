# Stage 1 — Intake

**Goal:** get the user's existing history into plain text we can work from. Read, don't
interpret. Interpretation happens in the interview (stage 2) and corpus-building (stage 3).

## Step 0 — Profile / bio (do this first; local-only)

Before reading any resume, capture the user's **profile** to `data/<user>/profile.json` (template:
`templates/profile.example.json`) — a small structured bio: legal name (first / middle / last),
preferred name, pronouns; contact (email, phone); location + relocation / remote preference; links
(LinkedIn, GitHub, portfolio); **work eligibility** (work authorization, visa-sponsorship need);
**job-search status** (open-to-work + since when, notice period, confidential?); comp expectations;
and an optional voluntary EEO self-ID block.

Why first: it makes the resume header accurate, and it's exactly the field set job applications ask
for — so later we can **autofill (never auto-submit)** an application from it. Fill what the user
states; leave unknowns blank and list them in `_confirm` — **don't guess** identity, location,
work authorization, or self-ID. The `compensation` and `voluntary_self_id` blocks are sensitive:
capture only if the user wants them, keep them local-only, and never put them on a resume or submit
them automatically. Like all personal data, `profile.json` lives only under gitignored
`data/<user>/`.

## Steps

1. **Look in `data/inbox/`.** Create it if missing (`mkdir -p data/inbox`). List what's there.
2. **If it's empty,** ask the user to drop an old resume in — any of PDF, DOCX, TXT, or MD.
   If they genuinely have no resume, that's fine: tell them we'll build the corpus from the
   interview instead, and skip straight to stage 2.
3. **Read each file** with the right tool:
   - **PDF** → use the **`pdf` skill** to extract text.
   - **DOCX** → use the **`docx` skill**.
   - **TXT / MD** → read directly.
   - LinkedIn export, notes, a bulleted brain-dump — all welcome; treat as more raw input.
4. **Normalize** everything into one file, `data/inbox/_parsed.md`, lightly structured under
   headings (Contact, Summary, Experience, Education, Skills, Other). Preserve the user's own
   wording and every date/number exactly — this is source material, and its provenance will be
   `on-old-resume`. Do not embellish, drop, or "improve" anything here.
5. **Confirm and orient** (explicit step — do both):
   - **Completeness:** briefly summarize what you found ("I read a 2-page resume: 3 roles, one
     degree, ~10 skills") and ask if that's the full set, or whether there's history, projects,
     or skills not in these files (including anything newer than the resume).
   - **Direction (quick read only):** ask whether they're sharpening for their **current track**,
     exploring a **pivot/career change**, or **undecided**. This sets context for where to probe
     a little extra in the interview — it does **not** narrow what we capture (we capture
     everything; see stage 2). Make clear the full "what do you want and why" conversation comes
     later, at stage 4. If they're unsure, that's a fine answer; note it and move on.

## Notes

- Multiple files are fine; merge them, noting any contradictions (e.g. different dates for the
  same role) to raise during the interview rather than silently picking one.
- If a scan/image PDF has no extractable text, say so and ask for a text version or to proceed
  by interview.
- Keep everything under `data/`. Never copy resume content anywhere else.

**Next:** stage 2 (`references/02-interview.md`).
