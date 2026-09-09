# Math Research 2.0

[English](README_EN.md) | [使用与迁移](docs/v2.0-guide.md) | [实施与验证](docs/v2.0-implementation-status.md)

面向长期数学研究的 Codex 插件. 帮助人和 agent 从论文, 成功证明与失败路线中积累可复用的工具和理解, 再把它们带入下一个问题.

四个组件统一为 `2.0.0`, 以简短工作引导配合实际工具. 研究者可以自主选择证明, 反例, 文献, 计算, 协作或 Lean, 按问题需要使用各组件.

## 能做什么

| 研究中的需要 | 2.0 提供的支持 |
| --- | --- |
| 论文读过以后还能找到并用上 | 保存原文, 版本和定位, 按段读取, 建立工具卡及可重建指针 |
| agent 能留下自己的理解和疑问 | 可检索的自由批注, 关联具体卡片版本, 保留来源与适用范围 |
| 成功和失败都能帮助后续研究 | 保存变换, 构造, 程序, 关键障碍和重试条件, 按需比较路线 |
| 人能参与整理与判断 | 可编辑的项目理解页, 区分已有解释, 候选想法, 直觉与待讨论问题 |
| 会话或额度中断后继续 | 读取当前进展, 保存原子快照, 找回实际任务与日志, 防止重复执行及旧状态覆盖 |
| 在研究中使用 Lean | 编译反馈, 精确声明及传递公理检查, 分开报告执行, 语义, 根目标与证据身份 |

工具卡与指针表是核心. 卡片保存数学内容和条件, 注释承载理解与修正, 指针帮助下一次研究找到实际证据. 卡片数量和图节点数量本身不是研究成果.

## 选择组件

四个组件可以分别安装和调用, 无须强制串联.

| 插件 / Skill | 适合的工作 |
| --- | --- |
| `$math-research-workflow` | 跨问题, 跨会话研究的组织与续接 |
| `$rigorous-open-math-research` | 证明, 反例, 构造和数学论证审查 |
| `$manage-math-research-program` | 文献, 可批注工具库, 研究经验和项目理解 |
| `$lean-verify` | Lean 反馈, 形式化目标核对和可复现验证 |

例如:

> 使用 $manage-math-research-program, 找出这些证明与失败路线中值得复用的工具, 保留适用条件和证据指针, 更新我们对问题的理解.

> 使用 $rigorous-open-math-research 继续这个问题. 根据当前数学进展选择方法, 有必要时使用文献或 Lean, 并保留能够帮助下一次研究的信息.

## 安装

本仓库的 marketplace 名为 `math-research`. 在支持插件的 Codex CLI 中:

```bash
codex plugin marketplace add xsoc1/rigorous-open-math-research
codex plugin add math-research-workflow@math-research
codex plugin add rigorous-open-math-research@math-research
codex plugin add manage-math-research-program@math-research
codex plugin add lean-verify@math-research
```

可只安装需要的组件. 已安装时刷新 marketplace 后重新安装目标组件. 安装后新开任务以加载新版技能与工具, 参见 [OpenAI 插件说明](https://learn.chatgpt.com/docs/plugins). 工具需要 Python 3.10+; 文献索引使用 PyYAML; Lean 功能使用项目固定的 Lean/Lake 环境.

安装完整插件, 不单独复制 `SKILL.md`: 部分可执行工具位于插件的 `scripts/` 和 `runtime/` 下. DSH 用户使用单向适配仓库 [math-research-dsh](https://github.com/xsoc1/math-research-dsh).

## 成果仓库

[Sturm-Liouville theory research](https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research) 是使用本插件开展长期人机协作研究的成果仓库, 包含谱理论证明, 开放问题, 失败路线, 工具卡, 计算证书与部分 Lean 工程.

插件协助研究的组织, 探索和核验. 数学成果的具体贡献, 严格性和适用范围以该仓库的证明与审计记录为准; 使用插件不等于所有结论已经形式化验证.

## 验证与已知范围

[实施记录](docs/v2.0-implementation-status.md) 区分实际完成的功能, 行为测试, 迁移回放和实验范围. [迁移指南](docs/v2.0-guide.md) 说明旧卡片, 批注, 检查点和验证结果如何继续使用.

旧版 / 新版 / 空白对照原件保留在 [L1](benchmarks/codex-20260906-l1/CONCLUSIONS.md) 与 [Q9](benchmarks/codex-20260908-q9/CONCLUSIONS.md). 这些是 1.x 的既有实验, 不作为 2.0 的加速或新发现证据. Q9 三组都通过证明外审, 空白组最快. 2.0 的价值需要通过实际复用, 范围正确性和长期研究进展来衡量.

Fuse / Prove2Me 的方法调研见 [报告](docs/lean-verification-platform-research-2026-09-09.md). 本地实现不意味着已经接入其生产服务, 也不意味着本仓库独立重放了完整 Kakeya 或 FLT 形式化.

## 开发与维护

```bash
python3 -X utf8 scripts/validate_all.py
python3 -X utf8 tests/test_research_state.py
```

其余行为检查由 [CI](.github/workflows/validate.yml) 统一运行. 验证结果不能只依赖提示词中出现某个关键词. 旧协议的兼容检查显式使用 `validate_pipeline.py --legacy-v1`.

| 路径 | 内容 |
| --- | --- |
| `plugins/` | 四个可安装组件, 简短入口及按需工具与参考 |
| `tests/`, `scripts/` | 行为验证, 维护工具和独立实验装置 |
| `docs/` | 2.0 指南, 实施结果, 方法调研和历史设计 |
| `benchmarks/` | 冻结的题目, 运行记录, 证明, 审计与成本证据 |
| `AGENTS.md` | 维护方法与当前会话摘要 |

[重构设计](docs/v2.0-refactor-plan.md) | [清理记录](docs/v2.0-cleanup.json) | [维护历史](AGENTS_HISTORY.md)

## 许可与来源

代码与文档按 [MIT](LICENSE) 许可发布. 方法参考及归属保留在各组件的 `references/` 与调研报告中. 第三方论文, 软件和名称遵循其各自许可与归属; 项目不暗示第三方背书.
