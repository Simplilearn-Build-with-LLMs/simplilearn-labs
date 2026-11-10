# Building with LLMs — Labs

All 8 lab notebooks for the course live here. Each lab appears in this repo about **two days before its live session**, as a new folder.

## Before the setup session: install three things

| | Windows | Mac |
|---|---|---|
| **Python 3.12** | [python.org/downloads](https://www.python.org/downloads/) → find **3.12** → *Windows installer (64-bit)*. On the first screen, **tick "Add python.exe to PATH"**. | [python.org/downloads](https://www.python.org/downloads/) → find **3.12** → *macOS 64-bit universal2 installer*. |
| **Git** | [git-scm.com/downloads/win](https://git-scm.com/downloads/win) → keep all default options. | Open **Terminal**, run `git --version`, click **Install** when asked (10–20 minutes). |
| **VS Code** | [code.visualstudio.com](https://code.visualstudio.com/) | [code.visualstudio.com](https://code.visualstudio.com/) |

Then open VS Code → Extensions (left sidebar) → install **Python** and **Jupyter** (both by Microsoft). Restart VS Code once everything is installed.

## One-time setup (setup session)

**1. Clone the repo.** In VS Code: *Terminal > New Terminal*, then:

```
git clone https://github.com/Simplilearn-Build-with-LLMs/simplilearn-labs.git
cd simplilearn-labs
```

**2. Create the virtual environment and install packages.**

| Windows (PowerShell) | Mac |
|---|---|
| `py -3.12 -m venv .venv` | `python3.12 -m venv .venv` |
| `.venv\Scripts\python -m pip install -r requirements.txt` | `.venv/bin/python -m pip install -r requirements.txt` |

**3. Open the folder:** *File > Open Folder* → select `simplilearn-labs`.

**4. Open `START_HERE.ipynb`.** Click **Select Kernel** (top right) → *Python Environments* → **.venv**. Then run the three cells (Shift + Enter):

- Cell 1 → `Done. Labs available: ...`
- Cell 2 → paste the course API key from the chat → `Saved to .env`
- Cell 3 → `Ready.`

That's it. You won't need to set anything up again.

## Every session

Open the `simplilearn-labs` folder in VS Code, open `START_HERE.ipynb` and **run cell 1**. New labs appear as new folders. Open today's notebook and make sure the kernel (top right) says **.venv**.

**If the instructor fixes a notebook during class**, run cell 1 again, then reload the notebook (VS Code will ask, or close and reopen it). If you had already changed that notebook, your version is saved next to it as `<name>.my-copy-MMDD-HHMM.ipynb`, so nothing is lost.

Prefer the terminal? `.venv\Scripts\python sync.py` (Windows) or `.venv/bin/python sync.py` (Mac). Want a clean copy of a lab? Add `--reset 01`.

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
| `python`, `py` or `git` "not recognized" / "command not found" | Close and reopen VS Code after installing. Windows: re-run the Python installer → *Modify* → tick *Add to PATH*. |
| `python3.12: command not found` (Mac) | Python 3.12 isn't installed yet. Install it from python.org (above). |
| `ModuleNotFoundError` | The kernel isn't **.venv**. Click the kernel name (top right) → *Python Environments* → **.venv**. |
| VS Code asks to install `ipykernel` | Click **Install**, or redo step 2 above. |
| `AuthenticationError` / 401 | Run cell 2 in `START_HERE.ipynb` again, then restart the kernel. |
| `not a cloned copy of the labs repo` | Use `git clone` (step 1), not *Download ZIP*. |
| `destination path 'simplilearn-labs' already exists` | You already cloned it. Run `cd simplilearn-labs` and continue. |

The key lives in the `.env` file at the repo root. `sync.py` never overwrites it. Never paste the key into a notebook or share your `.env`.
