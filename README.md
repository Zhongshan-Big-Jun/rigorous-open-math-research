# rigorous-open-math-research

Codex 数学研究技能集: 严格开放数学研究 (求解执行层) 与数学研究项目管理 (项目/知识管理层).

本仓库包含两个相互关联的 Codex skill:

## 目录

| 目录 | Skill | 定位 |
| --- | --- | --- |
| `rigorous-open-math-research/` | 严格开放数学研究 | 求解执行层: 显式定理契约, 多样化搜索, 持久研究台账, 可执行验证, 对抗性证明审计, 文献核验, 校准式报告, 快照绑定的数学知识图谱集成 |
| `manage-math-research-program/` | 数学研究项目管理 | 项目管理层: 跨会话研究项目管理, 文献策展与版本, 论文地图/开放问题组合/工具库/预算/检查点, 任务包派发, 已接受知识流水线 (hash 绑定 -> 确定性校验 -> 独立审查 -> 确定性接收 -> 收据) |
| `plugins/lean-verify/` | lean-verify 插件 | Lean 4 形式化验证: 陈述保真审计, 机器验证 (lake build + sorry/admit/axiom 扫描), 义务级独立审计, 结构化裁决, hash 绑定运行清单 |

两者只允许单向调用: `manage-math-research-program -> rigorous-open-math-research`.
`lean-verify` 是独立插件 (随本仓库分发), 用于对 Lean 4 形式化做严格验证, 与两个 skill 互补.

仓库结构: 父仓库为 `xsoc1/rigorous-open-math-research`; `Zhongshan-Big-Jun/rigorous-open-math-research` 是其 fork 副本, 可随时用 GitHub 的 Sync fork 跟进更新.

## 安装

方式一 (skill-installer): 在 Codex 中使用 `$skill-installer`, 仓库路径分别为

- `xsoc1/rigorous-open-math-research/tree/main/rigorous-open-math-research` (父仓库)
- `xsoc1/rigorous-open-math-research/tree/main/manage-math-research-program` (父仓库)

方式二 (手动): 将对应目录整体复制到 `~/.codex/skills/` 下 (Windows: `C:\Users\<用户名>\.codex\skills\`).

`manage-math-research-program` 自带 `MANIFEST.sha256` (sha256 逐文件校验清单), 修改后需重新生成.

插件安装: 将 `plugins/lean-verify/` 复制到本地 `~/plugins/lean-verify` (Windows: `C:\Users\HuangZY\plugins\lean-verify`),
确认个人 marketplace (`~/.agents/plugins/marketplace.json`) 中有 `lean-verify` 条目后执行
`codex plugin add lean-verify@personal`; 或在 Codex 桌面端插件页从 personal marketplace 安装.

## 使用

- 证明/反例/构造/形式化/严格审计单个数学问题: 调用 `$rigorous-open-math-research`.
- 长期项目/文献/工具库/任务包/知识库维护: 调用 `$manage-math-research-program`, 具体数学任务一律派发给前者.
- 若项目根目录是 git 仓库, 两个 skill 会自动检查并保持仓库同步 (会话开始时 `git status`/`git fetch`, 阶段收尾时提交并推送), 详见 `manage-math-research-program/references/git-sync.md`.

## 版本

- 2026-08-11: 新增子 agent 分工模式 (rigorous-open-math-research): 路线探索/义务证明/反例猎手/文献审计/证明验证的并行子 agent 分工, 子任务包契约, 隔离与去相关, 合并协议, 失败机制入档, 动态资源分配与单 agent 顺序 fallback; 管理侧文档同步 (delegation-and-ingestion.md).
- 2026-08-11: 新增 lean-verify 插件 (Lean 4 形式化验证: 陈述保真审计, 机器验证, 义务级独立审计, 结构化裁决与 hash 绑定运行清单).
- 2026-08-11: 新增 arXiv 定理语义检索机制 (完整陈述查询语义定理库, 引用前下载原文核验, 局部结果记录障碍), 新增检索与深度思考交替调度, 新增结构化验证输出规范 (verdict + critical_errors/gaps/repair_hints), 新增用户引用目录机制 (rigorous-open-math-research); 文献策展新增语义定理检索渠道, MANIFEST 同步更新 (manage-math-research-program).
- 2026-08-10: 新增自动 git 仓库同步检查 (MRP 工作流第 0 步 + Rigor Phase 0/10/12).
- 2026-08-09: 蒸馏 Blueprint v2.2 数学工具包 (数学超图/类型/状态语义/可信闭包/四审计/事务-研究状态分离), 整合进两个 skill.
- 2026-08-05: rigorous-open-math-research 迭代自 rigorous-mathematical-research; 建立 manage-math-research-program.
