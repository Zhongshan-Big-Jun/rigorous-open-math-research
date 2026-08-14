# Math Research Workflow 插件

管理-研究-验证一体化的数学研究流水线编排插件 (工作流插件仓库旗舰).

## 组成

- `.codex-plugin/plugin.json` -- 插件清单
- `agents/openai.yaml` -- 代理配置
- `skills/math-research-workflow/SKILL.md` -- 编排协议 (三阶段流水线 + 子 agent 分工)
- `skills/math-research-workflow/references/workflow-design.md` -- 设计文档 (角色/交接/并行/失败处理)
- `assets/pipeline-handoff.template.md` -- 阶段交接记录模板
- `assets/interruption-handoff.template.md` -- 中断交接记录模板 (已试路线/未完成义务/下一步动作, 供后续 agent 续接)
- `assets/whiteboard.template.md` -- 求解循环白板模板 (当前计划/路线历史/待回想法/未完成义务/工件索引)
- `scripts/validate_pipeline.py` -- 确定性阶段门禁 (任务包字段/哈希绑定/运行清单/数值证据纪律/git 清洁检查)
- `scripts/doctor.py` -- 环境自检 (插件与依赖 skill 是否安装启用, 市场是否注册, config.toml 启用条目是否完好)

## 依赖的 skill

| Skill | 阶段 | 职责 |
| --- | --- | --- |
| `$manage-math-research-program` | A 管理 | 程序上下文、任务包、工具库、git 同步 |
| `$rigorous-open-math-research` | B 研究 | 契约、多路线、对抗审计、候选证明 |
| `$lean-verify` | C 验证 | Lean 形式化、机器验证、义务级审计 |

## 安装

```text
codex plugin marketplace add xsoc1/rigorous-open-math-research
codex plugin add math-research-workflow@math-research
```

## 使用

用户请求数学项目全流程 (研究 + 形式化验证 + 同步) 时, 本插件编排三阶段流水线;
各阶段内部按子 agent 分工并行, 阶段边界强制交接契约与 git 同步.

阶段 A 派发前先跑环境自检与门禁:

```text
python plugins/math-research-workflow/scripts/doctor.py
python plugins/math-research-workflow/scripts/validate_pipeline.py --project .
```

门禁强制数值证据纪律: 数值检验只能作探索与佐证, 不得单独支撑
`已证`/`CANDIDATE_COMPLETE_PROOF`/`FORMALLY_VERIFIED` 状态; 含数值标签的交付
必须带严格标签或显式降级声明, 否则阶段边界 FAIL.

阶段 B 求解按 OpenProver 式循环运行 (2026-08-14 蒸馏自
arXiv:2607.09217): 求解主导者 (Planner) 维护每 run 一个紧凑 `whiteboard.md`
(当前计划/路线历史/待回想法/未完成义务/工件索引), 并行独立 Worker 只领各自
交付物, 审计 agent 独立复核 Worker 产出; Lean 片段经 `lean_verify` 机器验证
后才入库, `lean_search` 先查 Mathlib 既有声明, `lean_store` 累积已验证上下文.
2026-08-14 之后开始的求解 run 必须携带 whiteboard, 门禁硬校验.

工作中断 (预算耗尽/用户叫停/环境失败) 时, 中断方按
`assets/interruption-handoff.template.md` 写交接记录 (含已尝试路线与结果
标记、未完成义务、精确下一步), 后续 agent 依记录续接, 不得无新理由重跑已
失败路线; 门禁校验交接记录字段完整性.

## 常见问题: 插件"消失"或未启用

- 现象: `codex plugin list` 显示 `math-research-workflow@math-research not
  installed`, 但插件缓存与市场检出都完好.
- 原因: 桌面应用可能在启动/设置同步时重写 `config.toml`, 抹掉
  `[plugins."math-research-workflow@math-research"]` 启用条目.
- 修复: 重跑 `codex plugin add math-research-workflow@math-research` (或在应用
  插件面板重新启用), 无需重装仓库或市场. 阶段 A 的 `doctor.py` 前置检查会在
  派发前自动发现该问题并打印修复命令.
