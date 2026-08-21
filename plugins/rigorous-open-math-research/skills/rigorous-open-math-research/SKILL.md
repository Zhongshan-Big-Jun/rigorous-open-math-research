---
name: rigorous-open-math-research
description: >-
  Investigate open or research-level mathematics problems with explicit theorem contracts, diverse search, persistent research ledgers, executable checks, adversarial proof audits, literature verification, calibrated reporting, and snapshot-bound mathematics knowledge-graph integration when the project provides one. Use when asked to solve, disprove, advance, formalize, or rigorously audit a difficult mathematics problem.
  中文触发: 适用于定理证明, 猜想攻关, 反例搜索, 结构分类, 等价刻画, 复杂推导, 严格审计等困难数学问题,
  也用于把计算证据升级为可审计定理或给出精确剩余缺口.
---

# Rigorous Open Mathematics Research

## 中文使用说明 (摘要)

本 Skill 用于对开放、前沿或高难度数学问题做严格研究. 它不承诺用措辞解决开放问题,
而是最大化可审计进展: 显式定理契约, 多样化搜索, 持久研究台账, 可执行验证, 对抗性证明审计, 文献核验与校准式报告.

- 触发场景: 定理证明, 猜想攻关, 反例搜索, 结构分类, 等价刻画, 复杂推导, 严格审计.
- 图谱集成: 若项目提供已接受知识库 (Blueprint v2.2 数学超图), 检索将绑定快照 (math-closure / math-frontier), 可依赖前提与前沿由确定性程序给出, 合同见 references\blueprint-math-graph-integration.md.
- 启动后按 Phase 0-12 工作, 并维护 "Default research artifacts" 中的台账文件.
- 结果必须按 "Output protocol" 的状态标签开头, 未闭合义务不得标为完成.
- 本 Skill 是求解执行层; 长期项目管理由 `$manage-math-research-program` 负责, 二者只允许 管理到求解 的单向调用.
- 中文设计依据与完整分析: `references/ai-open-math-prompting-design-analysis.zh-CN.md`; 旧版中文 v1 全文: `references/rigorous-mathematical-research.v1-zh-CN.md`.
## Purpose

Use this skill to conduct serious AI-assisted research on an open, frontier, or unusually difficult mathematics problem.

The goal is not to produce a persuasive-looking proof. The goal is to maximize the chance of obtaining one of the following, with its status stated honestly:

- a complete proof or disproof;
- a formally or independently verified construction;
- a rigorous partial theorem;
- a useful reduction with a strictly smaller unresolved core;
- a falsified route, counterexample, or exact obstruction;
- a reproducible computational pattern that yields clear proof obligations.

Treat the **entire research configuration** as the input: problem statement, attachments, known results, code, evaluators, theorem-prover versions, tools, model constraints, search restrictions, and human-provided hints. Never pretend that a one-line instruction was the full prompt when essential context came from other files or systems.

## Non-negotiable epistemic rules

1. Never claim a complete solution while any required proof obligation remains open.
2. Never silently change a quantifier, domain, definition, regularity assumption, asymptotic regime, or boundary case.
3. Never call a theorem-strength missing lemma “routine”, “standard”, or “technical” without proving it or citing an exact applicable theorem.
4. Finite computation, numerical evidence, and passing a score function do not imply a general theorem unless a proof or universally checkable certificate bridges the gap.
5. Formal verification proves the formal statement, not automatically its fidelity to the original problem or its novelty.
6. Distinguish correctness, completeness, novelty, autonomy, and reproducibility. Do not collapse them into one word such as “solved”.
7. Do not invent hidden prompts, run counts, model settings, tool traces, or human interventions. Mark unknown information as unknown.
8. Do not require or expose private chain-of-thought. Require externally checkable artifacts: definitions, lemmas, equations, constructions, counterexamples, citations, code, certificates, and exact gap reports.
9. A failed route is a research result when its failure mechanism is precise and reusable. Record it.
10. At a resource boundary, report the strongest audited progress and exact remaining gaps. Only the **completion label** is withheld until the proof is complete; useful partial results must not be suppressed.
11. Every material progress item is first-class: register it immediately in the ledger, route registry, and tool library, and when a formalization project exists create a Lean scaffold for the new result before moving on. Partial progress is progress; it must be auditable and formalization-tracked, not deferred until a complete proof exists.
12. Lean verification is not only for the final conclusion: machine-check key intermediate lemmas as soon as they become load-bearing, so errors are caught before a route is invested further. A later, more advanced result may supersede an earlier partial/scaffold result; keep the old record in history but mark it superseded in the formalization progress and knowledge base.
13. A candidate proof submitted for repository acceptance must pass the proof submission audit pipeline (manage workflow 8e): repository comparison, Lean verification/audit, then rule-based integration. The submission audit record must accompany the proof.

## Default research artifacts

When persistent files are available, maintain the following. If files are unavailable, use equivalent clearly labeled sections in the response.

- `problem_contract.md` — exact normalized statement and completion criteria.
- `repro_manifest.md` — all inputs, versions, tools, restrictions, hashes or identifiers, and unknown fields.
- `status_and_literature.md` — current problem status, exact known theorems, citations, and novelty risks.
- `obligation_graph.md` — claims, dependencies, and proof status.
- `approach_registry.md` — route families, owners, states, and exact gaps.
- `research_ledger.md` — chronological experiments, derivations, decisions, and failures.
- `counterexample_log.md` — tested edge cases, failed lemmas, minimal counterexamples, and search code.
- `candidate_proof.md` — current integrated proof or disproof draft.
- `audit_report.md` — independent verification results and unresolved issues.
- `reproducibility/` — code, exact commands, seeds, certificates, and formalization files.
- `formalization_progress.md` — when a formalization project exists, track every new result's Lean scaffold/status here (or in the project's `lean-proof/STATUS.md`).
- `research_map.md` — the human-readable, continuously updated survey of the problem: routes/methods tried, intermediate results, unexpected findings, failures and reasons, tools, open directions, an avoid list, and human/other-agent contributions (maintained per manage workflow 8f).
- `escalation_ladder.md` — when cost-tiered escalation is used, the run-level log of cheap probes attempted, tier changes, triggers, failure mechanisms, and the current cost tier (see `references/escalation-ladder.md`).

Update the ledger immediately after any substantial computation, proof attempt, literature discovery, or route decision. Do not begin a near-duplicate exploration until the previous result and failure mechanism are recorded. Publish every material finding, surprise, and failure reason to the research map (or ensure its source is aggregated there) so partial progress is never lost and later humans/agents can build on it.

# Workflow

## Phase index

Read the referenced file through this skill's resourceBase directory before
executing a phase; every phase file repeats this contract at its top.

| Phase | File |
|---|---|
| 0-1 provenance, scope, theorem contract | `references/phase-01-contract.md` |
| 2-3 literature map + proof-obligation graph | `references/phase-23-search.md` |
| 4-5 route portfolio + research loop | `references/phase-45-routes-loop.md` |
| cost-aware escalation ladder (light first) | `references/escalation-ladder.md` |
| 6 computational and evolutionary search | `references/phase-6-computation.md` |
| 7-8 synthesis + adversarial proof audit | `references/phase-78-synthesis-audit.md` |
| 9-11 revision, formalization, novelty | `references/phase-91011.md` |
| 12 stopping and reporting (+ Result template) | `references/phase-12-reporting.md` |
| delegation, sub-agents, role prompts | `references/agent-orchestration.md` |
| Rethlas-distilled methods (memory/failure synthesis/counterexample reuse/search discipline) | `references/rethlas-distilled.md` |
| Dual-track audit (informal + Lean formal verification coexistence) | `references/dual-track-audit.md` |

Global contracts (epistemic rules, artifacts, Output protocol, anti-patterns)
stay in this file and bind every phase.
# Output protocol

Begin with a one-line status chosen from:

- `FORMALLY_VERIFIED_PROOF`
- `INDEPENDENTLY_AUDITED_PROOF`
- `CANDIDATE_COMPLETE_PROOF`
- `RIGOROUS_PARTIAL_RESULT`
- `VERIFIED_GENERAL_CONSTRUCTION`
- `FINITE_COMPUTATIONAL_RESULT`
- `NUMERICAL_EVIDENCE`
- `COUNTEREXAMPLE_CANDIDATE`
- `BLOCKED_REDUCTION`
- `NO_MATERIAL_PROGRESS`

Then provide:

```markdown
# Anti-patterns

Do not rely on:

- “You are a genius mathematician” role-play;
- forceful persistence language without actual resources;
- fixed numbers of ideas, agents, or hours as universal constants;
- long prompts that repeat the same completion demand;
- post-hoc hints presented as original discovery prompts;
- same-model approval as the only proof check;
- a verifier that checks style instead of obligations;
- finite test success presented as asymptotic or universal proof;
- hidden human selection presented as autonomous discovery;
- a beautiful reduction whose missing lemma is equivalent to the conjecture;
- polished LaTeX before mathematical closure;
- novelty claims without literature audit.

# Minimal invocation

```text
Use the rigorous-open-math-research skill on the following problem.
First build and audit the theorem contract, then run a diverse research portfolio,
maintain an obligation graph and route ledger, use computation or formalization where
appropriate, and subject every candidate proof to adversarial verification.
Return the strongest rigorously supported result with an exact status label, remaining
gaps, provenance, and reproducibility information. Do not invent unpublished run data.

Problem:
{{problem}}

Available attachments/tools/constraints:
{{context}}
```


## Changelog (2026-08-11)
## Changelog (2026-08-12)

- 新增发散式检索契约 (Phase 2): 搜索宽不守门, 相关性判断与正确性审计分离, 来源诚实三要素 (query -> result -> locator), 分层检索流水线 (关键词族/KB 优先/本地引用/arXiv+OpenAlex+zbMATH/通用网页/深读正文).
- 新增首次见证验证者标准与自动失败模式 (Phase 8): verifier 无记忆首次审稿, 14 类自动 FAIL 模式, 首错定位 + 错误层分类 (陈述/证明/依赖/边界约定), 结构化输出增加 first_error.
- 新增最小责任失败路由 (Phase 9): 失败按归属分类 (计划/来源/定义/装配/路线策略/目标障碍), 派最小责任角色, regulator 只分类不代笔.
- 新增形式化三机制 (Phase 10): 陈述冻结后再修证明 (已批准陈述修改需重新过审), sorrifier 分解 (失败块 sorry 化保留骨架 + 子问题递归), 四道闸 + 人工语义复核 (编译/sorry/axiom/guard + 陈述仍忠于来源).
- 新增新鲜上下文收敛检查 (Phase 12): 收尾/长跑中段/策略转向后只从文件重建现状, 判断收敛与否, 只登记不修改.
- 方法来源: MMAT nl-prover/fl-prover prompts (https://github.com/MechMath/MechMath-agent-team), LeanMarathon (https://github.com/YuanheZ/LeanMarathon), MechMath-v1 sorrifier (https://github.com/MechMath/MechMath-v1), M2F (https://github.com/optsuite/M2F), FaithSieve (https://github.com/TropicalFatFish/anonymous-faithsieve), FormalRx (https://github.com/LARK-AI-Lab/formalrx, arXiv:2607.04655), Archon-Horizon (https://github.com/frenzymath/Archon-Horizon).


- 新增子 agent 分工模式 (Agent orchestration + references/subagent-delegation.md + assets/subtask-packet.template.md): 路线探索/义务证明/反例猎手/文献审计/证明验证的并行子 agent 分工, 子任务包契约 (subgoal_id, 输入 hash, 输出契约, 约束, 预算), 隔离与去相关, 合并协议 (只合并已审计模块 + Phase 7 接口检查), 失败机制入档, 动态资源分配与单 agent 顺序 fallback.
- 新增 arXiv 定理语义检索机制 (Phase 2): 以完整数学陈述查询语义定理检索服务, 记录完整陈述/arXiv id/theorem id/paper id, 下载原文核验后再引用; 局部结果必须记录额外假设与真实障碍.
- 新增检索与深度思考交替调度 (Phase 5): 检索轮与禁用检索的独立推理轮交替, 检索失效时转入非检索技能并记录停滞查询.
- 新增结构化验证输出规范 (Phase 8): audit 记录采用 verdict + critical_errors/gaps/repair_hints 字段, 严格规则 (errors 与 gaps 全空才 PASS), 非 PASS 必须提供修复提示.
- 新增用户引用目录机制 (Phase 0): 问题附带引用目录时先于外部检索读取, 视为用户提供的上下文而非已核验事实.
## Changelog (2026-08-09)

- 蒸馏整合 Blueprint v2.2 数学工具包 (Downloads/blueprint-v22-math-codex-toolkit): 命题/推理超图与状态语义, 可信闭包与目标 frontier 查询钩子, research_goal 结构化契约字段, 内容哈希证明包, 四项强制审计 (definition/logic/boundary/adversarial), 事务状态与研究状态分离, 失败入档纪律.
- 新增参考: `references/blueprint-math-graph-integration.md` (v2.2 蒸馏合同).
- 原有 Phase 3/4/8/12 与 Output protocol 相应增强; 当项目提供规范知识库 (MRP knowledge/ 或 Blueprint statistics/) 时, 工作流与图集成.
## Changelog (2026-08-05)

- 由 `rigorous-mathematical-research` v1.0 (中文) 迭代升级并改名为 `rigorous-open-math-research`.
- 基底内容来自 `Downloads/rigorous-open-math-research` (英文版).
- 新增: 双语触发描述, 中文使用说明摘要, `references/` 中文设计分析报告与旧版 v1 全文.

## Changelog (2026-08-14)
- 渐进式披露重构: Phase 0-12 详细契约与角色 prompt 纯移动至 references/ (phase-01-contract, phase-23-search, phase-45-routes-loop, phase-6-computation, phase-78-synthesis-audit, phase-91011, phase-12-reporting, agent-orchestration); SKILL.md 退化为驱动层 (全局规则/工件清单/Phase 索引表/Output protocol/Anti-patterns), 单次加载从 44978 bytes 降至 12042 bytes; 内容未改写, scripts/split_rigorous_skill.py --verify 可复验覆盖.
## Changelog (2026-08-14, distilled methods)
- 吸收社区方法 (纯增量, 不改动已有内容): 答案空间与验收标准前置 (phase-01);
  覆盖维度枚举与 coverage_gaps 定向侦察 (phase-23); 边际信息增益停止规则 +
  证据三态 confirmed/uncertain/gaps (phase-45); 零增益停止见证 (phase-12);
  角色模型分层 (agent-orchestration). 方法来源: dsh-deep-research
  (https://github.com/omdsh-dev/dsh-deep-research), dsh-multiagent-modes
  (https://github.com/y08lin4/dsh-multiagent-modes).
## Changelog (2026-08-14, optional external capabilities)
- Phase 0 新增第 9 条: 可选文档解析/图像转写服务的使用约定 (记录服务与版本; 解析与
  视觉输出一律视为未验证输入, 必须回查原始来源才能支撑证明步骤). 方法来源: DSH 生态
  dsh-plugin-mineru (https://github.com/HuanLinOTO/dsh-plugin-mineru), dsh-vision
  (https://github.com/william-jin-cmu/dsh-vision), dsh-vision-toolkit
## Changelog (2026-08-16, distilled methods round 2)
- 检索契约增强 (phase-23): 每条检索记录 `query -> result -> locator` 之外再记
  `status` (ok/degraded/unavailable) 与 `uncertainty` vs `warnings` 二分、引擎尝试
  顺序; 禁止编造相关性分数; 本地已读文献/确定性索引取有界证据片段并以章节名引用;
  新增目标问题状态确认小节 (fetch_required: 摘要级不足以判定开放/已解决, 逐条记
  fetch status fetched-verified/abstract-only/paywalled/unreachable, 分层确认 +
  证据强度排序启发 + 缺口侦察清单 + 跨会话回填复用). 方法来源: modsearch, argo,
  dsh-zotero, dsh-exa-mcp, dsh-kb-sieve, dsh-web-search-pro.
- 对抗审计增强 (phase-78): 对抗者只以反例/矛盾排除路线 (counterexample-only);
  简化情形 ground truth 双导线重导 (两次独立手段一致才算一致); 结构化输出新增
  covered_scope 与 residual_risk 字段, 完成声明必须陈述覆盖范围与残余风险.
  方法来源: dsh-rigorquant, Aegis.
- 路线循环增强 (phase-45): 路线尝试视为有状态假说 (预测->测试->终止并记录精确
  缺口, forward-only 重开需新机制); 循环检测 (无新机制重试 REFUTED/BLOCKED 路线
  即拒绝). 方法来源: dsh-science, dsh-trajectory-governance.
- 契约增强 (phase-01): 目标问题状态命中一律 fetch_required; 契约新增
  `## Forbidden moves` 每问题禁用清单. 方法来源: argo, dsh-design-skills.
  (https://github.com/Anionex/dsh-vision-toolkit).
## Changelog (2026-08-16, submission audit)
- 新增规则 13: 候选证明提交仓库前必须经过证明文件提交审计流程 (manage 8e:
  仓库比对 -> Lean 验证与审计 -> 依规则加入), 并附带提交审计记录.
## Changelog (2026-08-16, efficiency)
- Phase 10 增加 Tier 0/1/2 分级验证与 lemma reuse index: 用最低足够档位验证,
  证明前先查 `lean-proof/LEMMA_INDEX.md` 避免重复证明.
## Changelog (2026-08-16, Rethlas distillation)
- 新增 `references/rethlas-distilled.md`: 蒸馏 Rethlas 方法精髓 - 持久结构化记忆,
  失败综合驱动下一代方案, 分解计划组合筛选与递归并行, 反例复用库, 搜索是支撑不是
  替代, 外部引用非黑盒, 严格零错误零缺口接受, 论文式蓝图输出.
## Changelog (2026-08-16, dual-track audit)
- 新增 `references/dual-track-audit.md`: Danus 式非正式审计与 Lean 形式化验证
  共存的四层协议 (非正式审计 -> Lean scaffold -> Lean 完整验证 -> 论文级再验证),
  冲突裁决规则, Danus 硬禁止项, 双轨验证矩阵.
## Changelog (2026-08-16, research map)
- 默认工件新增 `research_map.md` (人类可读、持续更新的研究综述); 中间结果、
  意外发现、失败原因必须发布进地图 (或确保其来源被聚合), 部分进展不丢失.
## Changelog (2026-08-16, escalation ladder)
- 新增 `references/escalation-ladder.md` (cost-tiered escalation, light first):
  研究动作按成本分层 (Tier 0 查与测 / Tier 1 小改动 / Tier 2 中等系统化 /
  Tier 3 重型并行), 行动按信息增益/成本排序, 升级必须由零收益/反例/load-bearing
  gap/用户授权触发, 重型失败后回退寻找更小变体; Phase 4 route card 增加
  `cost_tier` / `minimal_first_step` / `escalation_criteria`, Phase 5 增加第 0 步
  cheapest admissible probe, 默认工件新增 `escalation_ladder.md`.
