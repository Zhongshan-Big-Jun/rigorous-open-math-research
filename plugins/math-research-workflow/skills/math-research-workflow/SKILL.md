---
name: math-research-workflow
description: >-
  Orchestrate the full mathematics research pipeline: program management
  (manage-math-research-program) to rigorous problem research
  (rigorous-open-math-research) to Lean formal verification (lean-verify),
  with sub-agent division of labor, artifact handoff contracts, hash binding,
  and automatic git sync at every stage boundary. Use when the user asks to
  run or manage a complete research+verification workflow for a mathematics
  project, to iterate the three-skill pipeline, or to coordinate parallel
  solve/audit/formalize agents. 中文触发: 数学项目全流程一体化 (管理-研究-验证),
  三个 skill 协同工作流, 研究+Lean 形式化验证流水线, 子 agent 分工优化.
---

# Math Research Workflow (管理-研究-验证一体化流水线)

## Purpose

This skill is the **orchestration layer** for the three-skill pipeline. It
sequences, delegates, and hands off work between:

- `$manage-math-research-program` -- program context, task packets, tool
  library, accepted knowledge, git sync (stage A);
- `$rigorous-open-math-research` -- theorem contracts, routes, adversarial
  proof audit, candidate proofs (stage B);
- `$lean-verify` -- Lean 4 formalization, machine checks, obligation-level
  audit, structured verdicts (stage C).

It never re-implements any of their workflows. Its only job is to decide
**what** runs **when**, **by whom** (sub-agents), and to enforce the **handoff
contract** between stages.

## Dependency direction

```text
math-research-workflow -> manage-math-research-program -> rigorous-open-math-research
math-research-workflow -> lean-verify
```

No reverse calls. Each referenced skill keeps its own hard boundaries (see
`manage-math-research-program` "Hard non-overlap rule").

## Trigger boundary

Use this skill when the user asks to:

- run a complete research program end to end (manage -> solve -> verify);
- formalize a batch of already-proved results into Lean and verify them;
- coordinate several sub-agents (solve / audit / formalize / verify) on one
  project with a shared task packet;
- sync a mathematics project repository (git) across research sessions;
- resume or checkpoint a multi-stage research pipeline.

Do **not** use this skill for a single proof request (use
`$rigorous-open-math-research`), a single formalization audit (use
`$lean-verify`), or project bookkeeping only (use
`$manage-math-research-program`).

## Pipeline protocol

### Stage A -- Program (manager)

1. Read the project entry point (`AGENTS.md` if present), `lean-proof/STATUS.md`
   (formalization matrix) and the program index produced by
   `manage-math-research-program`.
2. Run the git-sync check (manage skill section 0): record dirty files,
   ahead/behind, current commit hash.
3. Run the deterministic pipeline gate shipped with this plugin
   (`scripts/validate_pipeline.py --project .`). Fix every hard `FAIL` before
   dispatch; treat `warn:` lines as advisory notes to record, not as blockers.
4. For each task: build or refresh the **task packet** (contract, source
   documents, obligations, verification criteria, hashes) and delegate.

### Stage B -- Research (solver)

For every concrete problem in the packet, invoke `$rigorous-open-math-research`
with the exact contract. Its run artifacts (`problem_contract.md`,
`candidate_proof.md`, `audit_report.md`, `reproducibility/`, ...) are produced
in a per-run directory and ingested by reference (never rewritten by the
manager).

**Sub-agent division (efficiency):**

- **Solver agent**: builds routes, derives, records ledger entries.
- **Adversarial audit agent**: independently re-derives each obligation and
  attacks the candidate proof; reports F-xxx findings.
- The two alternate in bounded loops until either `CANDIDATE_COMPLETE_PROOF`
  or an exact gap report is reached. The audit agent never shares a chain of
  thought with the solver; only artifacts are exchanged.

### Stage C -- Verification (formalizer)

For every result labeled `已证` / `CANDIDATE_COMPLETE_PROOF` that the user
wants formalized:

1. Create/update the Lean project (`lean-proof/`), map each obligation to a
   `.lean` declaration (obligation map O1..On).
2. **Formalizer agent** writes the Lean files; **verifier agent** runs
   `verify_lean_project.py --project . --build` (sorry/axiom scan + lake
   build) and refreshes `run-manifest.json`.
3. Write/extend `audit_report.md` (per-obligation fidelity) and
   `verification.json` (structured verdict), then update `STATUS.md` and
   `README.md`. Fix source-document errors found in the process in place and
   record them as F-xxx in the audit report (do not silently change sources).
4. Machine evidence required: build exit 0, zero sorry/admit/axiom hits,
   obligation map complete. No machine evidence => no "FORMALLY_VERIFIED".

### Stage boundary checks (mandatory)

- A -> B: packet contains contract + source paths + obligation list; no open
  questions left unresolved.
- B -> C: only results with an honest status label (`已证`, not numerical
  evidence) enter formalization; numerical/猜想 results are excluded and
  recorded as such.
- C -> done: verification.json verdict, audit report, STATUS matrix updated;
  git synced; AGENTS.md session log appended.
- Every dispatch and every stage close re-runs
  `scripts/validate_pipeline.py`; a hard `FAIL` must not be left open at a
  stage boundary. Statuses outside the formalization gate are reported as
  warnings, never silently promoted.

## Efficiency rules

- Parallelize where dependencies allow: stage B's audit agent may review
  obligations while the solver opens the next route; stage C's verifier may
  scan files as the formalizer writes them.
- Reuse before redo: check the tool library (`tools/`), the accepted-knowledge
  base, and `STATUS.md` before starting a route or a formalization; hash-bound
  artifacts prevent duplicate work.
- One artifact per claim: never maintain two copies of a proof state; the
  manager records paths and hashes verbatim.
- Automatic git sync after every stage (manage skill section 0). If the user
  has a fork topology (parent repo + personal fork), sync the child fork by
  pushing to the parent first, then updating the fork, and state the direction
  in the session log.

## Reference files

- `references/workflow-design.md` -- full design: roles, handoff schemas,
  parallelism, checklists, and failure handling.
- `assets/pipeline-handoff.template.md` -- handoff record template.
- `scripts/validate_pipeline.py` -- deterministic task-packet, hash-binding,
  run-manifest, and git gate checks for stage boundaries.

## Changelog (2026-08-13)

- Added a deterministic stage gate (`scripts/validate_pipeline.py`): required
  task-packet fields, unfilled-template placeholder detection, task-type enum,
  source-bundle and run-manifest hash bindings, lean-proof input hashes, optional
  git cleanliness check, and a formalization gate (`已证` /
  `CANDIDATE_COMPLETE_PROOF`) that reports non-gate statuses as warnings.
- Stage A and the stage-boundary checks now require the gate to run; hard `FAIL`
  findings must be resolved before dispatch or stage close.
- CI smoke fixtures and runners live under `tests/` in the repository root.
