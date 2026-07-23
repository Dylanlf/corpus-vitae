#!/usr/bin/env python3
"""
build_dashboard.py — render a local, self-contained, theme-aware HTML dashboard from index.db.

Reads data/<user>/index.db (built by build_index.py) and writes data/<user>/dashboard.html — a
read-only "best-fits-today" snapshot: ranked by capability×desire, with salary (posting or BLS
benchmark), company sector/size, ghost-job/repost signal, rating/award deep-links, and status.
Personal data stays local (no external requests; nothing embedded but the user's own data).
Interactions are edited via the skill/CLI, not this page. Stdlib only.

Usage:  python build_dashboard.py --user dylan
        python build_dashboard.py --db data/dylan/index.db --out data/dylan/dashboard.html
"""
import argparse, datetime, html, json, os, sqlite3


def esc(x):
    return html.escape(str(x if x is not None else ""))


def money(v):
    try:
        return "$" + format(int(float(v)), ",")
    except Exception:
        return esc(v) if v else ""


def salary_cell(job, bench):
    if job.get("salary_raw"):
        return esc(job["salary_raw"])
    b = bench or {}
    if b.get("median"):
        lo, hi = money(b.get("p25")), money(b.get("p75"))
        rng = f" <span class='muted'>[{lo}–{hi}]</span>" if lo and hi else ""
        return f"{money(b['median'])}{rng} <span class='muted'>· mkt</span>"
    return "<span class='muted'>—</span>"


def fit_cell(job):
    cap, lit, des = job.get("capability_fit"), job.get("literal_fit"), job.get("desire")
    if cap is None and lit is None:
        return "<span class='muted'>not scored</span>"
    risk = (job.get("screening_risk") or "").lower()
    rk = {"high": "risk-high", "med": "risk-med", "medium": "risk-med", "low": "risk-low"}.get(risk, "")
    badge = f"<span class='badge {rk}'>screen: {esc(job.get('screening_risk'))}</span>" if risk else ""
    heuristic = job.get("method") == "heuristic"
    approx = "~" if heuristic else ""
    rough = "<span class='badge' title='rough heuristic triage — not the deep Stage-6 score'>rough</span>" if heuristic else ""
    lit_txt = "–" if lit is None else esc(lit)  # heuristic leaves literal fit blank on purpose
    return (f"<b>{approx}{esc(cap if cap is not None else '–')}</b><span class='muted'>/10 cap</span> "
            f"<span class='muted'>· lit {lit_txt} · want {esc(des if des is not None else '–')}</span> {badge} {rough}")


def signal_cell(job):
    bits = []
    rc = job.get("repost_count") or 0
    if rc:
        d = job.get("days_open")
        bits.append(f"<span class='badge warn'>reposted {rc}×{(' · open ' + str(d) + 'd') if d not in ('', None) else ''}</span>")
    if (job.get("times_seen") or 0) > 1:
        bits.append(f"<span class='muted'>seen {job['times_seen']}×</span>")
    return " ".join(bits) or "<span class='muted'>—</span>"


def links_cell(rating_links, awards):
    out = []
    for k in ("glassdoor", "levels", "indeed", "comparably", "linkedin"):
        u = (rating_links or {}).get(k)
        if u:
            out.append(f"<a href='{esc(u)}' target='_blank' rel='noopener'>{esc(k)}</a>")
    for a in (awards or []):
        if a.get("url"):
            out.append(f"<a href='{esc(a['url'])}' target='_blank' rel='noopener' title='{esc(a.get('name',''))}'>award?</a>")
    return " · ".join(out) or "<span class='muted'>—</span>"


CSS = """
:root{--bg:#fff;--fg:#1a1a1a;--muted:#6b7280;--line:#e5e7eb;--card:#fafafa;--accent:#1f3a5f;--warn:#b45309;--hi:#b91c1c;--lo:#15803d}
@media(prefers-color-scheme:dark){:root{--bg:#0f1114;--fg:#e5e7eb;--muted:#9aa4b2;--line:#232833;--card:#151922;--accent:#8fb3e0;--warn:#f59e0b;--hi:#f87171;--lo:#4ade80}}
:root[data-theme=dark]{--bg:#0f1114;--fg:#e5e7eb;--muted:#9aa4b2;--line:#232833;--card:#151922;--accent:#8fb3e0;--warn:#f59e0b;--hi:#f87171;--lo:#4ade80}
:root[data-theme=light]{--bg:#fff;--fg:#1a1a1a;--muted:#6b7280;--line:#e5e7eb;--card:#fafafa;--accent:#1f3a5f;--warn:#b45309;--hi:#b91c1c;--lo:#15803d}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:24px}
h1{font-size:20px;margin:0 0 2px}.sub{color:var(--muted);font-size:13px;margin-bottom:14px}
.note{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;color:var(--muted);font-size:12px;margin-bottom:16px}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;min-width:820px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);position:sticky;top:0;background:var(--bg)}
tr:last-child td{border-bottom:none}
.title{font-weight:600}.title a{color:var(--fg);text-decoration:none}.title a:hover{text-decoration:underline}
.co{color:var(--muted);font-size:12px}
.muted{color:var(--muted);font-size:12px}
a{color:var(--accent)}
.badge{display:inline-block;font-size:11px;padding:1px 6px;border-radius:10px;border:1px solid var(--line)}
.warn{color:var(--warn);border-color:var(--warn)}
.risk-high{color:var(--hi);border-color:var(--hi)}.risk-med{color:var(--warn);border-color:var(--warn)}.risk-low{color:var(--lo);border-color:var(--lo)}
.dim{opacity:.5}
.st{font-size:11px;padding:1px 6px;border-radius:10px;border:1px solid var(--accent);color:var(--accent)}
"""


def build(db_path, out_path, user):
    db = sqlite3.connect(db_path); db.row_factory = sqlite3.Row
    rows = db.execute("""
      SELECT j.*, c.sector, c.employees, c.salary_benchmark, c.rating_links, c.award_pointers,
             f.literal_fit, f.capability_fit, f.desire, f.screening_risk, f.method,
             i.rating, i.status
      FROM jobs j
      LEFT JOIN companies c ON c.company_key = j.company_key
      LEFT JOIN fit f ON f.job_key = j.job_key
      LEFT JOIN interactions i ON i.job_key = j.job_key
    """).fetchall()
    jobs = [dict(r) for r in rows]
    # rank: capability*desire desc, then last_seen desc; drop reposts (show only the initial of a cluster)
    for j in jobs:
        cap = j.get("capability_fit") or 0; des = j.get("desire") or 0
        j["_score"] = (cap * des) if (cap and des) else (cap or 0)
    visible = [j for j in jobs if not j.get("is_repost")]
    hidden_states = {"applied", "rejected", "withdrawn"}
    best = [j for j in visible if (j.get("rating") not in ("dislike", "hide")) and (j.get("status") not in hidden_states)]
    best.sort(key=lambda j: (j["_score"], j.get("last_seen", "")), reverse=True)

    trs = []
    for j in best:
        bench = json.loads(j.get("salary_benchmark") or "{}")
        rlinks = json.loads(j.get("rating_links") or "{}")
        awards = json.loads(j.get("award_pointers") or "[]")
        co = esc(j.get("company", ""))
        meta = " · ".join(x for x in (esc(j.get("sector", "")), (f"{esc(j.get('employees'))} emp" if j.get("employees") else "")) if x)
        _link = j.get("apply_url") or j.get("url")  # prefer the company/ATS apply link
        title_html = (f"<a href='{esc(_link)}' target='_blank' rel='noopener'>{esc(j['title'])}</a>"
                      if _link else esc(j["title"]))
        status = f"<span class='st'>{esc(j['status'])}</span>" if j.get("status") else (
                 "👍" if j.get("rating") == "like" else "")
        trs.append(f"<tr><td class='title'>{title_html}<div class='co'>{co}{(' · ' + meta) if meta else ''} "
                   f"· {esc(j.get('location',''))}</div></td>"
                   f"<td>{fit_cell(j)}</td><td>{salary_cell(j, bench)}</td>"
                   f"<td>{signal_cell(j)}</td><td class='muted'>{links_cell(rlinks, awards)}</td>"
                   f"<td>{status}</td></tr>")
    db.close()
    today = datetime.date.today().isoformat()
    doc = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Job market — {esc(user)}</title>
<style>{CSS}</style></head><body><div class=wrap>
<h1>Job market — {esc(user)}</h1>
<div class=sub>Best fits today · {len(best)} shown ({len(jobs)} jobs in store) · generated {today}</div>
<div class=note><b>Read-only snapshot.</b> Ranked by capability×desire (your corpus). Salary shows the
posting range, else the BLS occupation <i>market</i> median [p25–p75] (national — context, not a
company-specific figure). Ratings/awards are <b>deep links</b> to the source (never scraped). Reposts
are collapsed to the initial listing; "reposted N×" is a ghost-job/hard-to-fill signal. A spare-time
work in progress — verify everything.</div>
<div class=tablewrap><table>
<thead><tr><th>Role</th><th>Fit</th><th>Salary</th><th>Signal</th><th>Company intel (links)</th><th>Status</th></tr></thead>
<tbody>{''.join(trs) or '<tr><td colspan=6 class=muted>No jobs yet — fetch some with scripts/fetch_jobs.py, then rebuild the index.</td></tr>'}</tbody>
</table></div>
<div class=sub style='margin-top:14px'>corpus-vitae dashboard · data stays local under data/{esc(user)}/</div>
</div></body></html>"""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    open(out_path, "w").write(doc)
    print(f"wrote {out_path} ({len(best)} best-fit rows of {len(jobs)} jobs)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=None)
    ap.add_argument("--db", default=None); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    db = a.db or (f"data/{a.user}/index.db" if a.user else None)
    if not db:
        ap.error("provide --user NAME or --db PATH")
    out = a.out or os.path.join(os.path.dirname(db), "dashboard.html")
    build(db, out, a.user or "user")


if __name__ == "__main__":
    main()
