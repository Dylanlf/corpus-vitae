#!/usr/bin/env python3
"""
fill_plan.py — turn profile.json into a REVIEWABLE application "fill plan" before any browser action.

Part of the optional, opt-in autofill step (Stage 10, `references/12-autofill.md`). It never touches a
browser or submits anything — it just maps the user's stored bio to standard application fields and
sorts each into:
  • AUTO-FILL   — factual, safe to enter once the user says go (name, contact, links, work auth …)
  • ASK FIRST   — sensitive; only with explicit opt-in (compensation, voluntary EEO self-ID)
  • YOUR INPUT  — blanks we can't fill + a reminder that custom/knockout questions are surfaced live
The user reviews this plan first (review-first, pause-before-submit), then the browser step fills only
the AUTO-FILL rows (+ anything they approve). Submitting is always the human's click.

Usage:
  python scripts/fill_plan.py --user dylan
  python scripts/fill_plan.py --user dylan --target whatnot-head-of-data   # reads apply_url, writes fill-plan.md
"""
import argparse
import json
import os
import re


def load_json(path):
    with open(path) as f:
        return json.load(f)


def g(d, *keys, default=""):
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k)
        if d is None:
            return default
    return d


def yn(v):
    if v is True:
        return "Yes"
    if v is False:
        return "No"
    return ""


def joined_name(ident):
    parts = [g(ident, "first_name"), g(ident, "middle_name"), g(ident, "last_name")]
    return " ".join(p for p in parts if p).strip()


def location_str(loc):
    if g(loc, "display"):
        return g(loc, "display")
    bits = [g(loc, "city"), g(loc, "region"), g(loc, "country")]
    return ", ".join(b for b in bits if b)


def apply_url_from_target(user_dir, target):
    posting = os.path.join(user_dir, "targets", target, "posting.md")
    if not os.path.exists(posting):
        return ""
    for line in open(posting):
        m = re.match(r"\s*-\s*apply_url:\s*(\S+)", line)
        if m and m.group(1) not in ('""', "''"):
            return m.group(1)
    # fall back to source_url only if no apply_url
    for line in open(posting):
        m = re.match(r"\s*-\s*source_url:\s*(\S+)", line)
        if m:
            return m.group(1) + "  (source_url — no company apply_url captured)"
    return ""


def build_plan(profile, apply_url):
    ident = profile.get("identity", {})
    contact = profile.get("contact", {})
    loc = profile.get("location", {})
    links = profile.get("links", {})
    elig = profile.get("work_eligibility", {})
    js = profile.get("job_search", {})
    comp = profile.get("compensation", {})
    eeo = profile.get("voluntary_self_id", {})

    # (label, value) — factual fields; blanks are routed to "your input"
    factual = [
        ("Full legal name", joined_name(ident)),
        ("Preferred name", g(ident, "preferred_name")),
        ("Pronouns", g(ident, "pronouns")),
        ("Email", g(contact, "email")),
        ("Phone", g(contact, "phone")),
        ("Location", location_str(loc)),
        ("Willing to relocate", yn(loc.get("willing_to_relocate"))),
        ("Work arrangement", ", ".join(loc.get("work_arrangement_pref", []) or [])),
        ("LinkedIn", g(links, "linkedin")),
        ("GitHub", g(links, "github")),
        ("Portfolio / website", g(links, "portfolio") or g(contact, "personal_website")),
        ("Work authorization", g(elig, "work_authorization")),
        ("Needs visa sponsorship (now/future)",
         yn(elig.get("requires_sponsorship_now_or_in_future",
                     elig.get("requires_visa_sponsorship"))),),
        ("Available start date", g(js, "available_start_date")),
        ("Notice period (weeks)", str(js.get("notice_period_weeks") or "") if js.get("notice_period_weeks") is not None else ""),
        ("References available on request", yn(profile.get("application_misc", {}).get("reference_available_on_request"))),
    ]
    auto = [(l, v) for l, v in factual if v not in ("", None)]
    need = [l for l, v in factual if v in ("", None)]

    # sensitive — only with explicit opt-in
    sensitive = []
    cur = g(js, "search_status")
    if comp.get("desired_total_min") or comp.get("desired_base_min"):
        cyc = g(comp, "currency", default="USD")
        parts = []
        if comp.get("desired_total_min"):
            parts.append(f"total ≥ {cyc} {comp['desired_total_min']:,}")
        if comp.get("desired_base_min"):
            parts.append(f"base ≥ {cyc} {comp['desired_base_min']:,}")
        sensitive.append(("Desired compensation", "; ".join(parts) + " — enter only if the form asks AND you approve; never volunteer"))
    if any(eeo.get(k) for k in ("gender", "race_ethnicity", "veteran_status", "disability_status")) or eeo.get("hispanic_or_latino") is not None:
        sensitive.append(("Voluntary EEO self-ID", "values on file — fill only if you opted in; 'Decline to self-identify' is always valid"))
    else:
        sensitive.append(("Voluntary EEO self-ID", "not provided → leave blank / 'Decline to self-identify' (voluntary)"))

    return auto, sensitive, need, cur


def render(profile, apply_url, auto, sensitive, need, search_status):
    name = joined_name(profile.get("identity", {})) or "(name)"
    L = [f"# Application fill plan — {name}", ""]
    if apply_url:
        L += [f"**Apply at:** {apply_url}", ""]
    if search_status == "passive":
        L += ["> Passive search — if this is a confidential job hunt, double-check the employer isn't your current one before applying.", ""]
    L += ["> **Review-first.** The autofill step enters only the AUTO-FILL rows below (plus anything you",
          "> approve), attaches your résumé, then **stops for you to review and click submit**. It never",
          "> submits, creates accounts, enters passwords, or solves CAPTCHAs — those are handed back to you.",
          ""]
    L += ["## ✅ Auto-fill (factual — safe once you say go)", "", "| Field | Value |", "|---|---|"]
    L += [f"| {l} | {v} |" for l, v in auto]
    L += ["", "## ⚠️ Ask first (sensitive — explicit opt-in only)", "", "| Field | Handling |", "|---|---|"]
    L += [f"| {l} | {v} |" for l, v in sensitive]
    L += ["", "## ✍️ You'll answer live (we can't prefill)", ""]
    if need:
        L += ["Blank in your profile — you'll fill these (or update your profile first):",
              "", *[f"- {l}" for l in need], ""]
    L += ["Plus any **custom / knockout / screening questions** the form asks (sponsorship phrasing,",
          "years-of-experience gates, 'why this company', scenario prompts). These are surfaced live for",
          "you — **never guessed** — because a wrong knockout answer auto-rejects you.", ""]
    return "\n".join(L).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=None)
    ap.add_argument("--user-dir", default=None)
    ap.add_argument("--target", default=None, help="target slug under data/<user>/targets/ (for apply_url + output)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    user_dir = a.user_dir or (f"data/{a.user}" if a.user else None)
    if not user_dir:
        ap.error("provide --user NAME or --user-dir PATH")
    ppath = os.path.join(user_dir, "profile.json")
    if not os.path.exists(ppath):
        ap.error(f"no profile at {ppath} — capture it in Stage 0 first (template: templates/profile.example.json)")
    profile = load_json(ppath)

    apply_url = apply_url_from_target(user_dir, a.target) if a.target else ""
    auto, sensitive, need, search_status = build_plan(profile, apply_url)
    out_md = render(profile, apply_url, auto, sensitive, need, search_status)

    out = a.out or (os.path.join(user_dir, "targets", a.target, "fill-plan.md") if a.target else None)
    if out:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            f.write(out_md)
        print(f"fill plan → {out}  [{len(auto)} auto-fill, {len(sensitive)} sensitive, {len(need)} to-answer]")
    else:
        print(out_md)


if __name__ == "__main__":
    main()
