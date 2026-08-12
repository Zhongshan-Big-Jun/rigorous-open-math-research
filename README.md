# rigorous-open-math-research

Codex 数学研究工作流插件仓库 (marketplace): 一个仓库装下 管理 → 研究 → 验证 的完整数学研究工作流.

本仓库是标准 Codex marketplace (名 `math-research`), 包含 4 个插件, 安装后可在 Codex 中调用对应 skill.
`math-research-workflow` 是编排层 (旗舰), 把其余三个 skill 组织成三阶段流水线.

## 工作流总览

```mermaid
flowchart LR
  A["阶段 A 管理<br/>$manage-math-research-program"] -->|"任务包 Q-<date>-<tag>-<hash8>"| B["阶段 B 研究<br/>$rigorous-open-math-research"]
  B -->|"候选证明 (CANDIDATE_COMPLETE_PROOF)"| C["阶段 C 验证<br/>$lean-verify"]
  C -->|"verdict + run-manifest"| D["已接受知识库 (hash 绑定)"]
  B --> B1["求解子 agent"]
  B --> B2["审计子 agent"]
  C --> C1["形式化子 agent"]
  C --> C2["验证子 agent"]
```

- 阶段边界强制交接契约 (`assets/pipeline-handoff.template.md`) 与自动 git 同步 (先父仓库, 后 fork).
- 只有 `已证` / `CANDIDATE_COMPLETE_PROOF` 的结果进入阶段 C; `数值证据` / `猜想` / `开放` 显式标注且不进入形式化.

## 插件清单

| 插件 | 提供的 Skill | 定位与能力 |
| --- | --- | --- |
| `math-research-workflow` | 一体化工作流编排 | 编排层 (旗舰): 管理-研究-验证三阶段流水线, 子 agent 分工, 交接契约, 阶段边界 git 同步 |
| `rigorous-open-math-research` | 严格开放数学研究 | 求解执行层: 定理契约, 多路线搜索, 研究台账, 对抗性审计, 文献核验 (引用必须附链接且不得编造), 子 agent 分工 |
| `manage-math-research-program` | 数学研究项目管理 | 项目管理层: 工作区初始化, 文献策展, 开放问题组合, 工具库, 任务包派发, 已接受知识流水线 |
| `lean-verify` | Lean 4 形式化验证 | 验证层: 陈述保真审计, 机器验证 (lake build + sorry/axiom 扫描), 义务级独立审计, hash 绑定运行清单 |

依赖方向 (单向, 无反向调用):

```text
manage-math-research-program -> rigorous-open-math-research
math-research-workflow -> manage-math-research-program + rigorous-open-math-research + lean-verify
lean-verify 独立插件, 与其余 skill 互补
```

## 安装 (推荐: marketplace)

```bash
# 添加本仓库为 marketplace (仅需一次), marketplace 名为 math-research
codex plugin marketplace add xsoc1/rigorous-open-math-research

# 查看可用插件
codex plugin list

# 按需安装 (可只装需要的组件)
codex plugin add math-research-workflow@math-research
codex plugin add rigorous-open-math-research@math-research
codex plugin add manage-math-research-program@math-research
codex plugin add lean-verify@math-research
```

- marketplace 清单位于仓库根 `.agents/plugins/marketplace.json`.
- 安装后需新开一个 Codex 会话以加载插件 skill.

## 安装 (备选: skill-installer)

在 Codex 中使用 `$skill-installer`, 仓库路径分别为

- `xsoc1/rigorous-open-math-research/tree/main/plugins/rigorous-open-math-research/skills/rigorous-open-math-research`
- `xsoc1/rigorous-open-math-research/tree/main/plugins/manage-math-research-program/skills/manage-math-research-program`
- `xsoc1/rigorous-open-math-research/tree/main/plugins/lean-verify/skills/lean-verify`
- `xsoc1/rigorous-open-math-research/tree/main/plugins/math-research-workflow/skills/math-research-workflow`

或手动将对应 skill 目录复制到 `~/.codex/skills/` (Windows: `C:\Users\<用户名>\.codex\skills\`).
`manage-math-research-program` 自带 `MANIFEST.sha256` (sha256 逐文件校验清单), 修改后需重新生成.

## 仓库结构

```text
.
├── .agents/plugins/marketplace.json      # marketplace 清单 (插件顺序 = Codex 渲染顺序)
├── .github/workflows/validate.yml        # CI: 仓库级校验
├── plugins/
│   ├── math-research-workflow/           # 编排插件 (旗舰): 三阶段流水线编排
│   │   ├── .codex-plugin/plugin.json
│   │   ├── agents/openai.yaml
│   │   ├── assets/pipeline-handoff.template.md
│   │   └── skills/math-research-workflow/ (SKILL.md + references/workflow-design.md)
│   ├── rigorous-open-math-research/      # 求解执行层
│   ├── manage-math-research-program/     # 项目管理层
│   └── lean-verify/                      # 验证层
├── scripts/validate_all.py               # 本地校验入口 (与 CI 共用)
├── AGENTS.md                             # 仓库维护约定与会话记录
├── LICENSE
└── README.md
```

每个插件统一形态: `.codex-plugin/plugin.json` + `skills/<name>/SKILL.md` (+ 可选 `agents/`, `assets/`, `scripts/`, `references/`, `examples/`).

## 校验

```bash
# 本地校验: marketplace + 全部插件 + SKILL frontmatter + MANIFEST + UTF-8/BOM
python scripts/validate_all.py
```

push / PR 时 GitHub Actions 自动运行 `scripts/validate_all.py`.

## 使用

| 场景 | 调用 |
| --- | --- |
| 数学项目 研究+验证 全流程 (含子 agent 分工) | `$math-research-workflow` |
| 单个数学问题 (证明/反例/构造/审计) | `$rigorous-open-math-research` |
| 长期项目/文献/工具库/任务包/知识库维护 | `$manage-math-research-program` |
| Lean 4 形式化验证 | `$lean-verify` |

- 若项目根目录是 git 仓库, skill 会自动检查并保持仓库同步 (会话开始 `git status`/`git fetch`, 阶段收尾提交并推送), 详见 `manage-math-research-program/references/git-sync.md`.
- 所有研究结论遵循严格性标注: `严格证明` / `数值证据` / `猜想` 显式区分, 未完成严格证明的断言不标为 "已解决".

## 同步

- 父仓库: `xsoc1/rigorous-open-math-research`
- fork 副本: `Zhongshan-Big-Jun/rigorous-open-math-research` (同步方式: push 父仓库后, 在 fork 上执行 GitHub 的 Sync fork / merge-upstream)

## 版本历史
- 2026-08-12: AI4Math V2 方法蒸馏: 三 skill 新增发散检索契约/验证者自动 FAIL 清单/失败路由/陈述冻结/sorrifier/四道闸/首错定位/收敛检查/边际收益演化 (cachebuster `0.1.0+codex.20260812030804`).
- 2026-08-12: 编排为工作流插件仓库: 统一插件元数据, 补 workflow agents, marketplace 排序, 新增 LICENSE/校验/CI/AGENTS.md (cachebuster `0.1.0+codex.20260811160208`); 修复 lean-verify agents YAML, 校验器加严格 YAML/JSON 检查 (cachebuster `0.1.0+codex.20260812012356`); validate_all 68 项全绿.
- 2026-08-11: 编排为标准 marketplace (名 `math-research`, cachebuster `0.1.0+codex.20260811`); 新增 `math-research-workflow` 编排插件, 新增 `lean-verify` 插件; rigorous 新增子 agent 分工 + arXiv 语义检索 + 结构化验证输出.
- 2026-08-10: MRP 新增自动 git 仓库同步检查 (工作流第 0 步 + Rigor Phase 0/10/12).
- 2026-08-09: 蒸馏 Blueprint v2.2 数学工具包, 整合进两个 skill.
- 2026-08-05: `rigorous-open-math-research` 迭代自 `rigorous-mathematical-research`; 建立 `manage-math-research-program`.

## 版权与免责声明

- 版权归属: 本仓库的编排结构, 提示词组织, 文档与脚本由作者整合撰写, 按 MIT 许可分发 (见 `LICENSE`); 但其中的工作方法大量参考/改编自公开研究与开源项目 (如 MMAT, LeanMarathon, MechMath, M2F, FaithSieve, FormalRx, Archon-Horizon, EvE 等), 方法本身的思想与协议不归本仓库所有.
- 方法来源: 各 SKILL.md 的 Changelog 已附来源链接 (MMAT, LeanMarathon, MechMath, M2F, FaithSieve, FormalRx, Archon-Horizon, EvE, Blueprint v2.x 等), 引用以链接与要点转述形式呈现, 未复制受版权保护的论文正文或专有代码; 若署名或归属有误, 欢迎指正, 我们会在确认后修正.
- 第三方名称: 文中出现的项目, 组织与商标名称归各自所有者, 与本仓库无隶属或背书关系.
- 使用风险: 本仓库按"现状"提供, 不保证无缺陷; 生成的研究结果, 证明, 代码与结论须由使用者独立核验后再使用, 作者不对任何直接或间接损失负责, 内容不构成专业或法律意见.
