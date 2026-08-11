# rigorous-open-math-research

Codex 数学研究插件仓库 (marketplace): 覆盖 严格开放数学研究 -> 项目管理 -> Lean 4 形式化验证 的完整数学研究工作流.

仓库是标准 Codex marketplace, 包含 4 个插件, 安装后即可在 Codex 中调用对应的数学研究 skill.

## 插件清单

| 插件 | 提供的 Skill | 定位与能力 |
| --- | --- | --- |
| `rigorous-open-math-research` | 严格开放数学研究 | 求解执行层. 单个数学问题的 证明/反例/构造/形式化/严格审计: 显式定理契约, 多样化搜索, 持久研究台账, 可执行验证, 对抗性证明审计, 文献核验 (引用必须附链接且不得编造), 校准式报告, 子 agent 分工 |
| `manage-math-research-program` | 数学研究项目管理 | 项目管理层. 跨会话/跨论文/跨问题的长期研究项目管理: 项目工作区初始化与校验, 文献策展, 论文地图, 开放问题组合, 工具库, 预算/检查点/阶段总结, 任务包派发 (具体数学任务派发给 rigorous-open-math-research), 已接受知识流水线 (hash 绑定 -> 确定性校验 -> 独立审查 -> 确定性接收 -> 收据) |
| `lean-verify` | Lean 4 形式化验证 | 验证层. 对 Lean 4 形式化做严格验证: 陈述保真审计, 机器验证 (lake build + sorry/admit/axiom 扫描), 义务级独立审计, 结构化裁决 (verdict + gaps/repair_hints), hash 绑定运行清单 |
| `math-research-workflow` | 一体化工作流编排 | 编排层. 管理-研究-验证三阶段流水线: 阶段 A 项目管理与任务包, 阶段 B 严格问题研究 (求解/审计子 agent), 阶段 C Lean 形式化与机器验证; 强制交接契约, 诚实状态标注, 阶段边界自动 git 同步 |

依赖方向 (单向, 无反向调用):

```text
manage-math-research-program -> rigorous-open-math-research
math-research-workflow -> manage-math-research-program + rigorous-open-math-research + lean-verify
lean-verify 独立插件, 与两个 skill 互补
```

## 安装 (推荐: marketplace)

```bash
# 添加本仓库为 marketplace (owner/repo 或完整 URL 均可, 仅需一次)
codex plugin marketplace add xsoc1/rigorous-open-math-research

# 查看可用插件
codex plugin list

# 按需安装 (可只装需要的组件; marketplace 名为 math-research)
codex plugin add rigorous-open-math-research@math-research
codex plugin add manage-math-research-program@math-research
codex plugin add lean-verify@math-research
codex plugin add math-research-workflow@math-research
```

- marketplace 清单位于仓库根 `.agents/plugins/marketplace.json` (marketplace 名: `math-research`).
- 安装后需新开一个 Codex 会话以加载插件 skill.

## 安装 (备选: skill-installer)

在 Codex 中使用 `$skill-installer`, 仓库路径分别为

- `xsoc1/rigorous-open-math-research/tree/main/plugins/rigorous-open-math-research/skills/rigorous-open-math-research`
- `xsoc1/rigorous-open-math-research/tree/main/plugins/manage-math-research-program/skills/manage-math-research-program`

或手动将对应 skill 目录复制到 `~/.codex/skills/` 下 (Windows: `C:\Users\<用户名>\.codex\skills\`).
`manage-math-research-program` 自带 `MANIFEST.sha256` (sha256 逐文件校验清单), 修改后需重新生成.

## 使用

| 场景 | 调用 |
| --- | --- |
| 单个数学问题 (证明/反例/构造/审计) | `$rigorous-open-math-research` |
| 长期项目/文献/工具库/任务包/知识库维护 | `$manage-math-research-program` (数学任务派发给前者) |
| Lean 4 形式化验证 | `$lean-verify` |
| 管理-研究-验证全流程一体化 (含子 agent 分工) | `$math-research-workflow` |

- 若项目根目录是 git 仓库, skill 会自动检查并保持仓库同步 (会话开始 `git status`/`git fetch`, 阶段收尾提交并推送), 详见 `manage-math-research-program/references/git-sync.md`.
- 所有研究结论遵循严格性标注: 严格证明 / 数值证据 / 猜想 显式区分, 未完成严格证明的断言不标为 "已解决".

## 仓库结构

- 父仓库: `xsoc1/rigorous-open-math-research`
- fork 副本: `Zhongshan-Big-Jun/rigorous-open-math-research` (可用 GitHub 的 Sync fork 跟进更新)

## 版本历史

- 2026-08-11: 仓库编排为标准 Codex marketplace (`.agents/plugins/marketplace.json`, 名 `math-research`); 两个 skill 迁移为插件形态 (`plugins/<name>/skills/<name>`, 各含 `.codex-plugin/plugin.json`), 4 个插件统一元数据 (author/repository/license/版本 cachebuster `0.1.0+codex.20260811`); README 安装方式改为 marketplace 优先.
- 2026-08-11: 新增 `math-research-workflow` 一体化编排插件 (管理-研究-验证三阶段流水线 + 子 agent 分工 + 交接契约 + 阶段边界 git 同步).
- 2026-08-11: 新增 `lean-verify` 插件 (Lean 4 形式化验证: 陈述保真审计, 机器验证, 义务级独立审计, 结构化裁决与 hash 绑定运行清单).
- 2026-08-11: 子 agent 分工模式 (rigorous-open-math-research): 路线探索/义务证明/反例猎手/文献审计/证明验证并行分工, 子任务包契约 (裸 JSON + artifact_sha256, 合并前重算哈希核验); 新增 arXiv 定理语义检索与结构化验证输出规范.
- 2026-08-10: 新增自动 git 仓库同步检查 (MRP 工作流第 0 步 + Rigor Phase 0/10/12).
- 2026-08-09: 蒸馏 Blueprint v2.2 数学工具包 (数学超图/类型/状态语义/可信闭包/四审计/事务-研究状态分离), 整合进两个 skill.
- 2026-08-05: `rigorous-open-math-research` 迭代自 `rigorous-mathematical-research`; 建立 `manage-math-research-program`.
