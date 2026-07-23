#!/usr/bin/env python3
"""
setup.py — one-shot environment bootstrap for the résumé renderer (Stage 8).

Creates a local, gitignored `.venv` and installs the two rendering deps (python-docx, reportlab)
so `scripts/render_resume.py` can produce the ATS-safe PDF + DOCX. Safe to re-run: if the venv is
already good, it just says so. Stdlib only (it has to run before anything is installed).

    python scripts/setup.py

If the system Python lacks pip/ensurepip, this bootstraps pip via the official get-pip.py
(one network download). If it can't finish (no network, locked-down box), the skill still works —
you just get the Markdown résumé instead of PDF/DOCX.
"""
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VENV = REPO / ".venv"
REQ = REPO / "scripts" / "requirements.txt"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"
DEPS_CHECK = "import docx, reportlab"  # python-docx imports as `docx`


def venv_python(venv=VENV):
    return venv / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], **kw)


def deps_ok(py):
    return py.exists() and run([py, "-c", DEPS_CHECK], capture_output=True).returncode == 0


def pip_ok(py):
    return run([py, "-m", "pip", "--version"], capture_output=True).returncode == 0


def bootstrap_pip(py):
    """Install pip into the venv via get-pip.py when ensurepip is unavailable."""
    print("  · pip missing in the venv — bootstrapping via get-pip.py …")
    try:
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td) / "get-pip.py"
            req = urllib.request.Request(GET_PIP_URL, headers={"User-Agent": "corpus-vitae-setup"})
            with urllib.request.urlopen(req, timeout=60) as r:
                dest.write_bytes(r.read())
            return run([py, dest]).returncode == 0
    except Exception as e:
        print(f"  · couldn't bootstrap pip: {e}")
        return False


def main():
    if not REQ.exists():
        print(f"! expected {REQ} — are you running this from the repo root?")
        return 1

    py = venv_python()
    if deps_ok(py):
        print(f"✓ Renderer already set up ({VENV}). Nothing to do.")
        return 0

    print(f"Setting up the résumé renderer in {VENV} …")

    # 1) create the venv (with pip if ensurepip is available, else without)
    if not py.exists():
        if run([sys.executable, "-m", "venv", VENV], capture_output=True).returncode != 0:
            print("  · venv+pip failed; creating venv without pip, will bootstrap pip next …")
            if run([sys.executable, "-m", "venv", "--without-pip", VENV]).returncode != 0:
                print("! Could not create a virtual environment. The skill still works — you'll get "
                      "the Markdown résumé; PDF/DOCX just won't render on this machine.")
                return 1

    # 2) ensure pip
    if not pip_ok(py) and not bootstrap_pip(py):
        print("! Could not get pip working in the venv. Skill still works (Markdown résumé); "
              "PDF/DOCX won't render here.")
        return 1

    # 3) install deps
    print("  · installing python-docx + reportlab …")
    if run([py, "-m", "pip", "install", "-q", "-r", REQ]).returncode != 0:
        print("! Dependency install failed. Skill still works (Markdown résumé); PDF/DOCX won't "
              "render here.")
        return 1

    # 4) verify
    if not deps_ok(py):
        print("! Installed, but the deps don't import cleanly. Falling back to Markdown for PDF/DOCX.")
        return 1

    print(f"✓ Done. Stage 8 can now render PDF + DOCX with:\n"
          f"    {venv_python()} scripts/render_resume.py <resume.json>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
