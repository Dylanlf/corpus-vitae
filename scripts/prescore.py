#!/usr/bin/env python3
"""
prescore.py — fast, offline HEURISTIC fit over every ingested job, so the dashboard can rank the
whole store. This is a TRIAGE sort, not real fit: capability ≈ overlap of your corpus skills/tags
vs the JD; desire ≈ match to goals directions (minus avoid-terms); screening-risk ≈ simple knockout
checks. Rows are tagged `method:heuristic` and shown as "rough" on the dashboard. The expensive
Stage-6 two-layer analysis (`method:analyzed`) is the real score and overrides the heuristic.

Appends to data/<user>/fit.jsonl; SKIPS any job that already has an `analyzed` score. Stdlib only.

Usage:  python prescore.py --user dylan
        python prescore.py --shared data/_shared --user-dir data/dylan
"""
import argparse, datetime, hashlib, json, os, re


def load_jsonl(path):
    if not path or not os.path.exists(path):
        return []
    out = []
    for line in open(path):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def corpus_vocab(corpus):
    """Lowercased skill/tag phrases that signal capability."""
    v = set()
    for g in corpus.get("skills", []) or []:
        if g.get("name"):
            v.add(g["name"].lower())
        for kw in g.get("keywords", []) or []:
            v.add(kw.lower())
    xcv = corpus.get("x_cv", {}) or {}
    for s in xcv.get("stories", []) or []:
        for t in s.get("tags", []) or []:
            v.add(t.lower().replace("-", " "))
        for c in s.get("competencies", []) or []:
            v.add(c.lower().replace("-", " "))
    # clean: drop very short/noisy terms and parenthetical notes
    cleaned = set()
    for t in v:
        t = re.sub(r"\(.*?\)", "", t).strip()
        t = re.sub(r"\s+", " ", t)
        if len(t) >= 3 and t not in ("etc", "the", "and"):
            cleaned.add(t)
    return cleaned


def has_advanced_degree(corpus):
    for e in corpus.get("education", []) or []:
        st = (e.get("studyType") or "").lower()
        if any(k in st for k in ("master", "m.s", "msc", "phd", "ph.d", "doctor", "mba")):
            return True
    return False


STOP = set("the and for with your you our are was will who this that from role team work data "
           "job company are role roles per within across into their its has have who what when".split())


def goals_terms(goals_md):
    """Rough desire signals from goals.md: direction keywords (+) and avoid terms (-)."""
    plus, minus = set(), set()
    if not goals_md:
        return plus, minus
    lines = goals_md.splitlines()
    in_dir = False
    for ln in lines:
        low = ln.lower()
        if low.startswith("##"):
            in_dir = ("candidate direction" in low or "positioning" in low or "appetite" in low
                      or "alternative path" in low)
            continue
        toks = re.findall(r"[a-z][a-z0-9/+-]{3,}", low)
        if "avoid" in low or "dealbreak" in low or "drain" in low:
            minus.update(t for t in toks if t not in STOP)
        elif in_dir:
            plus.update(t for t in toks if t not in STOP)
    return plus, minus


def score_job(job, vocab, adv_degree, plus, minus):
    jd = (job.get("title", "") + "  " + job.get("body", "")).lower()
    title = job.get("title", "").lower()

    # capability: distinct corpus skill/tag phrases present in the JD (word-boundary), diminishing returns
    matched = 0
    for term in vocab:
        pat = r"\b" + re.escape(term) + r"\b"
        if re.search(pat, jd):
            matched += 1
    capability = round(10 * (1 - 0.85 ** matched), 1)

    # desire: neutral 5, +2 if a direction keyword hits the title, -3 if an avoid term appears in the JD
    desire = 5.0
    if plus and any(re.search(r"\b" + re.escape(p) + r"\b", title) for p in plus):
        desire += 2
    if minus and any(re.search(r"\b" + re.escape(m) + r"\b", jd) for m in minus):
        desire -= 3
    desire = max(1.0, min(9.0, desire))

    # screening-risk: crude knockout detection
    risk = "low"
    degree_req = re.search(r"(ph\.?d|doctorate|master'?s?|graduate degree)\b[^.]{0,40}(require|must|need)", jd) \
        or re.search(r"(require|must have|minimum)[^.]{0,40}(ph\.?d|doctorate|master'?s? degree)", jd)
    yrs = [int(m) for m in re.findall(r"(\d{1,2})\+?\s*years", jd)]
    maxyrs = max(yrs) if yrs else 0
    if degree_req and not adv_degree:
        risk = "high"
    elif maxyrs >= 10:
        risk = "med"
    # literal fit is not meaningfully estimable by heuristic — leave null; capability is the triage signal
    return {"literal_fit": None, "capability_fit": capability, "desire": desire,
            "screening_risk": risk, "matched_skills": matched}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=None)
    ap.add_argument("--shared", default=None); ap.add_argument("--user-dir", default=None)
    a = ap.parse_args()
    shared = a.shared or "data/_shared"
    user_dir = a.user_dir or (f"data/{a.user}" if a.user else None)
    if not user_dir:
        ap.error("provide --user NAME or --user-dir PATH")

    corpus = {}
    cpath = os.path.join(user_dir, "kb", "corpus.json")
    if os.path.exists(cpath):
        corpus = json.load(open(cpath))
    else:
        print(f"warning: no corpus at {cpath} — capability will be ~0 for everything.")
    goals_md = ""
    gpath = os.path.join(user_dir, "goals.md")
    if os.path.exists(gpath):
        goals_md = open(gpath).read()
    corpus_hash = hashlib.blake2b(json.dumps(corpus, sort_keys=True).encode(), digest_size=8).hexdigest()

    vocab = corpus_vocab(corpus)
    adv = has_advanced_degree(corpus)
    plus, minus = goals_terms(goals_md)

    # collapse jobs.jsonl → latest record per job_key
    jobs = {}
    for e in load_jsonl(os.path.join(shared, "jobs.jsonl")):
        k = e.get("job_key")
        if k and (k not in jobs or e.get("ingested_at", "") >= jobs[k].get("ingested_at", "")):
            jobs[k] = e

    fit_path = os.path.join(user_dir, "fit.jsonl")
    existing = load_jsonl(fit_path)
    analyzed = {r["job_key"] for r in existing if r.get("method") == "analyzed"}
    # already scored under the CURRENT corpus (heuristic or analyzed) → skip; re-score only if corpus changed
    fresh = {r["job_key"] for r in existing if r.get("corpus_hash") == corpus_hash}
    skip = analyzed | fresh

    ts = datetime.date.today().isoformat()
    added = 0
    os.makedirs(user_dir, exist_ok=True)
    with open(fit_path, "a") as f:
        for k, job in jobs.items():
            if k in skip:
                continue  # never override an analyzed score; don't duplicate a fresh heuristic
            s = score_job(job, vocab, adv, plus, minus)
            row = {"job_key": k, "literal_fit": s["literal_fit"], "capability_fit": s["capability_fit"],
                   "desire": s["desire"], "screening_risk": s["screening_risk"],
                   "method": "heuristic", "matched_skills": s["matched_skills"],
                   "corpus_hash": corpus_hash, "ts": ts}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            added += 1
    print(f"pre-scored {added} job(s) (heuristic) → {fit_path}  "
          f"[vocab={len(vocab)} terms, adv_degree={adv}, skipped {len(skip)} already-fresh "
          f"({len(analyzed)} analyzed)]")


if __name__ == "__main__":
    main()
