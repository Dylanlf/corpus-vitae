# Stage 7 — Tailoring (the perfect-but-honest resume)

**Goal:** produce a per-job resume that shows the *most relevant true version* of the user for
one posting. Output a **standard JSON Resume** at `data/targets/<slug>/resume.json` and a
rendered Markdown resume at `data/targets/<slug>/resume.md`.

Read for this target: `data/kb/corpus.json`, the target's `posting.md`, `gap-analysis.md`, and
`scorecard.md`. Read `templates/corpus.schema.md` for field names and
`templates/resume-tailored.md` for the Markdown layout.

## The honesty dial

The user sets a **0–10 tailoring dial** (default **6**). It controls how aggressively you
*frame* real experience — **never whether you tell the truth.** Ask for the setting (and let
them change it and regenerate).

| Setting | Framing behavior |
|---------|------------------|
| **0** | Straight from the corpus. Minimal reordering, the user's own wording, no spin. |
| **3–4** | Light tailoring: pick relevant entries, reorder to match the posting, tighten wording. |
| **5–7** (default) | Standard tailoring: select the best-matching stories, lead with strengths from the gap analysis, adopt the posting's vocabulary for things the user genuinely did, quantify real outcomes, write crisp achievement bullets. |
| **8–9** | Aggressive framing: strongest still-true interpretation of scope and impact; foreground leadership/ownership the user really had; confident, senior phrasing. |
| **10** | Maximal + "reasonable rounding": informal→formal title where defensible (e.g. "handled the schedule" → "Scheduling Coordinator (informal)"), generous-but-defensible scope. Everything still traceable and interview-defensible. |

### The hard floor (every setting, including 10)

Never fabricate: **employers, dates, degrees, certifications, titles implying a role never
held, or metrics/numbers the user didn't give.** Respect the target's **do-not-claim list**
from the gap analysis absolutely.

### The governing test

Before writing any claim, apply it: *Could the user defend this in a detailed interview
without dodging, deflecting, or inventing context?* If not, cut it or dial it back. And:
**every claim must trace to a corpus entry.** If you want to say something the corpus doesn't
support, either drop it or go ask the user and add it to the corpus (with provenance) first —
**do not invent it.**

## How to build the resume

1. **Select.** From the corpus, pull the entries the gap analysis marked as strengths / Met
   must-haves, plus supporting Partial items you can frame honestly. Leave out the irrelevant.
2. **Order.** Lead with what this posting most wants. Put the strongest, most on-target role
   and bullets first.
3. **Write bullets with the XYZ formula.** Each bullet: *accomplished **X**, as measured by
   **Y**, by doing **Z*** — action + quantified result + method. Map from the corpus `x_cv`:
   Action→the verb/X, `metric`→Y (omit Y honestly if `metric` is null), the how→Z.
   - *Example:* corpus story "wrote onboarding checklist, onboarding 3→2 wks" →
     "Cut new-cashier onboarding from 3 weeks to 2 by building a checklist and mentor-pairing."
4. **Mirror the posting's language** for skills/tools the user genuinely has (helps human and
   ATS readers) — but **no keyword stuffing**; only claim real matches.
5. **Tune to the dial** per the table above.
6. **Set the summary/label** to target the role, truthfully.

## Emit two files

- **`resume.json`** — a **standard** JSON Resume (strip all `x_cv`; standard fields only) so it
  validates and works with any JSON Resume theme. Put **internal** build info in the standard
  `meta` object (`version`, `buildTool`, `honestyDial`, `lastModified`) — see the schema doc.
- **`resume.md`** — render `resume.json` to clean, ATS-friendly Markdown per
  `templates/resume-tailored.md` (plain, single-column, no tables/graphics).

## Settings & AI provenance (Enhancement C)

Confirm these with the user (sensible defaults below); they control provenance and the AI-use story.

| setting | default | effect |
|---------|---------|--------|
| `build_credit` | on (neutral) | Optional one-line footer in `resume.md`, e.g. *"Drafted with corpus-vitae, an open-source résumé tool."* Neutral wording only. |
| `show_dial` | **false** | Whether the honesty-dial number is printed. **Keep false.** The dial lives in `resume.json` `meta.honestyDial` for the user's own tracking; printing "Honesty: 6" reads badly to a recruiter (implies other versions are less honest). |
| `ai_narrative` | off (opt-in) | Whether to include the "I build real products with AI" story (see below). |
| `audience` | traditional | `ai-forward` vs `traditional` — gates how prominently `ai_narrative` appears. |

### The AI-use narrative (the honest framing that matters)

Do **not** frame anything as "this résumé was written by AI" — that invites "he had AI lie for
him." Frame it as **the candidate builds real products with AI**, with corpus-vitae itself as the
proof: an AI-assisted product *whose entire point is enforcing honesty*. That's a flex, not a
confession. When `ai_narrative` is on, source it from `x_cv.narrative` and surface it as:

- a **`projects` entry** in `resume.json` for **corpus-vitae** — what it does, that the user built
  it (AI-assisted), and the anti-fabrication design — honest, concrete, evidence-backed; and/or
- a **cover-letter element** (the natural home when `audience: traditional`).

Gate by audience: for `ai-forward` employers, the résumé projects entry is a genuine differentiator;
for `traditional` ones, prefer keeping it to the cover narrative so framing/context is easier.
Never overstate — describe what was actually built (cite the real corpus story), same honesty floor
as everything else.

## Flag every stretch for the user to approve

Wherever the dial led you to round or aggressively reframe, **flag it** so the user
consciously signs off. Present flags alongside `resume.md` (don't bury them in the file), e.g.:

- `⚠️ rounded: "led team of 12" ← corpus says "co-led with the assistant manager". Defensible?`
- `⚠️ formalized title: "Scheduling Coordinator (informal)" ← "handled the schedule". OK?`

For each flag, note the risk and let the user confirm, soften, or cut. Then regenerate.

## Definition of done

- `resume.json` is valid standard JSON Resume (no `x_cv`); `resume.md` renders cleanly.
- Every claim traces to a corpus entry; nothing on the do-not-claim list appears.
- No fabricated employer/date/degree/cert/metric at any dial setting.
- All rounded/reframed claims were flagged and approved by the user.

**Apply is out of scope.** Hand the user the finished resume and stop. Do not submit, send, or
post anything.
