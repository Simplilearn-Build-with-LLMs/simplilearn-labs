# Lab 02: Retail Returns — Demonstrations and Worked Reasoning (Module 2)

Test how choosing in-context demonstrations and adding worked reasoning help an LLM apply a returns policy to tricky tickets (delivery dates, item condition, missing receipts). One controlled experiment: zero-shot vs. convenience few-shot vs. selected few-shot vs. worked reasoning, scored on accuracy, per-label F1, run-to-run stability and token cost.

## Files
| File | What it is |
|---|---|
| `Module_2_ICL_Returns_Guided_Practice.ipynb` | The lab notebook. The return policy, demonstration pool, dev and eval tickets are inside it. |

## Before you start
1. If this is your first session, do the one-time setup in the repo's `README.md`. You can skip the notebook's Task 1: the repo's `.venv` and `.env` already cover it.
2. Run cell 1 of `START_HERE.ipynb` to make sure you have the latest version.
3. Open the notebook, check the kernel (top right) says **.venv**, and run the cells in order.

Tasks 2–5 fit in one class session. Task 6 (the final evaluation, 360 API calls) runs on its own; start it and come back. Model: `gpt-4.1-mini`; the whole lab should cost well under a dollar. Run results are saved to `results/`, which git ignores.
