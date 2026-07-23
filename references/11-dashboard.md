# At-a-glance dashboard

A local, self-contained HTML view of **best-fits-today**, generated from the index (`index.db`).
Personal data stays on the machine — the page makes no external requests and embeds only the user's
own data. Read-only snapshot; interactions are edited via the skill/CLI (append to `interactions.jsonl`),
not the page.

## Generate
```
python scripts/build_index.py --user <user>       # refresh the index from the JSONL files
python scripts/build_dashboard.py --user <user>    # → data/<user>/dashboard.html
```
Open `data/<user>/dashboard.html` in a browser.

## What it shows (per row, ranked by capability×desire)
- **Role** (deep-links to the posting) + **company** with sector + employee count + location. When an
  **`apply_url`** (the company's own site / ATS posting) is present, link the role there — that's where
  you'd actually apply — and keep the `source_url` as a secondary "where we found it" link.
- **Fit** — capability/10 (the "can you do the real job" score), with literal fit + desire and a
  **screening-risk** badge (from Stage-6 two-layer scoring / `fit.jsonl`).
- **Salary** — the posting range if given, else the **BLS occupation market median [p25–p75]** (labeled
  "mkt" so it's clearly a national occupation benchmark, not a company figure).
- **Signal** — `reposted N× · open Nd` (ghost-job/hard-to-fill) and `seen N×` (times ingested).
- **Company intel** — deep-link pointers (Glassdoor / Levels / Indeed / Comparably / LinkedIn) and an
  award/best-places search pointer. Never scraped values — links only.
- **Status** — application status chip or a 👍 like.

Ranking excludes disliked/hidden jobs and those already applied/rejected/withdrawn; reposts collapse to
the initial listing.

## Honesty notes (shown on the page too)
- Read-only snapshot; a spare-time work in progress — verify everything.
- Salary benchmark is occupation-level national context, not a company-specific offer.
- Ratings/awards are links to the source, not data we collected or endorse.

## Theming
The page is theme-aware (`prefers-color-scheme` + a `data-theme` override) and responsive (the table
scrolls horizontally inside its own container). Uses a restrained neutral palette (see the `dataviz`
skill for the design system). Everything is inline — no external CSS/JS/fonts.
