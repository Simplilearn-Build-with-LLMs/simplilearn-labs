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

Works whether you used  git clone  or  Code > Download ZIP  (no Git needed).
"""
import argparse
import datetime
import hashlib
import importlib.util
import io
import json
import os
import shutil
import ssl
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = "main"
REPO = "Simplilearn-Build-with-LLMs/simplilearn-labs"
ZIP_URL = os.environ.get("LABSYNC_ZIP_URL",
                         f"https://codeload.github.com/{REPO}/zip/refs/heads/{BRANCH}")
MANIFEST = ROOT / ".labsync_manifest.json"   # what each file looked like at the last sync
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


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sync_git(reset_prefix):
    """Repo was cloned with git: fetch, back up conflicting edits, fast-forward."""
    git("fetch", "--quiet", "origin", BRANCH)
    upstream = set(split_z(git("diff", "--name-only", "-z", "HEAD", f"origin/{BRANCH}")))
    modified, untracked = local_changes()

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
    updated = sorted(p for p in upstream - PROTECTED if (ROOT / p).exists())
    return updated, backups


def download_zip():
    ctx = None
    try:
        import certifi                        # installed with openai; fixes Mac certificate errors
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    try:
        with urllib.request.urlopen(ZIP_URL, timeout=60, context=ctx) as r:
            return zipfile.ZipFile(io.BytesIO(r.read()))
    except Exception as e:
        raise SystemExit(f"[sync] Could not download the labs ({e}). Check your internet connection and try again.")


def sync_zip(reset_prefix):
    """Repo came from Download ZIP: compare with GitHub file by file, no git needed."""
    zf = download_zip()
    try:
        manifest = json.loads(MANIFEST.read_text())
    except (OSError, ValueError):
        manifest = {}

    updated, backups, new_manifest = [], [], {}
    for info in zf.infolist():
        if info.is_dir() or "/" not in info.filename:
            continue
        rel = info.filename.split("/", 1)[1]      # strip the "simplilearn-labs-main/" prefix
        if not rel:
            continue
        data = zf.read(info)
        up = sha(data)
        new_manifest[rel] = up
        local = ROOT / rel
        if local.exists():
            if rel in PROTECTED:
                continue                          # never touch the student's .env
            mine = sha(local.read_bytes())
            if mine == up:
                continue                          # already identical
            base = manifest.get(rel)
            in_reset = bool(reset_prefix and rel.startswith(reset_prefix))
            if base == up and not in_reset:
                continue                          # only the student changed it -> keep theirs
            if base != mine or in_reset:
                backups.append(backup(rel))       # student changed it (or we can't tell) -> keep a copy
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_bytes(data)
        updated.append(rel)
    MANIFEST.write_text(json.dumps(new_manifest, indent=0))
    return sorted(updated), backups


def main():
    ap = argparse.ArgumentParser(description="Get the newest labs and fixes.")
    ap.add_argument("--reset", metavar="LAB",
                    help="restore a fresh copy of one lab, e.g. --reset 02 (your files are backed up)")
    args = ap.parse_args()

    reset_prefix = None
    if args.reset:
        num = args.reset.strip().lower().removeprefix("lab").zfill(2)
        matches = [f for f in lab_folders() if f.startswith(f"lab{num}")]
        if not matches:
            raise SystemExit(f"[sync] No lab folder found for '{args.reset}'. Labs: {', '.join(lab_folders())}")
        reset_prefix = matches[0] + "/"

    before = set(lab_folders())
    if (ROOT / ".git").exists() and shutil.which("git"):
        updated, backups = sync_git(reset_prefix)
    else:
        updated, backups = sync_zip(reset_prefix)

    new_labs = sorted(set(lab_folders()) - before)
    updated = [p for p in updated if p.split("/")[0] not in new_labs]

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
        print("[sync] If one of these notebooks is open, close it and open it again.")
    if not (new_labs or updated or backups):
        print("[sync] Already up to date.")

    ensure_packages()
    print("[sync] Done. Labs available:", ", ".join(lab_folders()) or "(none yet)")


if __name__ == "__main__":
    main()
