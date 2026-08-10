# rigorous-open-math-research

Codex 数学研究技能集: 严格开放数学研究 (求解执行层) 与数学研究项目管理 (项目/知识管理层).

本仓库包含两个相互关联的 Codex skill:

## 目录

| 目录 | Skill | 定位 |
| --- | --- | --- |
| `rigorous-open-math-research/` | 严格开放数学研究 | 求解执行层: 显式定理契约, 多样化搜索, 持久研究台账, 可执行验证, 对抗性证明审计, 文献核验, 校准式报告, 快照绑定的数学知识图谱集成 |
| `manage-math-research-program/` | 数学研究项目管理 | 项目管理层: 跨会话研究项目管理, 文献策展与版本, 论文地图/开放问题组合/工具库/预算/检查点, 任务包派发, 已接受知识流水线 (hash 绑定 -> 确定性校验 -> 独立审查 -> 确定性接收 -> 收据) |

两者只允许单向调用: `manage-math-research-program -> rigorous-open-math-research`.

## 安装

方式一 (skill-installer): 在 Codex 中使用 `$skill-installer`, 仓库路径分别为

- `Zhongshan-Big-Jun/rigorous-open-math-research/tree/main/rigorous-open-math-research`
- `Zhongshan-Big-Jun/rigorous-open-math-research/tree/main/manage-math-research-program`

方式二 (手动): 将对应目录整体复制到 `~/.codex/skills/` 下 (Windows: `C:\Users\<用户名>\.codex\skills\`).

`manage-math-research-program` 自带 `MANIFEST.sha256` (sha256 逐文件校验清单), 修改后需重新生成.

## 使用

- 证明/反例/构造/形式化/严格审计单个数学问题: 调用 `$rigorous-open-math-research`.
- 长期项目/文献/工具库/任务包/知识库维护: 调用 `$manage-math-research-program`, 具体数学任务一律派发给前者.
- 若项目根目录是 git 仓库, 两个 skill 会自动检查并保持仓库同步 (会话开始时 `git status`/`git fetch`, 阶段收尾时提交并推送), 详见 `manage-math-research-program/references/git-sync.md`.

## 版本

- 2026-08-10: 新增自动 git 仓库同步检查 (MRP 工作流第 0 步 + Rigor Phase 0/10/12).
- 2026-08-09: 蒸馏 Blueprint v2.2 数学工具包 (数学超图/类型/状态语义/可信闭包/四审计/事务-研究状态分离), 整合进两个 skill.
- 2026-08-05: rigorous-open-math-research 迭代自 rigorous-mathematical-research; 建立 manage-math-research-program.