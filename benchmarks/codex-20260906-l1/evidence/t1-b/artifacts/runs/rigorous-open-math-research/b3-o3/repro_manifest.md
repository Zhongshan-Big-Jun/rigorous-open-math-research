# Reproducibility manifest

- Task: frozen B3 O3 root count, source TASK.md.
- Run: R-20260907T015148Z-B3-O3.
- Initial observed start: 2026-09-07T01:51:48Z.
- Latest resume reconciliation: 2026-09-07T07:06:27.716527+00:00.
- Wall-clock timestamps advanced across interruption; the user's latest shared
  remaining budget (1261 seconds) is authoritative. No inactive gap is treated
  as fresh research time.
- Python: 3.14.4 (/usr/bin/python3).
- Lean executable on PATH: None.
- Lake executable on PATH: None.
- Matrix, polynomial, signs, and boundary formulas were derived exactly by
  hand in the proof. No numerical scan, randomized search, or symbolic
  software result is used as a premise.
- Independent reviewer: /root/completion_auditor; audit PASS saved in completion_audit.json. The interrupted audit produced no result; the same
  outstanding task was resumed, not treated as a passed audit.

## Input and proof hashes

| Artifact | SHA-256 |
| --- | --- |
| TASK.md | 1fa717b9a5f195c42ecca97d51e20327cb4eb2c316c936c054f55f7dd7416f16 |
| PROMPT.md | bdc8d34d7fbb149d9d2c03c9f0c452605cdb3d7c3931e09ddd28cffabfb5802d |
| problem_contract.md | 60293062bebe70a64528f097590fbff5b13556afde62641f6a8644b11a165f9c |
| candidate_proof.md | 4a1fcc46e20b8ac122f68a391ec49628cfc4b749427f3891c08b329ab3d25b29 |
| obligation_graph.json | 7ab98b7664c36cd5f2e407d3236aabdb52f846f240bb4e417a64595c8a763c8a |
| completion_manifest.json | a56e7ea8aa052d9d84fd4bb666ed83033b57e8496a93239564f558ddac8757c3 |
| lean-proof/B3O3.lean | 94d4087c2aeefdcb1b0a8bead152b87d84fcc36a3cc07ff777c5fb5bbd80aeb3 |

## Restrictions and process decisions

Installed skills: math-research-workflow 1.15.0,
rigorous-open-math-research 1.12.0, manage-math-research-program 1.8.1,
lean-verify 1.6.0. These supplied procedure only; mathematical sources are the
statement and derivations in this run.

Repository inspection, git history/status/fetch/commit/push, other projects,
prior solutions, memory, sessions, and all internet/literature retrieval were
forbidden by the user and not performed. The skill's config-inspecting doctor
was not run because its scope exceeds the permitted statement/workspace
inputs. Loaded skill files and the installed workspace-only pipeline validator
were accessible. No plugin repair or installation was attempted.

The pipeline validator was run without --check-git. Its initial packet-format
failure concerned missing bold field markup; this was repaired, with no
mathematical source change. Pre-audit gate then passed. Exact command:

    python3 -B /home/huangzy/codex-benchmark/L1-20260906-ASTRA-ABC-r1/t1/b/home/plugins/cache/math-research/math-research-workflow/1.15.0/scripts/validate_pipeline.py --project .

No formal build was run. Eight explicit proof holes remain in the unverified
Lean statement scaffold. The natural-language proof is independent of this
scaffold. No formal verification or novelty claim is made.

Final deterministic gate: exit 0, zero errors and zero warnings, using
--gate-status CANDIDATE_COMPLETE_PROOF,INDEPENDENTLY_AUDITED_PROOF.
Log: pipeline_gate.log. An earlier field-format failure is preserved in
pipeline_gate.initial.log. The final answer export prepends the exact
matrix definitions from the audited TASK.md to the unchanged frozen proof.
