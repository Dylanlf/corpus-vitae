# Stage 7.5 — Callability review

**Goal:** before the user sends a tailored résumé, review it for **callability** — the probability it
survives the ATS + recruiter screen and earns a call — and surface fixable red flags. This is distinct
from Stage 6 fit: fit asks "can they do the job?"; callability asks "will a screener act on this doc?".
Output a short `data/<user>/targets/<slug>/callability.md`.

Run after Stage 7 (a résumé exists), or any time the user asks "will this get a call?".

## Grounding (evidence-graded — cite honestly, don't overclaim)

- **The 7-second scan is real** (Ladders eye-tracking): recruiters triage in ~6–7s, fixating on name,
  current title/company + dates, previous title/company + dates, and education, in an **F-pattern**
  (top third, then down the left margin). Design for that glance. *[moderate — small vendor study, but
  the direction holds]*
- **ATS mostly ranks and buries; it rarely auto-rejects.** The "75% auto-rejected" figure is a debunked
  myth. The one genuine auto-reject mechanism is **knockout questions** (location, work authorization,
  minimum years, required degree/license). Poor parseability causes *burial*, not rejection. *[strong]*
- **Gaps and job-hopping hurt; long tenure does not.** Employment-gap penalties are real and steep
  (Kroft/NBER); single-employer résumés actually out-callback job-hoppers (Chicago Booth). So long
  tenure is *not* a red flag — only a flat, non-progressing title is a mild concern. *[strong]*
- **The one-page rule is outdated** for experienced people: ~475–600 words / 2 pages is fine (better)
  for senior candidates. *[moderate]*
- **Clear writing raises hire rates** (~8% in a ~500k-user experiment) — the strongest causal result in
  the space. **AI *assistance for clarity* helps; generic AI *voice* hurts** (recruiters reject a
  majority of résumés they *flag* as AI — the tells are cliché verbs and uniform voice, not specific
  quantified content). *[strong for clarity; moderate/rising for AI-voice penalty]*
- **Quantified achievements + JD-keyword mirroring raise callbacks.** *[moderate]*

## The callability scorecard (score each 0–10, weights sum to 100)

| # | Dimension | Wt | 10 looks like |
|---|-----------|----|---------------|
| 1 | **Level & title fit** to the target | 22 | Current/previous titles at or one step below target; trajectory reads upward. |
| 2 | **Keyword/JD match & ATS-parseability** | 20 | Mirrors JD must-have terms; single-column, clean parse; no knockout fails. |
| 3 | **Quantified impact** | 18 | Most bullets carry a real number (%, $, count, time). |
| 4 | **Writing clarity & professionalism** | 15 | Crisp, specific, error-free, human voice (no generic-AI tells). |
| 5 | **Scannability / layout / length** | 12 | F-pattern, bold titles, bullets, length scaled to seniority. |
| 6 | **Tenure & continuity narrative** | 8 | No unexplained gaps; progression visible. |
| 7 | **Tailored summary / top-of-page value** | 5 | Role-specific 2–3 line summary in the highest-fixation zone. |

**Index = Σ(score×weight)/100.** Bands: **≥7.5 strong-yes · 5.5–7.4 maybe (burial risk) · <5.5 likely screened/buried.**
Always give a one-line rationale per dimension citing the résumé — never just a number.

## Ranked red-flag checklist (hard flags first)

1. **Knockout mismatch** — location, work-auth, missing required degree/license, below minimum years.
   *Hard flag; genuine auto-reject.* Check the posting's stated gates against the résumé. *[strong]*
2. **Unexplained employment gap** (esp. a long current one). *[strong]*
3. **Poor ATS parseability** — multi-column, tables, text boxes, header/footer contact info, graphics-as-text. *[moderate]*
4. **Level/title mismatch** — over- or under-leveled vs target (e.g. Director→Manager reads as flight risk); flat trajectory. *[folk + mechanism]*
5. **No quantification** — duty-listing with no results. *[moderate]*
6. **Job-hopping** — multiple unexplained <18-month stints. *[strong]*
7. **Generic-AI tells** — cliché verbs ("delve, leverage, spearheaded"), uniform voice; and an explicit
   "written by AI" signal. Note: specific, quantified content does NOT read as AI. *[moderate, rising]*
8. **Buzzword stuffing without evidence.** *[folk]*
9. **Wrong length for seniority.** *[moderate]*
10. **Weak/generic summary** in prime real estate; **typos** (cheap to fix, disproportionate penalty). *[strong for typos]*

## Honesty & the fix loop

- Every fix must be honest — improve *framing, targeting, clarity, and logistics*, never fabricate.
- The most common high-leverage fixes: fix a **knockout** (add "open to relocation" / confirm remote),
  **re-target the level**, make a **flat tenure show progression**, **add missing metrics** (ask the
  user; don't invent), tighten the summary, add a LinkedIn URL, and convert generic-AI phrasing to the
  user's specific, concrete language.
- If callability is capped by something honest-but-unfixable (a real knockout, a genuine over-level),
  say so and route to strategy (bypass the filter via referral, or pick a better-leveled target — see
  Stage 6 strategy routing). Don't inflate the résumé to fake a pass.

## Output: `callability.md`
Use `templates/callability-scorecard.md`: the 7 scored dimensions + index + band, the ranked red flags
found (with fixes), and a short verdict + top-3 fixes.

**Next:** apply the agreed fixes (back to Stage 7), then format the final files (`references/08-formatting.md`).
