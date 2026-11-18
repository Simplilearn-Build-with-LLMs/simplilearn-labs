# Lab 03 B: Ask the Manual

Build an assistant that answers questions about the Quillbrew QB-500 manuals. It retrieves a passage first, answers only from that passage, and says IDK when the passage does not contain the answer. Then compare that passage index with a second index made of customer-style questions.

## Files
| File | What it is |
|---|---|
| `ask_the_manual.ipynb` | The lab notebook. |
| `lab_data/` | Five manuals, the golden questions, and a saved question checkpoint. |

## Before you start
1. If this is your first session, do the one-time setup in the repo's `README.md`.
2. Run cell 1 of `START_HERE.ipynb` to make sure you have the latest version.
3. Open this notebook, check the kernel (top right) says **.venv**, and run the cells in order. `lab_data` sits beside the notebook.

In 6.1, write your own unanswerable question. Model: `gpt-4.1-mini`. Do not paste your API key into the notebook.
