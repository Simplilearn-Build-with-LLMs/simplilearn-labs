# Building with LLMs — Virtual Labs

All 8 lab notebooks for the course live here. Each lab appears in this repo about **two days before its live session**, as a new folder on the left.

## One-time setup (first session only)

1. Open a terminal in the virtual lab and clone the repo:
   ```
   git clone https://github.com/Simplilearn-Build-with-LLMs/simplilearn-labs.git
   cd simplilearn-labs
   ```
2. Open `START_HERE.ipynb` and run all three cells. This installs the packages and saves the course API key your instructor gives you in class.

That's it. You won't need to set anything up again.

## Every session

Get the newest labs and any fixes, from the `simplilearn-labs` folder:

```
python sync.py
```

(Or open `START_HERE.ipynb` and run the first cell.) Then open today's lab folder on the left.

**If the instructor fixes a notebook during class**, run `python sync.py` again, then *File > Reload Notebook from Disk*. If you had already changed that notebook, your version is saved next to it as `<name>.my-copy-MMDD-HHMM.ipynb`, so nothing is lost.

Want a clean copy of a lab? `python sync.py --reset 02` (your current files are backed up first).

## Lab schedule

| Lab | Folder | Live session | Status |
|---|---|---|---|
| 01 | [`lab01_brand_voice`](lab01_brand_voice/) | TBD | Available |
| 02 | | TBD | Coming soon |
| 03 | | TBD | Coming soon |
| 04 | | TBD | Coming soon |
| 05 | | TBD | Coming soon |
| 06 | | TBD | Coming soon |
| 07 | | TBD | Coming soon |
| 08 | | TBD | Coming soon |

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Run `python sync.py` (it installs missing packages), then restart the kernel |
| `AuthenticationError` / 401 | Re-run cell 2 in `START_HERE.ipynb`, then restart the kernel |
| `not a cloned copy of the labs repo` | Do the one-time setup above (use `git clone`, not *Download ZIP*) |
| Notebook says the file changed on disk | Choose *Reload*, or *File > Reload Notebook from Disk* |

The key lives in the `.env` file at the repo root (hidden in the file browser). `sync.py` never overwrites it. Never paste the key into a notebook or share your `.env`.
