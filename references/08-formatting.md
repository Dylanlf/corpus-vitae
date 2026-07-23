# Stage 8 — Format / export (ATS-safe PDF + DOCX)

**Goal:** turn the approved tailored résumé into the files the user actually submits — a **text-layer
PDF** and a **DOCX**, both single-column and ATS-safe, designed to satisfy the ATS parser *and* the
7-second human scan at once. Output to `data/<user>/targets/<slug>/`.

## What to produce & submit (evidence-based)
- Build **both** from the one source (`resume.json` / `resume.md`).
- **PDF (text-layer)** — the default when emailing a human or when a portal accepts PDF; modern ATS
  (Workday, Greenhouse, Lever) parse a clean text-based PDF fine.
- **DOCX** — submit when a portal/recruiter asks for Word, for staffing agencies, or known-legacy ATS
  (Taleo/iCIMS).
- **Never** submit an image/scanned PDF. Verify the PDF passes the **copy-paste text test** (select
  all → text copies cleanly). The "PDF fails ATS" horror stories are almost always image PDFs.
- The "always PDF" / "always DOCX" advice is wrong — it depends on the submission channel.

## Design spec — refined senior-technical (implement for PDF and DOCX)

ATS-safety comes from **structure** (single column, real text layer, standard headings, a clean font
ToUnicode map), **not** from a "safe generic" look. So this spec is deliberately *designed* — smaller
type with generous leading, a compact header, near-monochrome, hairline rules — which reads as
seniority/craft to a technical audience while parsing identically to a plain résumé. The
**non-negotiable gate is the copy-paste text test** (below), which settles ATS-safety better than any
font/size rule. (A "safe generic" 11–12pt Calibri variant is fine for conservative/non-technical
audiences — treat these as two presets.)

```
LAYOUT     Single column, full width. NO tables (except a borderless title/dates row), text boxes,
           sidebars, columns, or images. US Letter. Margins 0.7in sides / 0.55in top-bottom.
           Left-aligned. Length: 1pg (<10 yrs), 2pg (10+) — don't shrink <10pt to force 1 page.
FONT       ONE clean grotesque, EMBEDDED with a valid ToUnicode CMap. Default: Noto Sans (system,
           embeds via reportlab TTFont). Also good: IBM Plex Sans / Inter / Source Sans (ship a TTF).
           DOCX uses Arial (predictable, non-Calibri; recipient re-renders). Never outline text.
TYPE       Name 19pt bold · title/positioning line 10pt (#555) · contact 9.5pt one line ·
           section headings 10.5pt bold UPPERCASE (only ~0.5pt over body; weight+caps, not size) ·
           role line 10pt bold + dates 9.5pt (#555) right-aligned on the same line ·
           org/edu sub-line 9.5pt italic (#555) · body/bullets 10pt.
LEADING/   Body leading ~13.7pt (~1.37x). Spacing hierarchy (this is the "designed" rhythm):
SPACING    14pt BEFORE a section heading, ~4-5pt AFTER (heading hugs its content), 8-9pt between
           entries, 3pt between bullets within an entry.
COLOR      Near-monochrome: body #1A1A1A, secondary meta (dates, title line) #555. No accent color
           (or at most one restrained accent on the name). Color is invisible to ATS.
DIVIDERS   0.5pt hairline rule in #CCCCCC under each UPPERCASE heading. No thick/black/full-page bars,
           no shaded bands, no boxed header — those are the template tells.
CONTACT    Top of page 1 in the BODY (never the doc header/footer region — parsers drop it). Left-
           aligned name (not centered); one contact line, `·`-separated, no field labels. Whole
           header block <= ~0.75in tall. Source the name + contact line from `data/<user>/profile.json`
           (Stage 0) — legal/preferred name, email, phone, location, LinkedIn, GitHub — so it's exact.
           Never put comp, work-authorization, or voluntary self-ID fields on the resume.
HEADINGS   Standard literal names only: Summary, Skills, Experience, Projects, Education,
           Certifications. (Caps styling is fine; the word must stay intact in the text layer.)
BULLETS    Standard round •, hanging indent. Start with a strong verb; lead with the metric.
DATES      "Mon YYYY – Mon YYYY" (e.g. "Mar 2021 – Present"), consistent.
FILE NAME  FirstName-LastName-Resume.pdf / .docx (optionally add role). Hyphens; no spaces/ALL-CAPS.
```

## Toolchain (in order of preference)
1. **Pandoc** (if installed) — `resume.md` → DOCX via `--reference-doc=<styled.docx>` and → PDF via a
   LaTeX/Typst engine or HTML print. Single-column by construction → ATS-clean. Known-good.
2. **Bundled generator (recommended default here — no system tools needed):**
   **`scripts/render_resume.py`** reads a standard `resume.json` and emits both an ATS-safe DOCX
   (`python-docx`) and a text-layer PDF (`reportlab`) per the spec above — single column, standard
   fonts, standard headings, round bullets, dates right-aligned, `<First>-<Last>-Resume.{pdf,docx}`.
   It drops the internal `meta` (so the honesty dial never prints) and adds the neutral build-credit
   footer unless `--no-credit` is passed.
   ```
   python scripts/setup.py                                # one-time: builds .venv + installs deps
   .venv/bin/python scripts/render_resume.py data/<user>/targets/<slug>/resume.json
   ```
   `scripts/setup.py` is idempotent and handles the common gotchas itself: it creates the gitignored
   `.venv` and installs `python-docx` + `reportlab`, and if the system python lacks pip/ensurepip it
   bootstraps pip via the official get-pip.py automatically. **If setup can't finish** (no network /
   locked-down machine), still hand over `resume.md` and offer a Print-to-PDF path — don't surface the
   error to the user (see "How this runs" in `SKILL.md`).
3. **Browser/word-processor "Print/Save as PDF"** produces a text layer too — acceptable, but avoid
   anything that rasterizes (screenshot/scan/flatten/design-tool image export).

## JSON Resume themes — caution
Most default JSON Resume HTML themes are **two-column/sidebar** → they scramble ATS reading order.
Only use a **single-column** theme, or render via the toolchain above. Don't assume a theme is safe.

## Honesty note
Formatting changes presentation only — never content. The PDF/DOCX must match the approved
`resume.md`/`resume.json` word-for-word (minus the internal `meta`). Keep the neutral build-credit
footer only if `build_credit` is on (never the dial number).

**This is the last stage.** Hand the user the named PDF + DOCX; applying remains out of scope.
