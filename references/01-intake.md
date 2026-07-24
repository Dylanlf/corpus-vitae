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

1. **Check `data/<user>/inbox/`** (create it if missing). See what's there.
2. **Ask for any career materials they have — not just a résumé.** The more they share here, the
   richer the corpus and the lighter the interview later. Explicitly invite any subset, in whatever
   form is easiest (attach, paste, or point you to it — **you** save copies into `inbox/`; never ask
   them to move files around):
   - **Résumé / CV** (current or old) and **cover letters**
   - **LinkedIn** profile or data export
   - **Brag docs / accomplishment lists**; past **performance reviews / self-reviews**
   - **Task / responsibility lists or job descriptions** for current and past roles
   - **Certifications, licenses, transcripts, test scores**
   - **Project write-ups, portfolios, published work, awards, recommendation letters**

   Nothing is required. If they have none — or don't want to dig any up — that's fine: say so and go
   straight to the interview (stage 2), building the corpus from the conversation.
3. **Read each item** with the right tool:
   - **PDF** → the **`pdf` skill**; if it's a scan/photo (e.g. a certificate), OCR it.
   - **DOCX** → the **`docx` skill**. **XLSX / CSV** (e.g. an accomplishment tracker) → read as tables.
   - **TXT / MD** → read directly. **Images / screenshots** (certs, awards) → OCR or describe.
   - LinkedIn export, loose notes, a bulleted brain-dump, pasted text — all welcome as raw input.
4. **Normalize** everything into one file, `data/<user>/inbox/_parsed.md`, lightly structured under
   headings (Contact, Summary, Experience, Education, Skills, **Certifications & licenses**,
   **Accomplishments & awards**, **Other**). When several documents are provided, **label each fact
   with its source** (e.g. "from 2023 review", "from cover letter") and note any contradictions to
   raise in the interview rather than silently picking one. Preserve the user's own wording and every
   date/number exactly — this is source material (provenance: the document it came from). Do not
   embellish, drop, or "improve" anything here.
5. **Confirm and orient** (explicit step — do both):
   - **Completeness:** briefly summarize what you found across all the materials ("I read a 2-page
     résumé + a 2023 self-review + two certs: 3 roles, one degree, ~10 skills") and ask if that's the
     full set, or whether there's history, projects, accomplishments, or skills not in these files
     (including anything newer than the résumé).
   - **Direction (quick read only):** ask whether they're sharpening for their **current track**,
     exploring a **pivot/career change**, or **undecided**. This sets context for where to probe
     a little extra in the interview — it does **not** narrow what we capture (we capture
     everything; see stage 2). Make clear the full "what do you want and why" conversation comes
     later, at stage 4. If they're unsure, that's a fine answer; note it and move on.

## Notes

- Multiple files are fine; merge them, noting any contradictions (e.g. different dates for the
  same role) to raise during the interview rather than silently picking one.
- If a scan/image PDF (or a photo of a certificate) has no text layer, OCR it; if OCR is unreliable,
  say so and ask for a text version or capture the details in the interview instead.
- Keep everything under `data/`. Never copy resume content anywhere else.

**Next:** stage 2 (`references/02-interview.md`).
