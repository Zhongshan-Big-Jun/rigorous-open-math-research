# Implementation tracking: OpenProver token-conscious absorption

Date: 2026-08-16
Scope: absorb OpenProver (arXiv:2607.09217) strengths into the skill repo with
explicit token-budget control and pause/handoff/resume semantics.

## Features implemented

| # | Feature | Where | Verification |
| --- | --- | --- | --- |
| 1 | Planner action protocol (compact CoT + action list) | `math-research-workflow/references/openprover-absorption.md` + Stage B | doc + validate_all |
| 2 | Repository item system (repo/ + repo_index.md, verified-items-only) | openprover-absorption.md + Stage B | doc + validate_all |
| 3 | `theorem.lean` input skeleton | openprover-absorption.md + manage task packet | doc + validate_all |
| 4 | Planner history (planner_history.jsonl, sliding window) | openprover-absorption.md + Stage B | doc + validate_all |
| 5 | Token budget discipline (budget_state.json, pause+handoff+resume, extension) | openprover-absorption.md + manage + rigorous phase-12 | doc + validate_all |
| 6 | `assets/budget-state.template.json` | manage assets | JSON parse (validate_all) |
| 7 | Stage B section wired into workflow SKILL.md | workflow | validate_all + smoke |
| 8 | Task packet optional `theorem.lean` / `budget` fields | manage SKILL.md | validate_all |
| 9 | Ingest step for `budget_state.json` | manage SKILL.md | validate_all |
| 10 | rigorous Phase 12 budget-exhaustion paragraph | rigorous phase-12-reporting.md | validate_all |
| 11 | Cachebusters bumped (rigorous/manage/workflow) | plugin.json | validate_all |
| 12 | README (zh/en) version history updated | README.md / README_EN.md | validate_all |

## Verification performed

| Check | Result |
| --- | --- |
| Parent `validate_all.py` (68 checks) | PASS |
| Parent smoke tests (doctor, formalization, handoff, lean_verify, pipeline_gate, sync_remotes, whiteboard) | ALL PASS (7) |
| `scaffold_result.py` temp run (scaffold + STATUS + progress + audit) | PASS |
| `index_lean_lemmas.py` temp run (LEMMA_INDEX generation) | PASS |
| `budget-state.template.json` JSON parse | PASS (via validate_all) |

## Bugs found and fixed

- None blocking. Two design notes recorded:
  - `index_lean_lemmas.py` marks a whole file `SCAFFOLD` if it contains any
    `sorry`/`admit`/`axiom`, even if it also contains proven declarations. This
    is a conservative reuse-index heuristic; a per-declaration status would need
    a Lean-aware parser (future work).
  - The token-budget engine is currently a protocol/template (docs + JSON),
    not a compiled CLI. Runtime enforcement depends on agents following the
    pause+handoff discipline documented in `openprover-absorption.md` and
    phase-12.

## Post-sync DSH verification

| Check | Result |
| --- | --- |
| DSH `validate_all.py` (51 checks) | PASS |
| DSH `dsh-check-bundle.py` | BUNDLE OK |
| DSH smoke tests (11) | ALL PASS |
| DSH `package.json` | bump 0.1.10 -> 0.1.11 |
| Push to all remotes (parent origin+fork, DSH origin) | done, clean trees |

## How a paused budget resumes

1. On exhaustion, write `budget_state.json` (`status: paused_budget`), an
   interruption handoff, and persist whiteboard/repo/history/facts.
2. `state/RESUME.md` points to the handoff.
3. A later run reads handoff + budget state, adds budget, continues from the
   recorded next action.
4. `request_extension` is used when the target is almost complete.
