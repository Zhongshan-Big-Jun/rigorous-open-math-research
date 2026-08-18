# Pipeline full flow: from a math problem to a verified result

This document describes one full run of the math-research workflow pipeline
(`$math-research-workflow` driving `manage-math-research-program` →
`rigorous-open-math-research` → `lean-verify` → submission audit), including
all major branches and terminal states.

## Overview

```mermaid
flowchart LR
  A["输入数学问题"] --> S1["Stage A 任务准备<br/>manage-math-research-program"]
  S1 --> S2["Stage B 求解<br/>rigorous-open-math-research + 多子agent"]
  S2 --> S3["Stage C 验证<br/>lean-verify + 双轨审计"]
  S3 --> S4["提交审计 8e<br/>manage"]
  S4 --> Z["结果汇报 / 入库"]
```

## Full flow with branches

```mermaid
flowchart TD
  IN["输入数学问题"]
  IN --> A1["初始化/恢复项目<br/>(project.json, state/RESUME.md)"]
  A1 --> A2["写任务包 task packet<br/>+ 可选 theorem.lean 骨架 + budget"]
  A2 --> A3["B0 新颖性前置门禁<br/>(openness + novelty + 文献快照)"]
  A3 -->|"问题已解决"| E0["停止/报告已解决"]
  A3 -->|"与已有结果矛盾"| E1["报告冲突/拒绝"]
  A3 -->|"通过"| B0["Stage B: 读问题, 建定理契约"]

  B0 --> B1["检索 arXiv + 网页"]
  B1 -->|"检索有用"| B2
  B1 -->|"检索空转"| B2x["转入深度推理（不再依赖检索）"]
  B2x --> B2
  B2["立即结论 (标记是否脆弱)"] --> B3["构造 toy examples / counterexamples"]
  B3 -->|"反例成立"| E2["该声明被否证<br/>REFUTED / COUNTEREXAMPLE"]
  B3 -->|"未否证"| B4["提出多个分解计划"]
  B4 --> B5["逐计划 direct proving"]
  B5 -->|"某计划全解"| P0["组装 Blueprint"]
  B5 -->|"卡住"| B6["对该子目标立即构造反例"]
  B5 -->|"全败"| B7["递归并行子agent（每计划一个）"]
  B7 -->|"任一成功"| P0
  B7 -->|"全败"| B8["identify-key-failures<br/>综合共同卡点 → 下一代计划"]
  B8 --> B4

  P0 --> V1["调用非正式 verifier"]
  V1 -->|"correct（零错误零缺口）"| C0
  V1 -->|"wrong"| V1x["按 repair_hints 修订"] --> B2

  B5 -.->|"预算检查（每步边界）"| BK
  BK["预算检查"]
  BK -->|"足够"| B,继续
  BK -->|"接近完成但不够"| B9["request_extension（请求追加）"]
  BK -->|"耗尽"| B10["PAUSED_BUDGET: 保存whiteboard/repo/history/facts + 写handoff<br/>后续可恢复"]

  C0["Stage C: 双重审计"]
  C0 --> C1["① 非正式审计（Danus式）<br/>零错误零缺口"]
  C1 -->|"失败"| C1x["修订证明"] --> B2
  C1 -->|"通过"| C2["② Lean scaffold (Tier 0) 锁陈述"]
  C2 --> C3["③ Lean 完整验证 (Tier 2, 完成标签)"]
  C3 -->|"通过"| C4["④ 论文级再验证"]
  C3 -->|"失败"| C3x["修 Lean (statement freeze / sorrifier)"] --> C2
  C4 -->|"通过"| D0["提交审计 8e"]
  C4 -->|"失败"| C4x["修论文，不静默跳过"]

  D0["仓库比对"]
  D0 -->|"重复"| E3["REJECT"]
  D0 -->|"矛盾"| E4["停止，先解决矛盾"]
  D0 -->|"干净"| D1["依规则加入:<br/>更新STATUS/index/papers/tools + superseded + commit/push"]
  D1 --> Z["结果汇报 / 入库"]
```

## Branch summary

| 位置 | 分支 | 结果 |
| --- | --- | --- |
| B0 新颖性 | 已解决 / 矛盾 / 通过 | 停止 / 拒绝 / 继续 |
| 检索 | 有用 / 空转 | 继续 / 转深度推理 |
| 反例 | 成立 / 未成立 | 否证 / 继续 |
| 分解 | 某计划解 / 全败+递归 | 组装 / 失败综合下一轮 |
| 预算 | 够 / 追加 / 耗尽 | 继续 / 请求追加 / PAUSED_BUDGET |
| 非正式验证 | correct / wrong | Stage C / 修订 |
| Lean 验证 | 通过 / 失败 | 形式化通过 / 修 Lean 或回 NL |
| 论文级验证 | 通过 / 失败 | 交付 / 修论文 |
| 8e 比对 | 重复 / 矛盾 / 干净 | REJECT / 停止 / 入库 |

## Terminal states

- `FORMALLY_VERIFIED_PROOF` — 完整 + 机器验证
- `INDEPENDENTLY_AUDITED_PROOF` — 独立审计通过
- `CANDIDATE_COMPLETE_PROOF` — 候选完整证明
- `RIGOROUS_PARTIAL_RESULT` — 严格部分结果
- `COUNTEREXAMPLE_CANDIDATE` / `REFUTED` — 反例/否证
- `PAUSED_BUDGET` — 预算暂停，可恢复
- `NO_MATERIAL_PROGRESS` — 无实质进展
- `BLOCKED` / `INTERRUPTED`（带 handoff）— 阻塞/中断，可续接

## Research map

Throughout the run, every route/method, intermediate result, unexpected
finding, failure reason, tool, open direction, and human/other-agent
contribution is continuously collected into the project's `research_map.md`
(see `manage-math-research-program` workflow 8f).
