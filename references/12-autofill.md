# Stage 10 — Application autofill (OPTIONAL, opt-in, skippable)

**Goal:** for **one** application at a time, use the user's stored bio (`profile.json`) + their tailored
résumé to **fill** a live application form in the browser, then **stop for the human to review and
submit**. This assists the boring part of applying; it never applies *for* the user.

> **This stage is OFF by default and fully skippable.** The whole pipeline (corpus → search → scoring →
> résumé → PDF) works without it. Only run it when the user explicitly asks ("help me fill this
> application"). If they'd rather apply by hand, generate the fill plan (below) as a cheat-sheet and
> stop there. Preference: `autofill` (default **false**).

## Hard safety rules (non-negotiable — do not "optimize" these away)
These mirror the assistant's standing rules for acting in a browser. Every one is a hard stop:
- **Fill only. NEVER submit.** Do not click submit / apply / send / confirm. The human reviews the
  filled form and clicks submit themselves. (Submitting an application is irreversible and outward-facing.)
- **Get an explicit "go" before entering any personal data** into the form (per application). Show the
  **fill plan** first (below) so they see exactly what will be entered.
- **Hand back to the user — never do these yourself:** signing in / entering passwords, **creating an
  account** (common on Workday), **CAPTCHAs / bot checks**, anything asking for payment or IDs. Pause,
  say what's needed, let them do it, then continue.
- **Sensitive fields need opt-in:** compensation and the voluntary EEO self-ID block are entered only if
  the user tells you to for this form; "Decline to self-identify" is always acceptable. Never put comp
  or self-ID on the résumé.
- **Never guess a knockout/screening answer** (sponsorship, years-of-experience gates, eligibility).
  Surface it and let the user answer — a wrong knockout auto-rejects them.
- **No fabrication** (same as everywhere): if a field needs a fact that isn't in `profile.json`, ask —
  don't invent it.

## Requirements (and how to skip gracefully)
- **Logged-in real Chrome + the Claude browser extension** (`claude-in-chrome`). This is the surface
  that can attach a file and reach session-gated portals. It runs as the **machine owner's** session
  (see `05-coaching.md`) — fine for that person's own applications.
- An **`apply_url`** (the company/ATS form — captured per `05-coaching.md`) and a **tailored résumé PDF**
  (Stage 8), plus `profile.json` (Stage 0).
- **If the extension isn't connected** (it often isn't): say so plainly, generate the fill plan as a
  copy-paste cheat-sheet, and let the user fill the form themselves. Don't error out; this is the
  skippable path.

## Step 1 — Build the fill plan (review-first, no browser yet)
```
python scripts/fill_plan.py --user <user> --target <slug>
```
Writes `data/<user>/targets/<slug>/fill-plan.md`, sorting fields into **auto-fill** (factual/safe),
**ask-first** (comp, EEO), and **you'll answer live** (blanks + custom/knockout questions). Show it to
the user and get their go-ahead. This is the "here's exactly what I'll enter" preview the good autofill
tools show before touching anything.

## Step 2 — Open the form
Confirm the browser extension is connected (`list_connected_browsers`); if not, fall back to the
cheat-sheet path above. Otherwise `navigate` to the `apply_url` in the logged-in Chrome.

## Step 3 — Fill (map → enter → attach), one field at a time
- `read_page` to get the accessibility tree (`ref_N` for each field). Prefer `form_input` by `ref`
  (robust); fall back to `computer` click/type only when needed.
- Enter the **auto-fill** values from the plan; map by the field's visible label/name:
  name → first/middle/last, email, phone, location, LinkedIn/GitHub/portfolio, work authorization,
  sponsorship yes/no, start date. (See the map below.)
- **Attach the résumé** with `file_upload` (the Stage-8 PDF; DOCX if the portal demands Word).
- **Ask-first** fields: enter only what the user approved for this form.
- **Custom/knockout/EEO** questions: read them out, let the user answer, enter their answer verbatim.
- On a **login / account-creation / CAPTCHA / payment** wall: stop and hand it to the user.

## Step 4 — Review & stop
`screenshot` (or `read_page`) the completed form, summarize what you entered and what's left blank, and
**hand control back**: *"Filled everything I safely could — review it and click Submit yourself."*
Do not submit. If the user then reports success, you may record it via `interactions.jsonl`
(`event: status, status: applied`) — but that's their call, and applying/tracking is otherwise out of
scope.

## profile.json → common application fields
| Form field(s) | profile.json source |
|---|---|
| First / middle / last / full name, preferred name | `identity.*` |
| Pronouns | `identity.pronouns` |
| Email, phone | `contact.email`, `contact.phone` |
| City / state / country / location | `location.*` (use `location.display` for a metro label) |
| Willing to relocate, remote/hybrid/onsite pref | `location.willing_to_relocate`, `location.work_arrangement_pref` |
| LinkedIn / GitHub / portfolio / website | `links.*`, `contact.personal_website` |
| Work authorization; "require sponsorship now/future?" | `work_eligibility.*` |
| Desired compensation *(ask-first)* | `compensation.*` (enter only if asked + approved; never volunteer) |
| Available start date / notice period | `job_search.available_start_date`, `job_search.notice_period_weeks` |
| Voluntary EEO self-ID *(opt-in only)* | `voluntary_self_id.*` (else "Decline to self-identify") |
| Résumé / CV upload | the Stage-8 PDF (`<First>-<Last>-Resume.pdf`); DOCX if required |
| Cover letter | if generated for this target; else skip |

## Per-ATS reality (set expectations)
- **Lever** — single-page; fastest and cleanest. Ideal.
- **Greenhouse / Ashby / SmartRecruiters** — form-heavy (résumé upload + fields + a few knockout/EEO
  questions); EEO is optional with a decline option. Straightforward but read every custom question.
- **Workday** — **hard / partial.** Usually requires creating an account (hand off), then 5–7 pages with
  work-history re-entry. Fill what you can page by page; expect several handoffs; it's fine to tell the
  user this one is mostly manual.
- **Login-gated / heavy anti-bot / CAPTCHA** — hand off by rule; don't try to defeat protections.

**End of pipeline.** This is the furthest the skill goes: a filled, unsubmitted form the user reviews
and sends. Submitting, contacting, and tracking remain the user's.
