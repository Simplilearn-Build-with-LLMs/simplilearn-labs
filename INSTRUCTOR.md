# Instructor guide

This repo is **public**: anything pushed to any branch is visible to everyone. Keep unreleased labs and solutions somewhere else (your own machine or a private repo).

## Release a lab (about 2 days before the session)

1. Create the folder with the naming pattern `labNN_short_name/` (for example `lab03_rag_basics/`). The `lab` prefix and two-digit number keep folders in order and are how `sync.py --reset NN` finds them.
2. Put in it: the notebook, a short `README.md`, and any `data/` files.
3. Clear notebook outputs before committing:
   ```
   jupyter nbconvert --clear-output --inplace labNN_*/*.ipynb
   ```
4. Update the schedule table in the root `README.md`.
5. Commit and push to `main`.
6. If the lab needs new packages, add them to the root `requirements.txt` (and to `REQUIRED_IMPORTS` in `sync.py` if it's a new import). Students get them on their next sync.

## Fix a lab during or before class

Edit, clear outputs, commit, push. Then tell students: **run `python sync.py`, then *File > Reload Notebook from Disk*.**

- Students who haven't touched the file get the fix silently.
- Students who already changed it get the fix, and their version is saved as `*.my-copy-MMDD-HHMM.ipynb` next to it.

Small fixes are easiest for students if you keep cell order stable.

## API key

`.env` is in the repo **without** a key (just a commented placeholder), so every student already has the file. Students fill it in once via `START_HERE.ipynb`; `sync.py` always keeps the student's copy.

**Do this once in your own clone**, so your real key can never be committed by `git add -A`:
```
git update-index --skip-worktree .env
```
(To change the placeholder later: `git update-index --no-skip-worktree .env`, edit, commit, then turn it back on.)

- Never commit the key. GitHub scans public repos and providers such as OpenAI revoke leaked keys automatically, which would break every student's lab at once.
- Share it in the live session or the LMS, never in the repo.
- If the virtual lab environment can set `OPENAI_API_KEY` as an environment variable for everyone, that's even simpler: students skip the key step.
- Use a project-scoped key with a spending limit and rotate it after each cohort.

## Repo layout

```
simplilearn-labs/
├── README.md            student guide + lab schedule
├── INSTRUCTOR.md        this file
├── START_HERE.ipynb     every session: sync. One time: save key, check setup
├── sync.py              safe "git pull" for students (backs up their changes)
├── requirements.txt     packages for all labs
├── .env                 key placeholder; students fill it in once
└── labNN_short_name/    one folder per released lab
```
