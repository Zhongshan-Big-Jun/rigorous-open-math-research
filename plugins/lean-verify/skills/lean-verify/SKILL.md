---
name: lean-verify
description: >-
  Verify a Lean 4 formalization of a mathematical theorem with a strict, reproducible audit:
  pin the Lean environment, check statement fidelity against the informal contract, run machine
  checks (lake build, sorry/admit/axiom scan), independently audit every proof obligation, and
  emit a structured verdict plus a hash-bound run manifest. Use when asked to verify, audit, or
  certify a Lean 4 proof, or to check that a formalization faithfully represents a stated theorem.
  中文触发: 适用于 Lean 4 形式化验证, 证明审计, 陈述保真检查, 义务级独立审计,
  sorry/axiom 泄漏检查, 可复现验证报告, 形式化-非形式化一致性核对.
---

# Lean Verify

## 中文使用说明 (摘要)

本 Skill 用于对一个数学定理的 Lean 4 形式化做严格、可复现的验证. 它把验证拆成
机器可执行的部分 (环境固定, lake build, sorry/admit/axiom 扫描) 与需要独立判断的
部分 (陈述保真审计, 义务级独立审计, 引用核验), 最终产出结构化裁决与 hash 绑定的
运行清单.

- 触发场景: Lean 证明验证, 证明审计, 陈述保真检查, 义务级独立审计, 形式化一致性核对.
- 机器验证与独立审计分离: 机器检查证明 "Lean 接受", 独立审计检查 "形式化忠实于原问题".
- 输出必须按 "Output protocol" 的状态标签开头, 未闭合的义务不得标为完成.
- 本 Skill 是验证执行层; 长期项目管理与已接受知识入库由 `$manage-math-research-program` 负责.

## Purpose

Use this skill to certify a Lean 4 formalization of a mathematical statement, or to audit one.
The goal is a verdict that separates four distinct questions that are usually collapsed:

- Does the Lean code compile with a pinned environment and no leaked `sorry`/`admit`/`axiom`?
- Does the Lean statement faithfully represent the informal theorem contract (no silent
  quantifier, hypothesis, definition, or boundary-case change)?
- Is each proof obligation independently supported by a correct argument (not just accepted on
  the authority of the draft author)?
- Is the result reproducible from the recorded inputs, versions, and commands?

Never claim "formally verified" when only some of these hold. Machine acceptance proves the
formal statement, not its fidelity to the original problem, and not its novelty.

## Inputs

- A Lean 4 project directory (`lakefile.*`, `lean-toolchain`) and/or one or more `.lean` files.
- The informal theorem contract: original problem statement, target theorem, hypotheses,
  boundary cases, and completion criteria. When absent, the contract must be reconstructed and
  audited before verification.
- Optional: an obligation list (O1..On) mapping the theorem to its sub-claims; when absent,
  derive one and record the derivation.
- Optional: cited-source files or links for every external result used by the proof.

## Hard rules

1. Machine verification and independent audit are separate passes. A single pass may not
   certify both compilation and fidelity.
2. No `sorry`, `admit`, or undeclared `axiom` in the final artifact. Axioms outside an explicit
   whitelist are failures; each whitelisted axiom must be justified.
3. The Lean statement must be checked line by line against the informal contract. A proof of a
   different statement is not progress.
4. Cited literature must be real and linked. Never fabricate a paper, a citation, a theorem, a
   conclusion, or a compile result. Any claim about what a source proves must be checked against
   the actual source and version.
5. Numerical evidence is evidence, not proof. Label it and separate it from proof-level claims.
6. Record every input, version, command, and hash. A verification that cannot be replayed is
   incomplete.
7. Do not invent run counts, model settings, tool traces, or human interventions. Mark unknown
   fields as unknown.
8. At a resource boundary, report the strongest verified status and the exact remaining gaps.
   Only the completion label is withheld until verification actually closes.

## Scaffold mode

When the input result is partial/structural (e.g. `RIGOROUS_PARTIAL_RESULT`)
or a new result that is not yet a complete proof, the formalizer should create
a **scaffold** rather than run full verification:

1. Write a `.lean` file under `lean-proof/` that states the new declarations
   and open proof obligations. Mark unfinished proof blocks with `sorry` and a
   header comment:
   `-- SCAFFOLD: <result slug> <status> <open obligations>`.
2. If a build is available, run `lake build` and record whether the skeleton
   compiles; a scaffold may contain `sorry`, so a clean build is not required.
3. Do **not** run the full independent audit as if the result were final.
   Record the scaffold in `lean-proof/STATUS.md` / `README.md` /
   `formalization_progress.md` with status `SCAFFOLDED`.
4. A scaffold must never be reported as `FORMALLY_VERIFIED`; only a later full
   verification pass may upgrade it.

## Intermediate verification and supersession

Lean verification is also a research-time instrument, not only a final
certificate. Verify load-bearing intermediate lemmas as soon as they are
stable; a machine-checked intermediate result is a valid checkpoint that helps
the research avoid detours. It may be reported as `MACHINE_ACCEPTED_PENDING_AUDIT`
or `SCAFFOLDED` when the final theorem is still open.

When a later, more advanced result covers an earlier scaffold/partial/verified
result, record the earlier entry as `superseded` with a pointer to the newer
result. Keep the old files and verdicts in history; do not delete them, and do
not present a superseded result as the current state.

## Verification tiers

Use the cheapest tier that answers the current question:

- **Tier 0 - Statement scaffold**: write the declarations with `sorry` proof
  holes and confirm the skeleton parses/compiles. Use this for every new
  result before investing in a full proof.
- **Tier 1 - Machine-checked lemma**: run `lean_verify` on a load-bearing
  lemma or snippet and record a clean machine check for that snippet. Use this
  for intermediate research checkpoints.
- **Tier 2 - Full verification**: complete `lake build`, zero sorry/axiom,
  statement fidelity audit, and independent per-obligation audit. This is
  required only for completion labels (`FORMALLY_VERIFIED`).

## Submission audit

When this skill is used as part of the proof submission audit pipeline
(manage workflow 8e), the output must support an acceptance decision:

1. After machine verification and independent audit, state whether the
   submission is acceptable as `FORMALLY_VERIFIED`, acceptable only as a
   scaffold (`SCAFFOLDED`), or not acceptable (`REPAIRABLE_GAP` /
   `FATAL_GAP` / `VERIFICATION_INCOMPLETE`).
2. Check consistency with the repository state (existing declarations,
   STATUS.md entries, superseded records) and report any duplicate or
   conflicting formalization.
3. Record the audit trail in the submission audit record so the manager can
   apply the "add by rules" stage.

## Coexistence with informal audit

Lean verification is the machine track; it does not replace the informal
(Danus-style) natural-language audit. For a complete delivery, both must pass:

- The informal audit checks semantics, definitions, external citations, and
  proof flow.
- Lean checks the machine-checkable formal statement and proof.
- Conflict rule: an informal gap trumps a passing Lean check; a Lean failure
  trumps a passing informal check; a paper-level failure trumps both.

Record both tracks in the verification matrix of the submission audit
(see `references/dual-track-audit.md` in the rigorous skill).

## Build loop guard

Long-running sessions can get stuck repeatedly running `lake build` and
re-cloning mathlib4, saturating network and CPU. The plugin now guards builds:

- `verify_lean_project.py --build` calls `scripts/lake_build_guard.py --check`
  before starting `lake build` and `--release` afterwards.
- The guard refuses to start a build when:
  - a fresh `.lake/build_guard.lock` exists (a build may already be running),
  - too many build attempts occurred recently
    (default max 5 in 10 minutes).
- If mathlib4 is declared but not present under `.lake/packages/mathlib4`, the
  guard warns to prefer `lake exe cache get` / a single `lake update` over
  repeated cloning.
- If the guard refuses, do NOT bypass it blindly. Stop the runaway session,
  inspect `.lake/build_attempts.log`, use the mathlib cache, and then retry.

## Build robustness

Full `lake build` is heavy and can time out or fail for environmental reasons.
Prefer the cheapest sufficient build:

- Tier 0/1 checks: use `lake env lean <file>` on the specific file instead of
  full `lake build`. `verify_lean_project.py --build --build-targets FILE.lean`
  does exactly that.
- Before building, fetch the mathlib cache once:
  `verify_lean_project.py --build --use-cache` runs `lake exe cache get`.
- Set a realistic timeout with `--build-timeout SECONDS` (default 3600); a
  timeout is recorded as a build failure, never as a success.
- The build guard wraps all of these: it refuses runaway repeated attempts and
  releases its lock after the build (even on failure).

## Workflow

### Phase 0 - Environment and input inventory

1. Record `lean --version`, `lake --version`, the `lean-toolchain` content, and the `lakefile`
   dependencies before any check.
2. Inventory every input: contract file, Lean files, imports, external sources, scripts, and
   their sha256 hashes. Record which inputs are untrusted or unverified.
3. When the run workspace is a git repository, record the commit hash and dirty files.
4. If `lean`/`lake` is not installed, record that machine verification cannot run and continue
   with the static checks and the independent audit; never pretend a build ran.

### Phase 1 - Contract and obligation mapping

1. Normalize the informal contract: objects, definitions, hypotheses, target conclusion,
   quantifiers, boundary and degenerate cases, permitted outcomes, completion criteria.
2. Audit the contract against its source; a proof of the wrong contract is not verification.
3. Map every obligation O1..On to the Lean declarations that discharge it (`theorem`,
   `lemma`, `def`, or `structure` instance). Record the mapping table; obligations without a
   mapping are open obligations.

### Phase 2 - Statement fidelity audit

For each Lean declaration mapped to an obligation:

1. Compare the Lean statement with the contract text: objects, hypotheses, quantifier order,
   constants and their dependencies, definitions, and boundary cases.
2. Flag silent strengthening, weakening, or redefinition. Two definitions that look alike but
   differ in a formula, notation, or hypothesis are different definitions; say so explicitly.
3. Check that imported names refer to the intended objects (same-name collisions across
   libraries).
4. Record the fidelity result per obligation: `FAITHFUL` | `MINOR_PARAPHRASE` | `UNFAITHFUL`.

### Phase 3 - Machine verification

1. Scan all `.lean` files for `sorry`, `admit`, and `axiom` outside the declared whitelist;
   report file and line for each hit.
2. Run the build (typically `lake build`) with the pinned environment; capture the full log and
   the exit code. `#check`/`#eval` probes for the mapped declarations may be added only in a
   scratch file that is excluded from the final artifact.
3. If the build fails, record the first error and its location; the artifact cannot be
   `FORMALLY_VERIFIED` until the build passes.
4. Record the machine results exactly as observed: exit code, error text, scan hits. Do not
   summarize away failures.

**Single structured judgment (gate protocol).** Every machine check emits one
structured judgment - `build_passed`, `sorry_axiom_hits`, `first_error`
(location + error layer) - in the machine-readable verdict; free-text parsing
of build logs is never acceptable as evidence. The judgment separates the two
branches explicitly: a clean build is the *proved* branch, a build failure is
localized counter-evidence (first error + smallest failing claim), never a
vague "did not compile". (Distilled from forge-gates:
https://github.com/jinguanghai/deepseek-harness-forge-plugins.)

**Atomic, bounded, stateless checks.** Run each check in a request-scoped
temporary directory against the pinned environment; the check retains no
proof-state session and no source beyond its own inputs. A check result is a
typed value consumed by the obligation map, so the same check can be composed
into later stages. (Distilled from jacobian lean.check:
https://github.com/morluto/jacobian.)

### Four gates and semantic review

Any edited declaration proposed for acceptance must pass four gates: (1) compile check,
(2) sorry/admit scan, (3) axiom-set check, and (4) a guard that protected statement
signatures did not change since the last approval. After the gates, a human semantic review
confirms the Lean statement still means what the source means; this last check cannot be
delegated to the same LLM that wrote the statement. Any change to an already-approved
statement requires a fresh statement re-audit and a new guard snapshot before proof work
resumes.

### Repair strategy (when the artifact is incomplete)

When the build fails or obligations remain open, repair instead of regenerating from scratch:

- **Statement freeze**: keep the statement signatures fixed while repairing proofs; a statement change is a new audit, not a repair.
- **Sorrifier decomposition**: replace the failing proof block with `sorry`, re-check that the remaining skeleton compiles, extract the failing block as a clean subproblem, and solve it recursively.
- **Error taxonomy first**: classify each failure (statement layer / proof layer / dependency layer / boundary-convention) before fixing; diagnose in the order 判定 -> 分类 -> 定位 -> 修正.
- **Same-gap convergence**: when the same obligation is blocked by the same gap for three
  consecutive repair rounds, stop repairing; record the strongest derivation reached plus the
  exact gap (and the counterexample when one exists) and downgrade the verdict accordingly.
  Infinite repair loops are worse than an honest `REPAIRABLE_GAP`.
- Track every `sorry`; the final artifact must contain none.

### Phase 4 - Independent audit

Perform this pass as a separate role/pass from the formalizer. For each obligation:

1. Re-derive the argument independently; do not accept any step on the authority of the draft,
   a previous audit, or a repair list.
2. Check logical validity, theorem application, missing assumptions, unjustified jumps, and
   whether the Lean proof actually proves the Lean statement.
3. Check every external citation: the source exists, states the needed result, hypotheses match,
   and the result was not used under another name. Unverifiable citations are failures.
4. Check non-circularity: no obligation is discharged by a statement equivalent in strength to
   the target without a new proof.
5. Classify findings and return a verdict from the structured taxonomy (see Output protocol).
6. When a localized defect is found, specify the smallest failing claim and a concrete repair;
   after repair, re-run the affected checks from the changed point onward. The auditor cannot
   self-certify closure of its own repair.

7. Localize the **first** erroneous step (step index or smallest failing claim) for every
   finding and classify its error layer (statement / proof / dependency /
   boundary-convention); do not give vague comments.

### Phase 5 - Structured output and status label

Write three artifacts:

- `verification.json`: the structured verdict (schema in `assets/verification_output.schema.json`).
- `audit_report.md`: the full audit report (template in `assets/lean-audit-report.template.md`).
- `run-manifest.json`: input hashes, environment, commands, observed machine results, and status.

Status labels (first line of any report):

- `SCAFFOLDED` - a Lean scaffold exists for a new/partial result; it may contain
  `sorry` and is not a verified artifact.
- `FORMALLY_VERIFIED` - build passes, no leaked sorry/axiom, statement fidelity audited, and an
  independent audit closes every obligation.
- `MACHINE_ACCEPTED_PENDING_AUDIT` - build passes with no sorry/axiom leak, but fidelity or
  independent audit is not complete.
- `CANDIDATE_VERIFIED` - independent audit passes but machine verification is unavailable or
  incomplete.
- `REPAIRABLE_GAP` - localized defect found and specified, conclusion unaffected.
- `FATAL_GAP` - a required obligation is false, unsupported, or unfaithful.
- `VERIFICATION_INCOMPLETE` - any required check is missing; report what remains.

Falsification-first verdict rule: one obligation refuted by a verified
counterexample or contradiction vetoes the whole verdict (no partial
`FORMALLY_VERIFIED` around a refuted obligation), and obligations whose status
is uncertain never count as passed - all-uncertain means the verdict is not
`FORMALLY_VERIFIED`. (Distilled from Vibe-Mathematics:
https://github.com/ChongCyrus/Vibe-Mathematics.)

Do not present `MACHINE_ACCEPTED_PENDING_AUDIT` as `FORMALLY_VERIFIED`. Do not bury a fatal gap
in a footnote.

## Output protocol

Structured verdict JSON (schema enforced by `assets/verification_output.schema.json`):

```json
{
  "verdict": "SCAFFOLDED | FORMALLY_VERIFIED | MACHINE_ACCEPTED_PENDING_AUDIT | CANDIDATE_VERIFIED | REPAIRABLE_GAP | FATAL_GAP | VERIFICATION_INCOMPLETE",
  "machine": {
    "lean_version": "...",
    "build_passed": true,
    "sorry_axiom_hits": []
  },
  "statement_fidelity": [
    {"obligation": "O1", "result": "FAITHFUL", "notes": "..."}
  ],
  "critical_errors": [{"location": "...", "issue": "..."}],
  "gaps": [{"location": "...", "issue": "..."}],
  "repair_hints": "...",
  "first_error": {"location": "...", "issue": "...", "category": "statement | proof | dependency | boundary-convention"}  // optional field
}
```

Strict rule: a finding list is empty only when the corresponding check found nothing. Any
non-complete verdict must include non-empty `repair_hints`. Aggregate without dropping issues.

## Artifacts

- `problem_contract.md` - normalized contract and completion criteria.
- `obligation_map.md` - obligations to Lean declarations, with fidelity results.
- `machine_check.log` - build log and scan output (raw).
- `verification.json` - structured verdict.
- `audit_report.md` - independent audit with provenance and findings log.
- `run-manifest.json` - hashes, environment, commands, status.

## Anti-patterns

- Claiming "verified" from a passing build alone.
- Trusting `#check` of the theorem name without reading the statement.
- Accepting a citation without checking it exists and states the needed result.
- Treating a Lean proof as settling fidelity or novelty.
- Reporting a repair as independently verified by the same pass that made it.
- Deleting failed checks or build errors from the record.

## Changelog (2026-08-12)

- 新增四道闸 + 人工语义复核 (Phase 3): 编译 / sorry 扫描 / axiom 集 / 陈述守护 + 人确认形式化陈述仍忠于来源; 已批准陈述的修改需重新过审与新 guard 快照.
- 新增修复策略 (Phase 3): 陈述冻结 (修证明不动陈述签名) + sorrifier 分解 (失败块 sorry 化保留骨架, 子问题递归) + 错误分类优先 (判定 -> 分类 -> 定位 -> 修正), 最终 sorry 清零.
- 新增首错定位与错误层分类 (Phase 4): 每个发现定位第一个错误步骤并分类 (陈述/证明/依赖/边界约定); 结构化输出新增可选 first_error 字段 (schema 同步).
- 方法来源: M2F (https://github.com/optsuite/M2F), MechMath sorrifier (https://github.com/MechMath/MechMath-v1), MMAT fl-prover (https://github.com/MechMath/MechMath-agent-team), FaithSieve (https://github.com/TropicalFatFish/anonymous-faithsieve), FormalRx (https://github.com/LARK-AI-Lab/formalrx, arXiv:2607.04655).

## Changelog (2026-08-16, distilled methods round 2)
- Phase 3 机器核查升级: 单一结构化判定 gate 协议 (build_passed/sorry_axiom_hits/
  first_error 进机器可读裁决, 禁止自由文本解析当证据; 干净构建 = proved 分支,
  构建失败 = 局部反证分支, 定位首错 + 最小失败声明; 来自 forge-gates);
  原子/有界/无状态检查 (请求级临时目录 + 固定环境, 不保留会话与源码, 结果作为
  类型化值供义务图消费; 来自 jacobian lean.check).
- 修复策略新增同缺口收敛规则: 同一义务同一缺口连续三轮未修复即停止, 记录最强
  推导 + 精确缺口 (有反例则记录) 并降级裁决 (来自 dsh-rigorquant 三级停止).
- 裁决新增证伪优先规则: 任一义务被已核验反例/矛盾否决即整体否决; 状态不确定的
  义务不得当作通过, 全不确定不得 FORMALLY_VERIFIED (来自 Vibe-Mathematics).

## Changelog (2026-08-16, scaffold mode)
- 新增 Scaffold mode: 部分/结构结果必须先创建 Lean scaffold (声明 + 开放义务 +
  `-- SCAFFOLD` 头注释, 允许 `sorry`), 登记到 STATUS/README/formalization_progress,
  状态 `SCAFFOLDED`, 不得声称 FORMALLY_VERIFIED.
- 输出协议新增 `SCAFFOLDED` 状态.

## Changelog (2026-08-16, intermediate verification + supersession)
- 明确 Lean 验证也是研究途中的校验工具: 承重中间引理尽早验证, 避免走弯路.
- 更先进结果可覆盖旧结果: 旧 scaffold/partial/verified 记录标记 `superseded`
  并指向新结果, 保留历史但不得作为当前状态.

## Changelog (2026-08-16, submission audit)
- 新增 Submission audit 说明: 作为证明文件提交审计流程的一部分时, 输出必须支持
  接受决策 (FORMALLY_VERIFIED / SCAFFOLDED / REPAIRABLE_GAP / FATAL_GAP /
  VERIFICATION_INCOMPLETE), 并检查与仓库状态的一致性.

## Changelog (2026-08-16, verification tiers)
- 新增 Verification tiers: Tier 0 (scaffold skeleton) / Tier 1 (machine-checked
  lemma) / Tier 2 (full FORMALLY_VERIFIED); 使用能满足当前问题的最低档位.

## Changelog (2026-08-16, dual-track audit)
- 新增 Coexistence with informal audit: Lean 是机器轨, 不替代非正式审计; 完整交付
  要求双轨都过, 冲突按 非正式 gap > Lean 通过, Lean 失败 > 非正式通过, 论文级失败
  > 两者 裁决.

## Changelog (2026-08-16, build loop guard)
- 新增 `scripts/lake_build_guard.py` + `verify_lean_project.py` 集成: 防止会话
  反复 `lake build` / 反复 clone mathlib4 占满网络/CPU; 检查 fresh lock 与近期
  构建次数, 并提示优先 `lake exe cache get` 而非重复克隆.
- 构建鲁棒性增强: `verify_lean_project.py --build` 支持
  `--build-targets` (单文件 `lake env lean`, 不做全量 build)、`--use-cache`
  (先 `lake exe cache get`) 与 `--build-timeout`; 超时记录为失败而非成功.
