# AGENTS.md

## 仓库定位

工作流插件仓库 (Codex marketplace, 名 `math-research`): 4 个插件组成 管理-研究-验证 一体化数学研究工作流.

## 目录结构

- `.agents/plugins/marketplace.json` — marketplace 清单 (插件顺序 = Codex 渲染顺序)
- `plugins/<plugin-name>/` — 每个插件: `.codex-plugin/plugin.json` + `skills/<skill-name>/SKILL.md`
- `scripts/validate_all.py` — 仓库级校验入口 (本地与 CI 共用)
- `.github/workflows/validate.yml` — CI 校验

## 维护规则

1. 每次变更后运行 `python scripts/validate_all.py` (Python 3.10+, 建议 `PYTHONUTF8=1`).
2. 修改 `skills/<name>/` 内文件后, 若该 skill 带 `MANIFEST.sha256`, 必须重新生成并提交 (sha256 逐文件).
3. 修改插件元数据后, 用 plugin-creator 的 `update_plugin_cachebuster.py` 更新版本 cachebuster (`0.1.0+codex.YYYYMMDDHHMMSS`).
4. marketplace 插件顺序即 Codex UI 渲染顺序; 编排插件置顶, 新增插件追加到列表末尾.
5. 所有文本文件 UTF-8 无 BOM, 换行 LF (`.gitattributes` 已强制).
6. 同步顺序: 先 push 父仓库 `xsoc1/rigorous-open-math-research`, 再用 GitHub merge-upstream 同步 fork `Zhongshan-Big-Jun/rigorous-open-math-research`.
7. 如实记录: 不编造验证结果, 无法验证的能力明确标注为未验证.

## 会话记录
### 2026-08-12 会话: AI4Math V2 工作方法蒸馏采纳 (三个 skill 增强)

- 任务: 把 AI4Math V2 蒸馏路线图逐条写进 rigorous-open-math-research / manage-math-research-program / lean-verify 三个 SKILL.md.
- rigorous 新增: Phase 2 发散式检索契约 (宽搜索不守门, 来源诚实三要素, 分层流水线); Phase 8 首次见证验证者标准 + 14 类自动 FAIL 模式 + 首错定位与错误层分类; Phase 9 最小责任失败路由; Phase 10 陈述冻结 / sorrifier 分解 / 四道闸 + 人工语义复核; Phase 12 新鲜上下文收敛检查; Verifier 角色 prompt 更新.
- manage 新增: 第 3 节发散式检索契约 + 原始源不可变存储与知识卡片; 第 5 节证据状态行 + 边际收益演化规则; 第 8 节 5b 失败入档分类; 第 9 节新鲜上下文收敛检查.
- lean-verify 新增: Phase 3 四道闸 + 人工语义复核 + 修复策略 (陈述冻结/sorrifier/错误分类四步); Phase 4 首错定位与错误层分类; 结构化输出与 schema 新增可选 first_error 字段 (additionalProperties=false 下可选, required 不变).
- 各 SKILL.md 追加 Changelog (2026-08-12), 方法来源全部附链接 (MMAT/LeanMarathon/MechMath/M2F/FaithSieve/FormalRx/Archon-Horizon/EvE).
- 版本: 三个插件 cachebuster 更新为 0.1.0+codex.20260812030804; manage MANIFEST.sha256 重新生成 (43 条); 全局 skill 副本已同步; validate_all 68 项全绿.
- 已 push 父仓库, 并 merge-upstream 同步 fork Zhongshan-Big-Jun/rigorous-open-math-research; 本机 market math-research 已刷新重装.
- 后续: README 版本历史简化合并 (11 条 -> 6 条), 内容不变.
- 后续: README 新增「版权与免责声明」一节; 按用户指正修正原创表述 - 编排整合为原创 (MIT), 工作方法大量参考/改编自公开项目, 各 SKILL.md Changelog 附来源链接, 署名有误可指正.
### 2026-08-12 会话: 仓库结构复验与收尾

- 核对 GitHub 拓扑: 父仓库 `xsoc1/rigorous-open-math-research` (User, fork=false), fork `Zhongshan-Big-Jun/rigorous-open-math-research` (Organization), 双方 main 同一提交 (3d02ab6).
- 复验: `python scripts/validate_all.py` 68 项全绿; 临时 CODEX_HOME 冒烟通过 (marketplace add 本地克隆 -> 4 插件全部 installed/enabled, 均为最新 cachebuster: workflow 20260811160209, rigorous/manage 20260811160208, lean-verify 20260812012356).
- 清理 `scripts/validate_all.py` 死代码: 模板掩码第一次赋值被第二次覆盖, 已移除.
- 本机市场 `math-research` 刷新 (`codex plugin marketplace upgrade`) 并重装 4 插件至最新版本.
- 已 push 父仓库, 并同步 fork `Zhongshan-Big-Jun/rigorous-open-math-research`.

### 2026-08-12 会话: 仓库编排为工作流插件仓库

- 统一 4 个插件 `plugin.json` 元数据 (字段顺序, developerName 全部为 xsoc1, 修复 manage 描述丢字与 workflow 描述中英混杂).
- 补齐 `math-research-workflow` 的 `agents/openai.yaml` (与其他插件一致).
- marketplace 顺序调整为编排插件 `math-research-workflow` 置顶 (旗舰).
- 插件版本 cachebuster 更新为 `0.1.0+codex.20260811160208` (plugin-creator update_plugin_cachebuster.py).
- 新增 `LICENSE` (MIT), `scripts/validate_all.py`, `.github/workflows/validate.yml`, 根 `AGENTS.md`.
- README 重写: 流水线 mermaid 图, 仓库结构树, 校验与同步说明; 修正 lean-verify / workflow 插件 README 中的 marketplace 名 (`personal` → `math-research`).
- 验证结果: validate_plugin x4 通过, quick_validate x4 通过, MANIFEST.sha256 43 条全匹配, validate_all 全绿.
- 已 push 父仓库 `xsoc1/rigorous-open-math-research` (80b438c), 已通过 merge-upstream 同步 fork `Zhongshan-Big-Jun/rigorous-open-math-research` (fast-forward).

### 2026-08-12 会话: 编排收尾核对与修复

- 核对 GitHub 拓扑: `xsoc1/rigorous-open-math-research` = 父仓库 (fork=false), `Zhongshan-Big-Jun/rigorous-open-math-research` = fork, 与 README 一致.
- 发现并修复真实缺陷: `plugins/lean-verify/agents/openai.yaml` 的 `long_description` 末尾裸冒号导致严格 YAML 解析失败 (pyyaml); 已改写消除裸冒号.
- 强化 `scripts/validate_all.py`: 新增严格 YAML 解析 (PyYAML 可用时, 缺失则提示跳过) 与模板感知 JSON 校验 (掩蔽 `{{...}}` 占位符后解析; 模板设计上允许占位符); 本地 68 项检查全绿.
- CI `.github/workflows/validate.yml` 增加 `pip install pyyaml`, 保证严格 YAML 检查在 GitHub Actions 上生效.
- lean-verify 插件版本 cachebuster 更新为 `0.1.0+codex.20260812012356` (plugin-creator update_plugin_cachebuster.py).
- 端到端冒烟: 临时 CODEX_HOME + codex CLI 添加本地 marketplace `math-research` 并安装 4 插件, 全部 installed/enabled; lean-verify 以新 cachebuster 安装成功.
- 已 push 父仓库, 并 merge-upstream 同步 fork `Zhongshan-Big-Jun/rigorous-open-math-research`.

### 2026-08-12 会话: 根 README 新增英文版 README_EN.md 并同步双仓库

- 任务: skill 仓库 (父仓库 `xsoc1/rigorous-open-math-research`) 附加英文版 README.
- 完成:
  - 新增 `README_EN.md`: 中文 README 全文英译, 结构与口径完全一致 (工作流总览/插件清单/依赖方向/安装 x2/仓库结构/校验/使用/同步/版本历史/版权与免责声明), 协议标签 (已证/CANDIDATE_COMPLETE_PROOF/数值证据/猜想/开放) 保留原样并附英文说明.
  - `README.md` 顶部新增互链 `English: [README_EN.md](README_EN.md)` (英文版顶部对应 `中文版: [README.md](README.md)`).
  - 内容未改动 (仅翻译); 无公式, 无需 LaTeX 渲染; 版权与免责声明口径与中文版一致.
  - 校验: `python scripts/validate_all.py` 全绿; UTF-8 无 BOM, LF.
  - 已 push 父仓库, 并 merge-upstream 同步 fork `Zhongshan-Big-Jun/rigorous-open-math-research`.
  - 更正: 上行的 "merge-upstream" 表述不准确 - 实际为直接 push 同步 fork (双方 main 同提交 f86f81c, 与 merge-upstream 结果等价).

### 2026-08-13 会话: 编排层确定性门禁 + CI 行为冒烟

- 任务: 把工作流最脆弱的两处从 prose/checklist 下沉为可机器验证的机制: (1) 新增确定性阶段门禁校验器; (2) 为 lean-verify 脚本与门禁脚本接 CI 冒烟.
- 完成:
  - 新增 `plugins/math-research-workflow/scripts/validate_pipeline.py` (stdlib-only): 校验任务包必填字段与未填充模板占位符 (TASK-ID/PROJECT-ID/PROBLEM-ID/RUN_ROOT), 任务类型枚举, Source bundle 哈希绑定, 运行清单 JSON 与 task_packet_sha256 绑定, lean-proof/run-manifest.json 的 input_hashes 绑定, 可选 `--check-git`/`--allow-dirty`, 默认形式化门禁状态 `已证`/`CANDIDATE_COMPLETE_PROOF` (门禁外状态只 warn 不 promote). 不替代 solver/audit/verifier 的语义判断.
  - workflow `SKILL.md` 与 `README.md` 更新: Stage A 增加门禁脚本步骤, 阶段边界增加硬 FAIL 规则, Reference files 与组成清单补充脚本.
  - 新增 `tests/fixtures/lean-minimal/` (含 sorry + axiom + 干净定理), `tests/fixtures/pipeline-good/` (含哈希绑定的 Source bundle), `tests/fixtures/pipeline-bad/` (未填充占位符).
  - 新增 `tests/smoke_lean_verify.py` 与 `tests/smoke_pipeline_gate.py`; `.github/workflows/validate.yml` 新增 `smoke` job (两个脚本).
  - 本地验证: `validate_all.py` 68 项全绿; 两个 smoke 均通过 (lean-verify 命中 sorry+axiom 共 2 条, 坏 fixture 门禁 exit!=0).
- 备注: 未修改任何 plugin.json 元数据, 因此无需更新 cachebuster; 新增脚本/测试不影响 MANIFEST.sha256 (该清单仅属 manage 插件).
- 待办: 后续可把门禁脚本接到状态标签单点化 (`assets/status-vocabulary.json`) 与跨阶段 lineage.json; 本会话未实施这两项.
- 维护: 本文件追加会话记录; 提交后 push 父仓库并直接 push 同步 fork.
- 补记: 更新日志已补 - 根 `README.md`/`README_EN.md` 版本历史新增 2026-08-13 条目; workflow `SKILL.md` 新增 `## Changelog (2026-08-13)` 条目 (此前 workflow SKILL 无 Changelog).

### 2026-08-13 会话: README 优化 (版本历史精简 + 冒烟命令可发现)

- 任务: 按"更新日志写简洁点"的要求做仓库级小优化.
- 完成:
  - 根 `README.md`/`README_EN.md` 版本历史压成逐条一句话, 移除 cachebuster 噪音, 保留功能要点; 中英两版口径一致.
  - workflow `SKILL.md` 的 Changelog 由三句压成一句要点.
  - 两版 README 的校验段补充 `tests/smoke_lean_verify.py` 与 `tests/smoke_pipeline_gate.py`, 冒烟测试从 CI 后台变成用户可发现/可本地运行.
- 维护: 本文件追加会话记录; `validate_all.py` 68 项全绿; 提交后 push 父仓库并直接 push 同步 fork.

### 2026-08-13 会话: workflow 插件 cachebuster 刷新 + 本地安装

- 任务: 用户发现本地 Codex 未安装 workflow 插件, 要求安装; 因插件 SKILL/README/scripts 内容已更新而版本未动, 按要求刷新 cachebuster.
- 完成:
  - 本地诊断: `math-research` marketplace 已配置但 4 插件均 not installed; 市场检出已是最新 `95a96f6`.
  - 本地安装: `codex plugin add math-research-workflow@math-research` -> installed, enabled.
  - cachebuster: `update_plugin_cachebuster.py` 将 workflow 版本刷新为 `0.1.0+codex.20260812164950`; 根 README 两版版本历史与 workflow SKILL Changelog 同步标注.
  - 重装: marketplace upgrade 后 `codex plugin add math-research-workflow@math-research` 以新版本生效.
  - 校验: `validate_all.py` 68 项全绿; 提交后 push 父仓库并直接 push 同步 fork.
