#!/usr/bin/env python3
"""Get the newest labs and any fixes. Safe to run as often as you like.

Easiest: run cell 1 of START_HERE.ipynb (it runs  %run sync.py  with the .venv kernel).
From a terminal, use the .venv Python so packages land in the right place:
    .venv/bin/python sync.py              (Mac)
    .venv\\Scripts\\python sync.py          (Windows)
    ... sync.py --reset 01                (fresh copy of Lab 01; your copy is backed up)

What it does
- New lab folders appear in the file browser on the left.
- If the instructor fixed a file you have NOT changed, you get the fix.
- If the instructor fixed a file you HAVE changed (for example a notebook you
  ran), your version is saved next to it as  <name>.my-copy-MMDD-HHMM.ipynb
  and the fixed version takes its place. Nothing of yours is deleted.
- Your .env (API key), your own new files and results/ folders are never touched.
"""
import argparse
import datetime
import hashlib
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = "main"
PROTECTED = {".env"}   # student copies always win; never backed up or replaced
# pip package name -> import name, used to spot missing packages
REQUIRED_IMPORTS = {"openai": "openai", "python-dotenv": "dotenv", "pandas": "pandas",
                    "matplotlib": "matplotlib"}


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit(f"[sync] git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r.stdout


def split_z(out):
    return [p for p in out.split("\0") if p]


def local_changes():
    """Return (modified_tracked, untracked) as sets of repo-relative paths."""
    out = git("status", "--porcelain=v1", "-z", "--untracked-files=all")
    modified, untracked = set(), set()
    entries = split_z(out)
    i = 0
    while i < len(entries):
        code, path = entries[i][:2], entries[i][3:]
        if code[0] in "RC":          # rename/copy entries carry an extra path
            i += 1
        if code == "??":
            untracked.add(path)
        elif "D" not in code:        # deleted files simply come back
            modified.add(path)
        i += 1
    return modified, untracked


def backup(rel):
    src = ROOT / rel
    stamp = datetime.datetime.now().strftime("%m%d-%H%M")
    dst = src.with_name(f"{src.stem}.my-copy-{stamp}{src.suffix}")
    n = 2
    while dst.exists():
        dst = src.with_name(f"{src.stem}.my-copy-{stamp}-{n}{src.suffix}")
        n += 1
    shutil.copy2(src, dst)
    return dst.relative_to(ROOT).as_posix()


def lab_folders():
    return sorted(p.name for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("lab"))


def ensure_packages():
    req = ROOT / "requirements.txt"
    if not req.exists():
        return
    stamp_file = ROOT / ".labsync_requirements"
    digest = hashlib.sha256(req.read_bytes() + sys.executable.encode()).hexdigest()
    missing = [pkg for pkg, mod in REQUIRED_IMPORTS.items() if importlib.util.find_spec(mod) is None]
    if not missing and stamp_file.exists() and stamp_file.read_text() == digest:
        return
    print("[sync] Installing / updating Python packages (one time, about a minute)...")
    cmd = [sys.executable, "-m", "pip", "install", "-q", "-r", str(req)]
    # No virtual environment needed: each student has their own lab machine.
    # Try a normal install, then a user install, then allow it on "externally managed" Pythons.
    for extra in ([], ["--user"], ["--user", "--break-system-packages"]):
        if subprocess.run(cmd + extra).returncode == 0:
            break
    else:
        print("[sync] Could not install packages automatically. Run:  pip install -r requirements.txt")
        return
    stamp_file.write_text(digest)
    if missing:
        print("[sync] Packages installed. If a notebook is already open, restart its kernel.")


def main():
    ap = argparse.ArgumentParser(description="Get the newest labs and fixes.")
    ap.add_argument("--reset", metavar="LAB",
                    help="restore a fresh copy of one lab, e.g. --reset 02 (your files are backed up)")
    args = ap.parse_args()

    if shutil.which("git") is None:
        raise SystemExit("[sync] git is not installed in this environment. Ask your instructor.")
    if not (ROOT / ".git").exists():
        raise SystemExit(f"[sync] {ROOT} is not a cloned copy of the labs repo. See README.md.")

    before = set(lab_folders())
    git("fetch", "--quiet", "origin", BRANCH)
    upstream = set(split_z(git("diff", "--name-only", "-z", "HEAD", f"origin/{BRANCH}")))
    modified, untracked = local_changes()

    reset_prefix = None
    if args.reset:
        num = args.reset.strip().lower().removeprefix("lab").zfill(2)
        matches = [f for f in lab_folders() if f.startswith(f"lab{num}")]
        if not matches:
            raise SystemExit(f"[sync] No lab folder found for '{args.reset}'. Labs: {', '.join(lab_folders())}")
        reset_prefix = matches[0] + "/"

    backups, keep = [], {}
    for path in sorted(modified):
        if path in PROTECTED:
            keep[path] = (ROOT / path).read_bytes()
        elif path in upstream or (reset_prefix and path.startswith(reset_prefix)):
            backups.append(backup(path))      # instructor changed it too -> keep a copy, take the fix
        else:
            keep[path] = (ROOT / path).read_bytes()   # only you changed it -> keep yours
    for path in sorted((untracked & upstream) - PROTECTED):
        backups.append(backup(path))          # a new instructor file has the same name as yours

    git("reset", "--quiet", "--hard", f"origin/{BRANCH}")
    for path, data in keep.items():
        (ROOT / path).write_bytes(data)

    new_labs = sorted(set(lab_folders()) - before)
    updated = sorted(p for p in upstream - PROTECTED
                     if (ROOT / p).exists() and p.split("/")[0] not in new_labs)

    if new_labs:
        print("[sync] New lab(s):", ", ".join(new_labs))
    if updated:
        print("[sync] Updated files:")
        for p in updated:
            print("   ", p)
    if backups:
        print("[sync] Your previous versions were saved as:")
        for p in backups:
            print("   ", p)
        print("[sync] If one of these notebooks is open: File > Reload Notebook from Disk.")
    if not (new_labs or updated or backups):
        print("[sync] Already up to date.")

    ensure_packages()
    print("[sync] Done. Labs available:", ", ".join(lab_folders()) or "(none yet)")


if __name__ == "__main__":
    main()
