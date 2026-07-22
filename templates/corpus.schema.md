# Corpus schema — JSON Resume + the `x_cv` extension

The knowledge base `data/kb/corpus.json` is a **[JSON Resume](https://jsonresume.org/)**
document (so it interoperates with the whole JSON Resume ecosystem) **plus** a documented
`x_cv` extension that holds the richer facts-&-stories metadata JSON Resume doesn't model.

Two rules keep interop intact:

1. **The corpus keeps `x_cv`.** It is our working superset.
2. **A tailored resume strips `x_cv`** and emits only standard JSON Resume, so it validates
   against the official schema and renders with any JSON Resume theme. See stage 7.

## Standard JSON Resume sections we use

`basics`, `work`, `education`, `projects`, `skills`, `certificates`, `awards`, `volunteer`,
`languages`, `interests`. (Others in the spec — `publications`, `references` — are allowed if
relevant.) Use standard JSON Resume field names exactly (`name`, `label`, `email`, `summary`,
`highlights`, `startDate`/`endDate` as `YYYY-MM-DD` or `YYYY-MM`, etc.) so output stays valid.

## The `x_cv` extension

Two placements:

- **Top-level `x_cv`** — metadata about the corpus itself.
- **Per-entry `x_cv`** — attached inside any `work` / `project` / `education` / `volunteer`
  item (and usable elsewhere) to carry the story + provenance for that entry.
- **`x_cv.stories[]`** (top-level) — atomic stories that don't belong to a single standard
  entry; each may `link` to one by `id`.
- **`x_cv.narrative`** (top-level) — the story/disposition layer from Stage 2.5 (see below).

### Per-entry `x_cv` fields

| field | type | meaning |
|-------|------|---------|
| `star` | object | `{ situation, task, action, result }` — the story behind the entry. Fill what you have; leave blanks rather than inventing. |
| `metric` | string \| null | The real, quantified outcome (e.g. "cut load time 40%"). **`null` if the user gave no number — never fabricate one.** |
| `competencies` | string[] | Tags from: `leadership, teamwork, problem-solving, communication, adaptability, initiative, execution, technical-depth`. |
| `provenance` | enum | `user-stated` \| `on-old-resume` \| `verifiable`. How we know this. |
| `confidence` | number | 0–1. How sure we are the claim is accurate/defensible. |
| `tags` | string[] | Freeform themes for retrieval when tailoring. |

Give each `work`/`project`/story entry a stable `id` (kebab-case slug) so stages 6–7 and
`x_cv.stories[].link` can reference it.

## Example `corpus.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
  "basics": {
    "name": "Jordan Rivera",
    "label": "Retail Team Lead",
    "email": "jordan@example.com",
    "phone": "",
    "location": { "city": "Austin", "region": "TX" },
    "summary": "Retail team lead who moved from cashier to shift supervisor in 18 months."
  },
  "work": [
    {
      "id": "citymart-supervisor",
      "name": "CityMart",
      "position": "Shift Supervisor",
      "startDate": "2023-02",
      "endDate": "",
      "summary": "Runs front-of-store operations for a 12-person shift.",
      "highlights": [
        "Trained 6 new cashiers and cut onboarding time from 3 weeks to 2."
      ],
      "x_cv": {
        "star": {
          "situation": "New hires took ~3 weeks to work a register unsupervised.",
          "task": "Asked by store manager to speed up cashier onboarding.",
          "action": "Wrote a one-page checklist and paired each new hire with a mentor.",
          "result": "Onboarding dropped to ~2 weeks; fewer register errors."
        },
        "metric": "onboarding 3 wks -> 2 wks (~33% faster)",
        "competencies": ["leadership", "initiative", "communication"],
        "provenance": "user-stated",
        "confidence": 0.9,
        "tags": ["training", "process-improvement", "retail-ops"]
      }
    }
  ],
  "education": [],
  "skills": [
    { "name": "POS systems", "level": "", "keywords": ["Square", "cash handling"] }
  ],
  "certificates": [],
  "interests": [
    { "name": "Community gardening", "keywords": ["volunteer-organizing"] }
  ],
  "x_cv": {
    "schemaVersion": "1.0",
    "generator": "corpus-vitae",
    "stories": [
      {
        "id": "gm-food-drive",
        "link": null,
        "star": {
          "situation": "Neighborhood food bank was short volunteers before a holiday.",
          "task": "Volunteered to coordinate a weekend drive.",
          "action": "Recruited 15 neighbors and organized pickup routes.",
          "result": "Collected ~800 lbs of food in one weekend."
        },
        "metric": "~800 lbs collected, 15 volunteers",
        "competencies": ["leadership", "communication"],
        "provenance": "user-stated",
        "confidence": 0.85,
        "tags": ["volunteering", "organizing"]
      }
    ]
  }
}
```

### Top-level `x_cv.narrative` (Stage 2.5)

The disposition/trajectory layer — corpus-level, not tied to one entry. Every element must be
**evidence-backed** via `evidence_links` (ids of corpus stories), so it can't drift into opinion.

```json
"narrative": {
  "growth_arc": "1-3 sentence arc (hired with X -> grew into Y -> now Z).",
  "learning_agility": ["evidence-backed examples of learning fast in the unfamiliar"],
  "differentiators": ["what they do better than peers, each pointing at evidence"],
  "operating_principles": ["reusable rules/heuristics + origin"],
  "motivation": "what drives them and why",
  "evidence_links": ["corpus story/entry ids backing the above"]
}
```
See `references/02b-narrative-interview.md`. Feeds `basics.summary`, capability-fit (stage 6),
and the AI/portfolio + cover narrative (stage 7).

## Tailored-resume `meta` (standard JSON Resume field; internal build info)

JSON Resume defines a top-level **`meta`** object. Use it on a tailored `resume.json` to hold
**internal** build provenance — never printed on the résumé body:

```json
"meta": {
  "version": "corpus-vitae v1.x",
  "buildTool": "corpus-vitae",
  "honestyDial": 6,
  "lastModified": "YYYY-MM-DD"
}
```
The **`honestyDial` value stays internal** (for the user's own tracking); it is not rendered into
`resume.md`. An optional, neutral build-credit footer may appear in `resume.md` (no dial number) —
see `references/07-tailoring.md` (Enhancement C settings).

## Working with the corpus

- **Read → parse JSON → edit → write back.** Always keep it valid JSON. When adding an entry
  mid-interview, append to the right section and fill `x_cv` from what the user actually said.
- **Never invent `metric` or dates.** Empty/`null` is honest; a fabricated number is not.
- **Provenance discipline:** things pulled from the old resume are `on-old-resume`; things the
  user tells you in the interview are `user-stated`; things with documentation are
  `verifiable`. Stage 7 uses this to decide what it may safely assert.
