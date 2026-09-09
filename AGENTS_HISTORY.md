# Maintenance history

Archived from AGENTS.md on 2026-09-05. Historical versions and commands may be superseded by current AGENTS.md rules.

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
### 2026-08-13 会话: workflow 插件加固 (环境自检 + 数值证据纪律门禁)

- 任务: 用户反馈审计中反复出现数值证据冒充严谨证明的问题 (agent 自发用数值
  检验代替数学论证交付), 要求通过插件更新解决; 同时确认范围 - fork 同步与发布
  工具化属于仓库管理, 不进工作流插件; 项目级 fork 同步归 manage skill 且必须
  通用 (个人自 fork 只是配置实例).
- 完成 (workflow 插件, cachebuster `0.1.0+codex.20260813054312`):
  - 新增 `plugins/math-research-workflow/scripts/doctor.py` 环境自检: 检查
    workflow 插件与三个依赖 skill 是否 installed/enabled, 市场是否注册,
    config.toml 启用条目是否完好; 硬 FAIL 时打印精确修复命令; 支持
    `--list-file` (离线/测试) 与 `--json`. 针对性防护桌面应用重写
    config.toml 抹掉启用条目的复发问题 (2026-08-13 已发生两次).
  - `validate_pipeline.py` 新增数值证据纪律 (硬门禁):
    (a) gate 状态 (`已证`/`CANDIDATE_COMPLETE_PROOF`) 的 run 必须携带
    candidate_proof.md 或 audit_report.md; (b) 数值标签与强声明
    (`已解决`/`定理已证`/`CANDIDATE_COMPLETE_PROOF`/`FORMALLY_VERIFIED`)
    同块出现时必须带严格标签 (`严格证明`/`定理已证`/`STRICT`/`机器验证`/
    `形式化验证`) 或显式降级声明 (evidence only / not constitute proof /
    仅佐证 / cross-check only / no ... evidence ... used as), 否则 FAIL;
    (c) verification.json verdict=FORMALLY_VERIFIED 必须有
    machine.build_passed=true 且 sorry/axiom 命中为空; (d) STATUS.md 声称
    FORMALLY_VERIFIED 时必须有 verification.json.
  - 修复旧 bug: lean-proof/run-manifest.json 的 input_hashes 基准目录改为
    manifest 所在目录 (lean-proof/), 且路径兼容 Windows 反斜杠分隔符
    (此前对真实项目一直误报 referenced file missing).
  - SKILL.md: Stage A 增加 doctor 前置检查; Stage B 增加数值证据纪律硬规则
    (数值只作探索/反例/佐证, 不单独支撑交付状态; 审计 agent 必须 FAIL 并报
    缺失义务); fork 具体表述删除, 改为引用 manage skill 的通用远程拓扑配置;
    Changelog 与 Reference files 同步.
  - 插件 README.md: 组成/使用更新 + 新增 "常见问题: 插件消失或未启用" 排障
    章节 (原因: config.toml 被应用重写; 修复: plugin add 或应用面板重新启用).
  - 测试: 新增 `tests/fixtures/pipeline-numerical-abuse` 与
    `tests/fixtures/pipeline-gate-noevidence`; smoke_pipeline_gate.py 断言两类
    FAIL 触发; 新增 `tests/smoke_doctor.py` (伪造 plugin list 全健康/缺插件两
    场景, 断言修复命令); CI smoke job 接入 doctor.
- 真实项目回归 (F:\LaTeX\BVE research): 门禁从 31 FAIL 降到 0 FAIL. 过程中
  发现并就地更正历史工件 R-20260806T140000Z-keylemmaaudit-2F83B1/
  candidate_proof.md 缺严格标签 (数值网格检查未声明仅作佐证), 已在文件头补
  STRICT + do not constitute proof 声明, 未改任何数学内容; 其余历史 FAIL
  均为 "evidence only"/"cross-check only"/"no evidence used as a result"
  等显式降级声明, 门禁词表已覆盖, 转为温和 warn (建议补严格标签).
- 校验: validate_all.py 全绿; 三个 smoke 本地全过; 真实项目门禁 0 FAIL.
- 维护: 本文件追加会话记录; 提交后先 push 父仓库 origin (xsoc1), 再直接
  push 同步 fork (Zhongshan-Big-Jun).
### 2026-08-13 会话: manage skill 通用远程拓扑 + 历史工件严格标签收尾

- 任务: 承接上一会话, 执行两项遗留 - (1) manage skill 通用化多远程同步 (用户
  明确个人自 fork 只是配置实例, 不得写死); (2) 历史工件 o1revise-2ED02A 补严格
  标签 (门禁 warn 建议).
- 完成 (manage 插件, cachebuster `0.1.0+codex.20260813093832`):
  - 新增 `scripts/sync_remotes.py` (通用, stdlib-only): 从 project.json 读可选
    `git_sync.push_order` (默认 ["origin"]), 按顺序 push 当前分支到各 remote,
    每次 push 后核对 HEAD == <remote>/<branch>; dirty 工作树默认 FAIL
    (--allow-dirty 转 warn, 绝不覆盖未提交工件); 支持 --dry-run/--json.
  - `references/git-sync.md` 重写 Parent-fork 专名部分为通用多远程规则: 删除
    写死的 xsoc1/Zhongshan-Big-Jun 仓库名与本地 staging 路径; "父先子后" 变为
    push_order 配置实例; fork 关系丢失恢复步骤保留但用 <owner>/<repo> 占位.
  - SKILL.md 第 0 步: 提交后若 project.json 声明 git_sync.push_order 则按顺序
    推送全部 remote 并记录顺序与 commit hash; project.template.json 增加可选
    git_sync.push_order 字段 (默认 ["origin"]).
  - MANIFEST.sha256 重新生成 (44 文件, 含新脚本); 仓库根新增 project.json
    (push_order ["origin","fork"]) 作为该通用机制的配置实例.
  - 测试: 新增 tests/smoke_sync_remotes.py (本地 bare repo 双 remote, 验证
    推送顺序与 dirty 树 FAIL, 无网络依赖); CI smoke job 接入.
- 历史工件收尾 (Sturm-Liouville 项目): o1revise-2ED02A 的 audit_report.md 与
  research_ledger.md 补 STRICT 声明行 (proof-level claims argued analytically /
  proofs live in candidate_proof.md; 不改任何数学内容); 项目门禁重跑 0 FAIL
  (6 个 gate 外状态 warn 属正常).
- 校验: validate_all.py 68 项全绿; 四个 smoke (doctor/pipeline/sync_remotes/
  lean-verify) 本地全过; sync_remotes.py 对 skill 仓库 dry-run 行为正确.
- 维护: 本文件追加会话记录; 提交后按 project.json 的 push_order 先 push
  origin (xsoc1, 父) 再 push fork (Zhongshan-Big-Jun, 子).

### 2026-08-13 会话 (Stage B0 新颖性前置门禁 + CI failure 修复)
- 任务: (1) 按用户要求把 "open 判定 + novelty audit" 提升为 workflow Stage B
  的显式前置门禁, 检索结论回填 manage literature 快照并哈希防漂移;
  (2) 排查 xsoc1/rigorous-open-math-research 的 GitHub Actions failure.
- Stage B0 门禁 (workflow cachebuster 0.1.0+codex.20260813101438):
  - SKILL.md 新增 Stage B0 -- Openness and novelty preflight (强制, dispatch 前):
    open 判定 (Phase 0/1, 除非用户要求 blind benchmark) -> 发散式新颖性审计
    (query -> result -> locator 来源诚实, 付费墙/摘要级如实标注) -> 文献快照
    回填 (manage literature frontier + 快照哈希绑定, SNAPSHOT_MISMATCH 重取)
    -> 门禁放行 (包内须有 verdict + audit path 或显式 skip + snapshot hash).
  - validate_pipeline.py 机械拦截: solve/disprove/construct 任务包必须携带
    `## Novelty preflight (B0)` 区块 (Openness verdict / Novelty audit path /
    Snapshot hash), 缺失或占位符即 hard FAIL; 4 个 gate fixtures 同步补齐.
  - manage: task-packet.template.md 新增 Novelty preflight (B0) 区块与填写
    说明; SKILL.md 第 6 节任务包要素增加 B0 一节; manage plugin.json 版本
    同步为 0.1.0+codex.20260813101438; MANIFEST.sha256 重新生成.
- CI failure 排查与修复 (根因均为平台/环境差异, 非逻辑错误):
  - failure 1 (validate job, 自 f373971): MANIFEST.sha256 在 Windows CRLF
    工作树字节上生成, 而 git 按 .gitattributes eol=lf 存储, Linux CI checkout
    为 LF -> validate_all.py 字节级哈希校验失败. 修复: validate_all.py 校验前
    规范化 CRLF (replace \r\n -> \n) 再哈希; MANIFEST.sha256 按 LF 规范化
    内容重新生成 (44 文件, 双基准均匹配).
  - failure 2 (smoke job, 自 d4cc8b0): smoke_doctor.py 硬断言 doctor 输出
    "config.toml enables", 但 CI runner 无 ~/.codex/config.toml (doctor 只
    warn), 本地有配置故本地通过. 修复: 断言放宽为 "0 problem(s)" + "installed
    and enabled" (doctor 无 FAIL 即健康).
  - 修复后本地验证: validate_all.py 68 项全绿; smoke_lean_verify /
    smoke_pipeline_gate / smoke_doctor / smoke_sync_remotes 全部通过.
- 根 README 版本历史 (中英) 追加 2026-08-13 条目.
- 维护: 本文件追加会话记录; 提交后按 project.json 的 push_order 先 push
  origin (xsoc1, 父) 再 push fork (Zhongshan-Big-Jun, 子).
### 2026-08-13 会话 (workflow 中断交接功能)
- 任务: 给工作流插件加"交接未完成工作"功能 - 工作做一半中断时, 后续 agent
  能接上进度, 记录已尝试的方法和路线.
- 完成 (workflow cachebuster 0.1.0+codex.20260813144928):
  - 新增 assets/interruption-handoff.template.md: 中断交接模板, 含 run/packet
    ID, 中断原因 (RESOURCE_BOUND/USER_REQUEST/TOOL_FAILURE/UNKNOWN), 任务状态,
    已完成/未完成义务, 已尝试路线 (每条带 [FAILED|BLOCKED|PARTIAL|SUCCEEDED]
    结果标记与失败机制), 精确下一步, 关键文件路径+sha256, 恢复读序.
  - SKILL.md 新增 "Interruption handoff and resume (mandatory)" 协议: 中断前
    必写交接记录 -> manager 登记哈希 -> 后续 agent 按读序续接, 禁止无新理由
    重跑 [FAILED] 路线; 项目级恢复 (state/RESUME.md, checkpoint) 归 manage,
    本协议覆盖 run 级 (Stage B/C) 连续性.
  - validate_pipeline.py 机械门禁: 扫描 runs/**/handoff-interrupted-*.md,
    必填字段 (Run ID/Task packet ID/Date/Interrupt reason/Task state) 与必填
    区块 (Completed/Open obligations, Attempted routes, Next actions) 缺失或
    占位即 hard FAIL; 路线条目缺结果标记给 warn.
  - 测试: tests/smoke_handoff.py + fixtures pipeline-handoff-good/bad; CI
    validate.yml smoke job 接入.
  - workflow-design.md 新增 5.1 节; 插件 README 与根 README (中英) 版本历史
    更新.
- 校验: 本地 smoke_handoff 通过 (good 过, bad 因缺 Next actions/空 routes
  FAIL); 全套测试待提交前复跑.
- 维护: 本文件追加会话记录; 提交后按 project.json push_order 先 push origin
  (xsoc1) 再 push fork (Zhongshan-Big-Jun).
### 2026-08-14 会话: 蒸馏 OpenProver 方法进 workflow 求解循环

- 任务: 把 arXiv:2607.09217 (OpenProver, CICM 2026, Kripner & Straka,
  github.com/kripner/OpenProver) 的 Planner-Worker-Verifier 方法直接蒸馏进
  math-research-workflow 插件 (Stage B/C), 保留 B0 门禁与数值证据纪律.
- 完成 (workflow cachebuster 0.1.0+codex.20260814120000):
  - 新增 assets/whiteboard.template.md: 每 run 紧凑白板模板 (Run ID/Task
    packet ID/Last updated + Current plan/Route history/Ideas to return to/
    Open obligations/Key artifacts), 即 OpenProver Whiteboard + Repository
    (slug) 记忆模型的适配.
  - SKILL.md Stage B 新增 "OpenProver-style solve loop (distilled,
    mandatory)": 求解主导者 (Planner) 每步重写并读取 whiteboard; 独立并行
    Worker 互不见推理痕迹; 审计 agent 独立复核 Worker 产出 (verdict +
    critical errors + gaps + repair hints); 仓库按 slug 寻址且 Lean 片段仅
    机器验证通过后入库, 否则错误/警告回喂 Worker; Lean 实时验证回路三工具
    lean_verify / lean_search (LeanExplore, arXiv:2506.11085) / lean_store
    (上下文累积到 runs/<run_id>/lean_scratch/context.lean); 交互式人工引导
    (呈现计划/重定向 Worker/接受或拒绝下一步).
  - SKILL.md Stage C 新增 "Formalization feedback loop (mandatory)":
    Lean 失败按层分类修复, 证明层缺陷路由回求解主导者修 NL 证明后重形式化,
    不静默绕开.
  - validate_pipeline.py 新增 whiteboard 门禁: 扫描 runs/**/whiteboard.md
    硬校验必填字段与 5 个区块; 以 research_ledger.md 识别 Stage B 求解 run,
    2026-08-14 之后开始的 run 必须携带 whiteboard (解析 run 目录名 R-YYYYMMDD
    做 cutover, 存量 run 不追溯, 避免破坏历史记录).
  - 测试: tests/smoke_whiteboard.py + fixtures pipeline-whiteboard-good/bad
    (缺 whiteboard / 缺区块均 FAIL); CI validate.yml smoke job 接入.
  - references/workflow-design.md 新增 7.1-7.6 节 (Planner/仓库/独立性/Lean
    回路/反馈环/交互引导); 插件 README 与根 README (中英) 版本历史更新.
- 方法来源: OpenProver (arXiv:2607.09217, CC BY-SA 4.0), 仅协议转述, 未复制
  其代码或论文正文.
- 校验: 本地 smoke_whiteboard 通过; 全套校验 (validate_all + 5 个 smoke +
  真实项目门禁回归) 提交前复跑.
- 维护: 本文件追加会话记录; 提交后按 project.json push_order 先 push origin
  (xsoc1) 再 push fork (Zhongshan-Big-Jun); 最后本地 marketplace upgrade +
  plugin add 刷新已安装插件.
### 2026-08-16 会话: manage 新增人类可读 LaTeX 双语证明交付规范 (工作流 8c)

- 任务: 按用户要求给 manage-math-research-program 加一条规范 - Lean 验证之后,
  必须有存放 LaTeX 格式证明的文件夹, 供人类用自然语言阅读, 参考 arXiv 论文规范,
  中英两个版本.
- 完成 (manage 插件, cachebuster `0.1.0+codex.20260815170001`):
  - SKILL.md 新增强制工作流 8c "Deliver human-readable proofs as arXiv-style
    LaTeX (papers/)": Lean 验证通过 (FORMALLY_VERIFIED + build_passed + 零
    sorry/axiom) 的定理必须在 `papers/<SLUG>/` 交付 `<SLUG>-en.tex` (英文,
    arXiv 规范: amsart + amsthm/amsmath/hyperref, 标题/作者/日期/摘要/编号定理
    环境/带 DOI 或 arXiv 链接的参考文献, xelatex 零警告) 与 `<SLUG>-zh.tex`
    (中文对照, 同一陈述/证明结构/文献); 文档头绑定机器验证契约 (Lean 路径/
    验证提交哈希/lake build/零 sorry-axiom); 陈述必须与形式化一致, 人类证明是
    重述不是替代; STRICT vs EVIDENCE 标签纪律保留; 源 tex 哈希登记入 run 记录
    与工件索引.
  - 证据规则新增第 13 条 + 项目完成清单新增 papers/ 交付项.
  - `references/project-repository-spec.md`: 布局树新增 papers/, 所有权表新增
    manager 行, 完整性检查新增 papers 相关两项.
  - `scripts/init_project.py`: 新建项目创建 `papers/` 目录与 `papers/README.md`
    (规范说明); `scripts/validate_project.py`: REQUIRED_DIRECTORIES +
    REQUIRED_FILES 各加 papers 项.
  - 新增模板 `assets/proof-paper.template.tex` (可编译 amsart 骨架 + 形式化契约
    表格 + 证据纪律注释 + 中文版切换说明).
  - MANIFEST.sha256 重新生成 (45 条); 根 README 中英版本历史追加条目.
- 校验: validate_all 68 项全绿 (MANIFEST 匹配); 上游 tests 无 init/validate
  依赖, 冒烟不受影响.
- 维护: 本文件追加会话记录; 提交后按 project.json push_order 先 push origin
  (xsoc1) 再 push fork (Zhongshan-Big-Jun); 随后在 DSH 适配仓库重跑
  sync-from-parent.py 继承本变更.
### 2026-08-16 会话: 社区方法蒸馏第二轮 (四插件, 四方向)

- 任务: 按用户要求在 awesome-dsh-plugin 生态中寻找可改良本插件的方法/思想/工具,
  方向包括网络搜索 (arXiv 等确认问题状态)、多 agent 协作效率、Lean 验证、数学研究方法.
- 调研: 4 个并行子代理深挖 28 个仓库 README (全部 MIT/可蒸馏; dsh-eval-harness
  许可证未确认仅作思想参考). Top 来源: argo, modsearch, dsh-zotero, dsh-kb-sieve,
  dsh-web-search-pro, dsh-exa-mcp, dsh-suite plugin-team-board, dsh-proof,
  dsh-agent-team-gui, dsh-trajectory-governance, forge-gates, jacobian,
  dsh-rigorquant, Vibe-Mathematics, Aegis, dsh-science, dsh-scholar,
  dsh-design-skills, dsh-ops-kit, dsh-finance.
- 实施 (四插件 cachebuster 0.1.0+codex.20260815171704):
  - rigorous: phase-23 检索证据契约 (status 三态/uncertainty-warnings/引擎尝试/禁编
    造分数/本地文献有界片段+章节名引用/检索历史复用) + 目标问题状态确认小节
    (fetch_required, fetch status 四态, 分层确认, 证据强度排序启发, 缺口侦察清单,
    跨会话回填); phase-78 反例-only 对抗 + 双导线 ground-truth + 结构化输出新增
    covered_scope/residual_risk; phase-45 路线假说状态机 + forward-only + 循环检测;
    phase-01 Phase 0 fetch_required + 契约新增 Forbidden moves.
  - workflow: Stage B 义务认领 (claim before work) + 缺口回灌硬规则; Efficiency
    rules 并行失败聚合 + 循环检测; Stage C Lean 升级通道 (关键断言先 Lean 再落地).
  - lean-verify: Phase 3 单一结构化判定 gate 协议 + 原子/有界/无状态检查;
    Repair strategy 同缺口三轮收敛; 裁决证伪优先 (反例否决/不确定不通过).
  - manage: §3 检索证据契约 + 本地文献先查/历史复用; §5 工具溯源字段; 8b 新增
    第 8 条证据边界 (非受控输出不成为正式证据, 受控 run 冻结环境).
  - 补记: manage §5 追加工具晋升/退休触发规则 (3 次确认使用或 1 次机器验证证明
    晋升; 反模式 2 次确认失败退休) - 来自 dsh-task-planner.
  - 根 README 中英版本历史追加条目.
- 校验: validate_all 68 项全绿; MANIFEST 45 条重新生成; 冒烟不受影响 (无测试
  依赖被改动).
- 维护: 本文件追加会话记录; 提交后按 push_order 先 push origin (xsoc1) 再 push
  fork (Zhongshan-Big-Jun); 随后 DSH 适配仓库 sync-from-parent.py 继承 + README
  蒸馏表更新.
### 2026-08-16 会话: 优化方向落地 (fork 同步自动化)
- 任务: 用户选定优化方向后, 为父仓库补充 fork 同步自动化与本地脚本.
- 完成:
  - 新增 `scripts/sync-fork.sh`: 本地手动同步 origin -> fork (fetch/ff-only/push/verify).
  - 新增 `.github/workflows/sync-fork.yml`: push 到 main 后自动推送到
    Zhongshan-Big-Jun/rigorous-open-math-research; 需要仓库 secret `FORK_PAT`,
    未配置时 job 自动跳过.
  - 本地 `_xsoc1_work` 已从 323bfd8 fast-forward 到 3279e1a, 与远程 main 一致;
    `.gitignore` 增加 `verify_out/`.
- 校验: 父仓库 validate_all 待跑 (新增文件不影响插件 MANIFEST); DSH 适配仓库
  已同步最新 upstream 且 51 项校验/10 smoke 全绿.
- 维护: 提交后按 push_order 先 push origin (xsoc1) 再 push fork; fork 自动同步
  可选用 workflow (配置 FORK_PAT) 或本地脚本.
### 2026-08-16 会话: 轻量优先成本分级升级协议 (escalation ladder)
- 任务: 让 AI 研究问题先做轻量化小改动, 再按记录证据逐步升级到更困难复杂的做法.
- 完成:
  - 新增 `plugins/rigorous-open-math-research/skills/rigorous-open-math-research/references/escalation-ladder.md`:
    Tier 0 查与测 / Tier 1 小改动 / Tier 2 中等系统化 / Tier 3 重型并行;
    行动按信息增益/成本排序; 升级触发器 (two zero-gain / counterexample /
    load-bearing gap / user request); 重型失败回退机制; `escalation_ladder.md`
    运行级记录模板.
  - rigorous SKILL: Phase 索引与默认工件增加 escalation-ladder / escalation_ladder.md;
    Phase 4 route card 增加 `cost_tier` / `minimal_first_step` /
    `escalation_criteria`; Phase 5 增加第 0 步 cheapest admissible probe.
  - workflow SKILL: Stage B 增加 cost-tiered escalation (light first), 并行 fan-out
    视为 Tier 3, 白板模板增加 `current_cost_tier` / `last_escalation_reason`.
  - manage: 任务包模板与 SKILL 第 6 节增加可选 `Max cost tier` / `Escalation policy`.
- 版本: 四个插件统一 `1.2.0`; 根 README 中英版本历史新增 1.2.0 条目; 父仓库
  validate_all 68 项全绿, MANIFEST 重新生成 (51 条).
- 维护: 提交后按 push_order 先 push origin (xsoc1) 再 push fork; 随后 DSH 适配仓库
  sync-from-parent.py 继承 + package.json/README 版本同步.
### 2026-08-23 会话: 轻量 reuse 协议 (v1.3.0)
- 基于三轮受控插件性能实验 (A6 / B3 / DensBC O1') 落地轻量 reuse 协议:
  紧凑预扫描 (research_map + tools/README + LEMMA_INDEX + 最新 final/handoff),
  不再要求 per-route REUSE 标记; 每个实质 run 写 `reuse_summary.md` 并满足
  最低产物集; 新 STRICT/partial 结果必须补 Lean scaffold.
- 修改: workflow SKILL + references/reuse-protocol.md; manage SKILL §5;
  rigorous 默认工件; 四插件版本统一 1.3.0; README 中英版本历史.
### 2026-08-23 会话: 工具类作用域生命周期 (v1.4.0)
- 按用户意见, 工具退休/归档改为按问题类作用域: 工具在类 C 退休不影响类 D;
  全部类 retired 时进入 archived, 不删除, 显式检索仍可调用.
- 新增 scripts/manage_tool_lifecycle.py (list/status/set-class);
  tool-library-spec 与 tool-entry.template 增加 applicability/failure_records;
  workflow reuse-protocol 明确按类选择工具.
### 2026-08-23 会话: 性能可观测与示警 (v1.5.0)
- 新增 workflow `references/performance-observability.md`,
  `assets/performance-alert.template.md`, `scripts/performance_alert.py`.
- Stage B 运行后: 有 performance.json 则与可比 baseline 比较, 成本异常上升且
  产物/复用未改善时写 performance_alert.md 并在 final_report 向用户示警.
- 明确: 告警是候选, 单次实验可能误导 (reuse-gate 简单/困难问题不同权衡),
  需同问题类重跑或换类验证后再下结论.
### 2026-08-24 会话: Codex 入口上下文优化与 fence 修复 (v1.6.0)
- 四个 SKILL 的历史 changelog 移入 `references/changelog.md`, 入口总字节从
  124,443 降至 97,802 (-21.4%); rigorous 入口从 19,618 降至 11,184 (-43.0%).
- 修复 91293b0 渐进式拆分遗留的 rigorous Output protocol 断裂 fence;
  `validate_all.py` 新增 Markdown fence 与各 skill 入口上下文预算门禁.
- workflow 增加 Codex 索引发现, 目标切片读取, 有界 programmable batching,
  语义决策边界和 compaction 前 artifact 重建规则; 四插件统一升级 1.6.0.
- 修复 manage/workflow plugin.json 的中文 UI mojibake; smoke_doctor 隔离
  `CODEX_HOME`, 消除本机真实 config.toml 对离线 fixture 的污染.
### 2026-08-27 会话: benchmark 驱动的 closure-first 优化 (v1.7.0)
- 根据 pilot v5 实测定位调度冲突: light-first 协议要求 cheap probe, 但 agent 编排仍
  默认多路线与持续全局审计, 导致承重义务未定位前发生高成本 fan-out.
- rigorous 新增 closure-first 协议与模板: coordinator 先直接求解并廉价证伪首个
  承重义务, spawn 必须声明可改变的决策, 后续轮次必须返回 `decision_delta`.
- workflow Stage B 同步门禁; 空白/重复/no-delta 返回不再购买独立全局审计;
  load-bearing 与可复用结果仍保持独立审计. rigorous/workflow 升级 1.7.0.
- 新增 `tests/smoke_closure_first.py`, 固定协议入口, 模板字段, workflow 继承与版本
  绑定, 防止后续维护重新引入调度冲突.
### 2026-08-28 会话: fast-close 结构化证书 (v1.8.0)
- 用户在 pilot v6 三臂完成后要求继续优化插件, 并明确要求同步维护
  `docs/pipeline-full-flow.md`. 本轮不启动新的高耗额数学 arm.
- 根据 v1.6/v1.7/v1.8 benchmark 现象, 将 root obligations 闭合后的 Stage B 收口
  固化为 fast-close: canonical `obligation_graph.json` 与
  `completion_manifest.json` 冻结 contract, graph, proof, dependencies 和 root
  anchors; 不同 reviewer 的 `completion_audit.json` 必须绑定 manifest 且零缺口 PASS.
- 新增确定性校验和对抗 smoke: root 集合精确相等, proof anchor 实存,
  reviewer 独立, freeze/review 时间顺序, hash/path 安全, non-PASS 拒绝,
  同一 manifest 仅一个 completion audit, post-cutover 缺 gate 拒绝.
- STOP 后禁止追加 Stage B 研究模型调用. 唯一可选 frontier call 使用独立
  `frontier_upgrade.json`, 绑定原证书与 path/hash/locator 授权, sequence 1,
  正整数预算和停止条件; 同一 base certificate 只能使用一次.
- `docs/pipeline-full-flow.md` 已改为 closure-first 主线并纳入 smoke markers.
  发布前门禁: validate_all 81/81, 7 CI smoke, plugin validators, skill validators
  与 diff check 全部通过; 独立前向审查的两轮 P1 反例均已转成回归用例.
### 2026-08-29 会话: quota-safe interruption recovery (v1.9.0)
- 用户要求在五小时额度中断前建立低开销恢复机制, 并继续插件优化.
  本轮不重跑数学 benchmark arm, 避免将发布开销混入计分实验.
- 新增确定性 `scripts/checkpoint_resume.py` 和
  `assets/interruption-state.template.json`: 通过 canonical state, immutable checkpoint,
  unique resume receipt 与 contiguous predecessor chain 保存数学前沿,
  do-not-repeat 集合, exact action ID 和最小读取集.
- 计分实验续段必须保持 arm/task/workspace/prompt/harness/source/gold 绑定,
  有限非负的累计 response/tool/token/wall/cost 指标, 且不得丢失已完成义务.
  结果状态升级需新证据, 新审计和显式 transition.
- 在途 worker 不得静默消失. 恢复首动作必须为 `RECONCILE_INFLIGHT`,
  后续状态通过 `inflight_reconciliation` 和 hash-bound evidence 记录
  `INGESTED`, `INTERRUPTED` 或 `NO_RETURN`.
- 维护 `docs/pipeline-full-flow.md`, workflow/rigorous 入口, 设计文档,
  handoff 模板, changelog, README 和 CI. 新增对抗
  `tests/smoke_checkpoint_resume.py`, 覆盖跨段指标重置, arm 更换,
  双 receipt, transcript 回放, NaN, 时间倒置, 在途 worker 丢失,
  verify/write TOCTOU, 隔段旧 proof/audit 回放, 旧字节改名和 proof/audit 同工件别名.
- 当前门禁: validate_all 81/81, 8 CI smoke, 2 plugin validators,
  2 skill validators, Python compile 与 `git diff --check` 全部通过.
  Windows 上 skill quick validator 显式使用 `PYTHONUTF8=1` 避免 GBK 解码污染.
- 独立前向审查逐轮构造的 predecessor, receipt, metric, action,
  read-set, worker session, TOCTOU 与 lineage alias 反例均已转成回归;
  最终复审 PASS, 无新 P1/P2.
### 2026-08-30 会话: checkpoint recovery usability (v1.10.0)
- 根据真实 v1.9 live recovery 暴露的失败优化确定性 CLI. 新增 `advance` 命令:
  verify predecessor pair 后自动把 checkpoint-bound `whiteboard` 和
  `closure_gate` 复制为下一 sequence 路径, 重写 binding, 写带
  `advance_draft=true` 的 next state; 未完成 draft 不可 seal, 原 checkpoint
  保持可验证.
- 修复 project-prefixed cwd-relative path 被 project root 重复拼接, 支持
  PowerShell 7 位 fractional timestamp, 增加 canonical UTC timestamp/default.
  新增 typed `REFINES`/`SUPERSEDES` obligation lineage, 新 gap 可重命名继承
  predecessor, 自动退休并跨 receipt 传播旧 action, 无需保留旧 open ID 或手工
  补 `do_not_repeat`.
- 维护 workflow/rigorous SKILL, changelog, README 中英版与
  `docs/pipeline-full-flow.md`; rigorous/workflow 升级 1.10.0.
- 回归: 扩展 checkpoint smoke 覆盖三类真实缺陷和 advance guard. 11 个 smoke
  全过, validate_all 81/81, 2 plugin validators, 2 UTF-8 skill validators,
  py_compile 与 diff check 全过. 对 v1.9 G1 prime live artifact 做无模型 replay:
  sequence 01 仍 `READY`, advance sequence 02 成功, 两个 copy hash 相等,
  原 checkpoint 不变, draft seal 按预期拒绝.
### 2026-08-30 会话: scoped pipeline validation (v1.11.0)
- workflow `validate_pipeline.py` 新增 `--scope <relative-logical-root>`:
  scope 必须是带 `project.json` 或 `blueprint-project.json` 的自包含逻辑项目根;
  discovery, source/task/formalization/hash/checkpoint binding 和 git pathspec 均限制
  在该根内. absolute/escape/markerless/nested-git scope 预检失败, scoped PASS 明确
  不等于 whole-project PASS.
- 新增 `tests/smoke_scoped_pipeline.py` 与 CI 项, 并加固相对 source/formalization
  路径不可逃逸. 父仓库 validate_all 81/81, 12 个 smoke, plugin/skill validator,
  py_compile 与 diff check 均通过.
- BVE v1.9 G1 prime 隔离工作区直接校验和 scoped 校验均为 0 problem/2 warning;
  scoped git cleanliness PASS, BVE 全仓仍诚实报告 67 problem/20 warning. 当前安装
  环境未发现 active `runtime/blueprintctl.py`, 因而未运行或复制旧 project-local
  Blueprint tools; Blueprint v2.2 gateway/artifact-root 迁移留待网关可用后处理.
### 2026-08-30 会话: cross-root Tier 0 formalization handoff (v1.12.0)
- 新增确定性 `scripts/formalization_handoff.py`, 只接收 `formalization=scaffold`
  和 `copy_mode=exact` 的 Tier 0 Lean scaffold. immutable receipt 同时绑定 source
  run manifest, proof, source/destination scaffold, logical-root marker/project ID,
  destination registration anchors 和 seal-time hashes; path escape, nested git,
  overwrite, artifact 缺失, hash 漂移和 anchor 删除均 fail closed.
- 明确不支持完整 `formalization=requested` package, receipt 不提升数学状态且不得
  标为 `FORMALLY_VERIFIED`. Stage C 详细协议移入按需
  `references/stage-c-formalization.md`, 常驻 workflow SKILL 从 v1.11 的 31,931
  字节降至 27,619 字节, 同时完整保留决策, verification tier, dual-track audit,
  reuse, supersession, escalation 和 repair 规则.
- 新增 `tests/smoke_formalization_handoff.py`, 父仓库 validate_all 81/81 和全部
  13 个 smoke PASS; plugin validator, UTF-8 skill validator, py_compile 和
  `git diff --check` PASS. WindowsApps `python.exe` 是返回 9009 的占位程序,
  本轮固定使用 `py -3`, skill quick validator 使用 `-X utf8`.
### 2026-08-30 会话: canonical formalization consumption (v1.13.0)
- `formalization_handoff.py` 新增 `consume/verify-consumption`: receipt live
  `READY` 后只允许生成一个 canonical immutable sibling `FHC-<id>.json`, 绑定
  receipt path/hash, consumer logical root, consumption-time artifact hash 和已在
  receipt 中登记的 Stage C anchor. 未绑定 anchor, relocation 和 duplicate fail closed.
- consumption effects 固定为 mathematical/verification `UNCHANGED`. Stage C 后续
  合法修改 destination scaffold 不抹除 consumption history; receipt/source drift,
  project ID 变化, anchor 删除或状态伪升级仍失败. seal/consume 改用 exclusive-create,
  关闭 overwrite TOCTOU.
- workflow SKILL 仅 27,657/32,768 bytes; 详细语义在按需 handoff reference.
  validate_all 81/81, 13 smoke, plugin/skill validator, py_compile 和 diff check PASS.
### 2026-08-31 会话: Blueprint v2.2 active runtime gateway (v1.14.0)
- manage v1.7.0 新增 plugin-owned `runtime/blueprintctl.py`. 对存在
  `blueprint-project.json` 的项目先 `ensure` 一次, 绑定 runtime/layout/config,
  后续 canonical validate/query/proposal validation/integration 只走该入口.
- 修复内部 query 的跨根 artifact 解析和 receiver 对 project-local validator 的
  隐式依赖. BVE 精确隔离副本的 canonical validate, snapshot 和 artifact hash
  查询均 PASS, 未执行或复制项目内 Python tools.
- rigorous v1.11.0 的 Blueprint retrieval reference 同步切换到 active gateway,
  防止 Stage B 绕过 Stage A 的 layout/runtime 绑定.
- 新增 `tests/smoke_blueprint_gateway.py`, 覆盖 pre-ensure fail-closed,
  ensure 幂等, poisoned project-local validator, external artifact root,
  no-op proposal validation, layout escape 和 config mismatch.
- 维护 manage/workflow SKILL 与 changelog, README 中英版,
  `docs/pipeline-full-flow.md` 和 CI; workflow 升级 1.14.0.
- 父仓库门禁: validate_all 81/81, 14 smoke, 3 plugin validators,
  3 skill validators, py_compile 与 diff check 全部 PASS.
- 网关工具根同时解析 Codex plugin 布局与 DSH 扁平 skill 布局; 两者仍只调用
  同一份受版本绑定的插件工具, 不启用 project-local fallback.

### 2026-08-31 会话: checkpoint-current scoped validator 修复 (v1.14.1)
- BVE KP-DET 实跑暴露真实兼容缺口: sequence-00 whiteboard/closure 已被不可变
  checkpoint 绑定, `advance` 后当前状态位于 numbered artifacts, 但 workflow
  validator 仍只扫描祖先 basename, 误报 11 个格式问题.
- `validate_pipeline.py` 现在先验证每个 run 的最新 sealed checkpoint 全谱系, 再从
  其 state 选择当前 whiteboard/closure. 最新 checkpoint `STALE` 时 fail closed,
  禁止回退祖先; 无 checkpoint 的 run 维持原行为.
- checkpoint smoke 新增 legacy ancestor -> compliant versioned successor ->
  post-seal tamper 回归. 同步维护 quota reference, SKILL, README 中英版和
  `docs/pipeline-full-flow.md`; workflow 补丁版本升级为 `1.14.1`.
- BVE 实工件回归: 新 selector 正确选中 sequence-02 并暴露 12 个当前 schema
  缺口; 通过 deterministic advance 生成 sequence-03 后, scoped validator 为
  0 problem/1 expected warning. sequence 00-02 均保持可验证.

### 2026-09-05 会话: 当前 Codex 性能优化方案
- 用户要求结合 BVE 本体与插件的维护记录和 benchmark 标准提出方案. 核查远端快照, 本地 Codex/skill 来源, 历史预注册, 指标实现与调度规则, 新增 `docs/codex-performance-optimization-plan-2026-09-05.md`. 后续性能维护先读该方案, 按同模型基线, 指标统一, 条件读取和独立审计质量门禁推进. 本轮仅文档, 未改插件行为或安装配置, 未运行新数学 benchmark.
- 用户随后批准实施, 追加文献读取与可注记工具库/指针表, 以及额度中断续接优化. 当前进度与精确后续步骤在 `docs/optimization-20260905-progress.md`, 阶段边界检查额度并优先保存已有工件.

### 2026-09-05 会话: 文献工具库和额度续接优化

- 用户批准性能优化方案, 明确工具库及其 agent 批注/指针表是核心功能, 并要求额度耗尽后可续接. 额度恢复后接续已落盘实现, 未重启数学研究或消耗 reset credit.
- 发布批次: workflow 1.15.0, rigorous 1.12.0, manage 1.8.0. 新增实际来源保存/版本检索/有界读取, 卡片哈希批注及指针生成, latest-state 恢复入口, 幂等 receipt, 配额快照检查, 同名技能路径诊断和严格指标比较.
- 工作方法: 独立临时目录行为测试, 先保存进展再进入昂贵步骤, 保持数学审计/Blueprint 接受门禁. 独立审查发现旧卡片归档/适用范围丢失, 修复后复审 PASS. 原 reviewer 因额度中断无结论, 未算作 PASS.
- 验证: validate_all 81 项通过, MANIFEST 55 文件; 18 smoke 均通过. 更新版本断言, Windows 子进程需继承 PYTHONUTF8=1. 新 CI 覆盖 Linux/Windows 维护模块. 本批未运行新数学 A/B.
- 具体方案/结果/续接动作: docs/codex-performance-optimization-plan-2026-09-05.md, docs/optimization-20260905-results.md, docs/optimization-20260905-progress.md.

- 2026-09-05 release follow-up: parent validate CI and DSH validate CI passed. Fixed the pre-existing sync-fork job-level secrets condition using step-level env conditions per GitHub context availability. Preparing a no-model actual-artifact L0 replay after user-reported quota recovery; no research worker dispatch.

## Archived before the 2.0 implementation release, 2026-09-09

- 2026-09-09 用户批准按长期研究目标落地 2.0, 改善两个仓库 README, 整理内容并清理冗余代码. 在 codex/plugin-v2-implementation-20260909 实施, 具体进度见 docs/v2.0-implementation-status.md. 工作方法: 先保存成果仓库 68 个既存变更文件和哈希, 分离 Lean, 文献经验库和仓库整理的写入范围, 协调器实现短入口与持久恢复后统一验证. 不恢复额度门禁, 不改变 frozen benchmark 或 canonical 数学状态.

- 2026-09-09 用户要求 "使用这次调研学习到的方法, 修改原方案". 直接将 docs/v2.0-refactor-plan.md 更新为修订 2, 目标版本仍为 2.0.0. 工作方法: 以已提交的调研和隔离诊断为依据, 把精确目标/传递公理/根依赖, 可复用 Lean 反馈, 条件证明路线, 语义回译和审计复用纳入工程设计, 并贯通文献工具卡与编译任务恢复. P0 优先修复验证器假通过, 后续分批实现和验收; 保留旧版/新版/空白对照, 云平台和第二 checker 可选. 按需读取的入口体积目标不变, 不新增固定研究阶段或审批链. 本次只修订方案与维护文档, 调研原件和诊断结果保留, 插件实现/版本未变, 未启动实施或新 benchmark.
- 2026-09-09 用户要求先保留 2.0 方案, 调研 Fuse / 三维挂谷和 Prove2Me / 完整 FLT, 再讨论 Lean 验证与审计优化. 工作方法: 阅读机构公告, 论文和固定提交的实际根声明, 定义连接, 公理及 comparator / Nanoda 配置; 后台 researcher 单独核查 Prove2Me, 主协调器复核关键来源并检查现有验证代码. 新增 docs/lean-verification-platform-research-2026-09-09.md, 来源笔记和隔离诊断. 模拟进程结果确认主验证器将定向目标缺失/超时汇总成通过, Lean 块注释中的 sorry 被误报; 未执行 Lean 证明. 报告建议修复结果语义, 加入精确目标与传递依赖检查, 采用持久编译反馈, 针对关键定义和连接做语义回译, 复用工具库指针和持久任务恢复. 本次仅调研和文档维护, 原 2.0 方案, 插件运行逻辑及版本保持不变, 未安装平台或运行巨型证明/新 benchmark. 不把发布方验证摘要写成本次独立复现, 不恢复额度门禁.
- 2026-09-09 用户要求 "拟一个插件重构计划", 将插件变成 "工作流程引导", "极大减少不必要的约束", 目标版本定为 2.0. 本次仅提交 docs/v2.0-refactor-plan.md, 不实施重构或升级已安装版本. 工作方法: 以已冻结 L1/Q9 对照和当前四份入口/文献/恢复/校验代码为依据, 区分自主研究选择, 数据操作校验和实验控制; 计划取消强制阶段, 角色隔离, 默认多轮审计/Lean, 重复台账和额度门禁, 保留并简化文献内容到可批注工具卡/指针复用及中断续接. 四包拟统一 2.0.0, 当前仍为原 1.x. 后续按方案分批实施和验收, 本次不启动新 benchmark, 不续接已完成实验. 用户不关注额度的指示继续有效.
- 2026-09-09 用户要求的更难 Q9 三组对照已跑完. A/B/C 三份求解及三份外审均正常返回, 全部 PASS 100/100 且完整闭合, 无补证. B 外审 625.152405 秒, 41493 非缓存输入和 18193 输出 token, 14 项检查通过. B 全交付相对 A 的非缓存输入 -1.32%, 时间 +4.75%, 输出 +28.48%; 空白最快, 不宣称普遍加速. 六阶段 209 项冻结文件哈希及 475 个唯一响应复核通过, 两次无效隔离尝试的 59 响应另列. 已补全项目旧结果对应报告, 最终成本表和恢复入口, 原始数学交付不改写, 主项目来源及规范知识库哈希保持一致. 后续文献工具库和受控续接另做验收, 本轮不自动启动新测试. 入口 benchmarks/codex-20260908-q9/CONCLUSIONS.md 与 STATUS.md.
- 2026-09-08 Q9 新版 B 正常返回并封存, 2545.191219 秒, 323543 非缓存输入和 127577 输出 token, 126 个唯一响应, 主任务及 3 个实际子任务. 完整候选证明只用 C2/C3 推出 Q>0 时 r<c^2/4, 并由小 r 定理推出严格结论; 2565 个整数 Bernstein 系数和独立内部审计已交付. 63 个冻结文件与身份/隔离检查通过, 原字节准备匿名外审. 对 A 的求解非缓存输入及时间比分别约 1.008 和 1.027, 不提前认定优化获益.
- 2026-09-08 Q9 空白 C 外审正常返回, 527.603821 秒, PASS 100/100, PROVED 且 root_closed=true, 11 项关键检查无实质缺口或补证. 外审用独立三角基变换重建全部 230 个有理 Bernstein 系数. C 全交付 2483.409666 秒, 468683 非缓存输入和 137792 输出 token. 新版 B 已按封存输入首次启动; 同账户凭证私下刷新, 无额度查询或额外数学提示.
- 2026-09-08 Q9 空白 C 正常返回并封存, 1955.805844 秒, 423251 非缓存输入和 122462 输出 token, 204 个唯一响应, 1 个主任务及 3 个实际子任务. 候选证明只用 C2/C3 推出 Q>0 时 r<1/9, 并证明 r<=1/9 时 R>0; 全部 230 个 Bernstein 系数可精确检查. 63 个冻结文件和身份/隔离复核通过, 数学答案原字节送匿名外审, 尚未计外部通过. 不向随后 B 提供 A/C 的数学结果.
- 2026-09-08 C 的继承上下文日志含父 session_meta, 使封存运行器的原始身份列表重复显示父 ID. 用量统计原本就按逐响应 thread_id 和 response_id 去重, 未受影响. 报告器补充首条元信息与日志文件 UUID 绑定的身份表, 保留原日志及原列表, 加入回归用例. 不修改正在运行的封存运行器, 提示词, 时限或评分.
- 2026-09-08 Q9 r2 A 外部匿名审计正常返回, 548.878768 秒, PASS 100/100, PROVED 且 root_closed=true, 15 项关键论证无实质缺口或补证. 证实只用 C2/C3 即可推出更强的 S>0, 再推出原 Q9. A 全交付 3026.528950 秒, 369917 非缓存输入和 113459 输出 token; 两次隔离失败另列. 已启动空白 C, 新版 B 随后运行. 不把单组通过当作插件优劣结论, 主项目数学状态未在本次对照中集成.
- 2026-09-08 Q9 r2 A 正常返回并封存, 共 2477.650182 秒, 320926 非缓存输入和 96822 输出 token, 116 个唯一响应. 候选证明仅用 C2/C3 推出更强的充分不等式, 包含 1920 项精确系数证书; 内部审计已通过, 外部匿名审计尚未返回. 旧版清单路径及归档校验修复耗时计入 A. 数学答案原字节送审, 未移除证书输出中的 PASS. 59 个冻结工件及身份/隔离复核通过; 后续顺序仍为 C 再 B.
- 2026-09-08 r1 首个真实子任务仍收到额外技能, 274.305798 秒后被守卫停止, 工具调用数为 0; 原 10 响应用量和工件单独保存, 不计数学评分. 用真实账号元数据同步加本地模拟响应重现 35 秒延迟加载故障, 改为显式禁用远程 SKILL.md 路径, 正对照已通过. 增加真实子任务输入及沙箱执行门禁, 审计环境同步采用; r2 延续原题, 版本, 模型和时限, 全部额度查询仍关闭. 当前恢复按 Q9 STATUS.md 及 CHILD_ISOLATION_AMENDMENT.md, 不续接两个无效 A.
- 2026-09-08 原 Q9 A 续接前发现账号远程插件缓存使两个子任务收到未分配的技能元信息, 哈希检查阻止新推理. 原 950.671529 秒及 49 响应成本完整保留为隔离失败, 无数学评分且不再续接. 在相同 Q9, 模型, 版本, 评分和时限下建立全新 r1; 显式禁用额外插件, 拒绝工具访问缓存, 增加真实子任务输入监测. 额度检查仍按用户指示关闭. 当前入口 STATUS.md 和 ISOLATION_REPLACEMENT.md 优先于下条原续接计划.
- 2026-09-08 用户明确要求额度充足, 别管额度问题. 关闭 Q9 的全部额度查询和快照门禁, 用独立政策文件记录授权, 不伪造额度数值. 保留旧 seal 与首段运行器, A 沿原 UUID 和剩余 2649.328471 秒继续; C/B 及三次外审采用同一政策. 固定求解/审计时限, 原题, 评分及既有结果不变. USER_QUOTA_OVERRIDE.md 为当前优先入口, 不再恢复旧额度轮询.
- 2026-09-08 用户要求从主项目库选择更难的问题再跑对照. 新轮选取 sequence-26 仍为 OPEN 的 Q9, 保留完整分支和三个相容性方程, 区分前置审计进展与无返回任务. 复用旧版/新版/空白处理, 每组 3600 秒求解及 1200 秒外审, 固定 A,C,B 顺序. 恢复入口 benchmarks/codex-20260908-q9/STATUS.md. 主项目有既存未提交改动, 只冻结来源字节; L1 结果不改写. 运行器增加预注册任务和预算绑定, 题面及已安装插件逐文件哈希检查, 不靠新命令获得额外续接预算.
- 2026-09-08 Q9 题面独立复核 PASS, 三组实际隔离/工具/模拟续接预检均 PASS, 81 项仓库检查和 8 项运行器测试通过后封存并启动 A. 增加冻结工件及去重用量的导出器, 将 root_closed, 严格部分进展和数值评分分开核验; 只读原始数学交付, 不改已封存运行器或三组题面.
- 2026-09-08 A 运行期间桌面额度接口连续读取失败, 但求解响应返回同账户最新真实额度. 增加带原始事件时间和行哈希的额度输入回退, 仅接收 <=120 秒的 Codex 窗口, 不用读取时刻延长旧快照, 不修改封存运行器/预算/评分. 记录见 Q9 的 QUOTA_FEED_NOTE.md; 若两个来源均无新数据, 原有过期门禁仍暂停并按原会话续接.
- 完整旧记录: [AGENTS_HISTORY.md](AGENTS_HISTORY.md). 仅在查找历史决策, benchmark 或故障证据时按关键词读取相关段落.
- 2026-09-05 用户要求: 根据既有 benchmark 优化 Codex 研究插件, 重点完善真实文献读取, agent 可注释工具库与指针表, 以及额度中断续接; 额度恢复后继续实施.
- 本轮方法: 先做确定性 L0, 使用隔离的真实工具卡和 sequence-26 工件回放; 保留主项目原文件和数学状态. 高成本 solver A/B 留待后续匹配实验.
- 功能与验证证据见父仓库 docs/optimization-20260905-results.md; 发布和恢复入口见 docs/optimization-20260905-progress.md. 每次维护在本节追加简短结果, 长证据放专门报告.
- 2026-09-06 用户报告额度恢复后完成发布核对: manage 1.8.1 的 BOM/旧卡片修复和真实 L0 回放已发布, 父仓库与 DSH 1.15.1 CI 通过, Codex 和 DSH helper 哈希一致. 新数学 A/B 尚未运行, 同名技能副本只诊断和记录来源.
- 2026-09-06 用户批准三臂 benchmark 开始. 恢复入口为 benchmarks/codex-20260906-l1/STATUS.md. 先冻结旧版/新版/空白环境及相同模型预算, 用无模型 probe 核实隔离, 再逐臂运行并记录实际额度. 真实 cwd 已纠正, 不从桌面误传路径创建项目.
- 2026-09-06 用户要求继续. 改用 WSL 的固定 0.153.4 CLI 和新隔离目录, 现有代理已可用. T1 三臂完成文件/网络隔离与本地请求清单预检, 修复配置重写丢失插件启用项的问题; 新增限时单写运行器, 同 session 续接和 4 项无模型测试. 正式运行状态和剩余额度仍以 benchmark STATUS.md 及外部 run/state.json 为准.
- 2026-09-06 T1 初次空白组因 code-mode host 关闭导致工具不可用, 62.29 秒后停止并排除计分. r1 六个全新环境启用并固定匹配宿主, T1 三组通过真实工具调用和模拟同 ID 续接检查. 剩余额度低于启动门槛, 续接时直接读取 STATUS.md 的 r1 入口, 不重做准备, 不续接无效尝试.
- 2026-09-06 用户再次要求继续, 五小时额度恢复而周额度剩余 21%. 原 25% 周保留线为协调器策略, 在 r1 首次求解前记录资源修订为周剩余 <=10% 时停止; 本轮先推进 T1 空白组及盲审. 复用已通过预检的环境, 不改题目, 模型, 时间上限或评分.
- 2026-09-06 用户明确要求不需要保留额度. 取消全部人为额度保留线; 耗尽, 状态过期和固定运行时间仍触发检查点. 已运行段保留原代码哈希, 如旧门槛触发则按同会话及剩余预算续接. 未授权使用重置积分.
- 2026-09-06 T1 r1 空白组完成并冻结, 443.19 秒, 7 次有用量记录的响应; 41354 非缓存输入, 86272 缓存输入, 13231 输出 token. 尚待独立匿名盲审, 不将求解器自称证明完成直接计为通过. 用 response_id 去重继承用量, 未知项保留 null.
- 2026-09-06 T1 空白组独立盲审 PASS 100/100, 无实质缺口或补证. 求解 443.19 秒, 盲审 393.09 秒, 共 74002 非缓存输入和 25255 输出 token. 已保存匿名审计及 response_id 去重指标; 开始旧版插件 A 组, 不提前推断插件收益.
- 2026-09-06 用户要求继续. A 组日志确认此前因真实额度耗尽退出, 已按原 session 续接, 保留 451.422577 秒消耗和现有证明工件, 剩余 1348.577423 秒. 用户不保留额度的要求继续有效, 未兑换重置积分. 该自然中断不替代新版恢复功能的受控对照.
- 2026-09-06 A 组完成, 累计 1277.998 秒, 含一次内部审计, 返回 123374 非缓存输入和 35714 输出 token. 已按原字节处理冻结副本的目录内文件链接, 保留收据. 外部盲审仅去掉首行旧审计状态, 正文和原答案保持哈希绑定; 尚不计外部通过. 恢复入口仍为 benchmark STATUS.md.
- 2026-09-07 用户要求继续. A 外部审计在保存报告后触及额度, 已按原 session 和剩余预算续接并完整返回, 432.192 秒, PASS 100/100, 15 项检查无实质缺口. A 全交付计 1710.190 秒及 186108 非缓存输入 token. 已启动新版 B, 不重做 C/A, 不将自然中断差异全归因于插件.
- 2026-09-07 B 首段因隔离目录旧刷新凭证失效而退出, 未返回模型响应. 仅更新同账户私有认证文件, 按原 session 续接并保留 12.037755 秒. 认证内容不进入证据仓库, 模型, 配置, 题目和预算不变.
- 2026-09-07 用户再次要求继续. B 在内部审计期间触及真实额度限制, 累计 538.843714 秒. 已按原 session 启动第三段, 保留候选证明和研究记录, 剩余 1261.156286 秒, 无新尝试或额外预算.
- 2026-09-07 B 完整返回并冻结, 1151.973 秒, 244895 非缓存输入和 38060 输出 token, 含原内部审计任务的续接. 原始 B/A 时间比 0.901, 非缓存输入比 1.985, 未达到本题预设成本目标. 已启动同标准外部盲审; 仅去除首行及两行页尾的旧审计元信息, 数学正文不变.
- 2026-09-07 T1 三组均完成外部盲审, 全部 PASS 100/100, 无实质缺口或补证. B 全交付 1514.002 秒及 275403 非缓存输入, 对 A 分别为 0.885 和 1.480. 保存按实际 turn ID 分组的缓存证据和完整对照; 不能将跨窗口恢复差异当作纯插件效应. 按原计划进入 T2 预检, 不更换 T1 弱成本结果.
- 2026-09-07 用户继续后, T2 三组均通过文件/网络隔离及真实工具调用预检, 零外部模型调用. 已在零求解 session 时扩展原 seal, 保留旧 seal, 刷新同账户私有认证后启动 B. T2 仍按 B,A,C 顺序和原题原预算评估, 允许如实报告严格部分结果.
- 2026-09-08 用户要求继续. T2 B 在保存 answer.md 和候选证明后触及真实额度, 已按原 session 续接, 保留 1172.987794 秒消耗及 627.012206 秒剩余预算. 下界及上界候选均未计为外部审计通过, 继续按原题原评分核对交付.
- 2026-09-08 T2 B 在原预算内正常返回, 累计 1754.826646 秒, 277157 非缓存输入和 69407 输出 token, 包括一个研究子任务和一个独立内部审计. 已冻结完整候选证明及失败路线记录, 原字节提交外部盲审. c=1/2, C=10^12, t0=1024 暂为待外审结论, 未改主项目数学状态.
- 2026-09-08 用户再次要求继续. T2 B 外审因协调器额度快照过期而暂停, 已刷新真实额度并按原审计 session 续接, 保留 302.375437 秒及 597.624563 秒剩余预算. 该次为协调器暂停, 不记作真实额度耗尽或新版恢复收益; 不重跑已完成求解.
- 2026-09-08 用户继续后, T2 B 外审在真实额度恢复后沿原 session 正常返回, 共 670.340627 秒, PASS 100/100, 15 项关键论证无实质缺口或补证. 已保存两次暂停原因, 审计原件及实际逐响应成本; 全交付 415542 非缓存输入及 86552 输出 token. 按原顺序启动 T2 A, 不改题目, 插件版本或预算. 恢复入口仍为 benchmark STATUS.md.
- 2026-09-08 成本诊断: 按两值平均的通常中位数定义, T1 求解非缓存输入比已将两题中位数下界固定为 0.992490314, 高于目标 0.75. 精确分数及源哈希保存在 solver-cost-feasibility.json; 该结论保留全部实际中断成本, 不作纯插件因果归因. 继续完成 T2 A/C 的质量与空白对照, 不替换已完成尝试.
- 2026-09-08 用户要求继续跑完本轮. T2 A 在 1022.394337 秒触及额度后暂停; 当前桌面账号已更换, 接口返回 Pro 的单个 10080 分钟窗口. 运行器按实际窗口读取额度, 空值仍为未知, 不伪造五小时百分比; 6 项确定性测试覆盖新结构. 保留前一 seal 并记录基础设施及账号修订, 沿原 A session 和剩余 777.605663 秒续接, 不重跑已完成组或兑换重置积分.
- 2026-09-08 T2 A 在原求解上限停止, 含退出清理共 1802.783856 秒, 状态 BUDGET_EXHAUSTED. 完整答案及内部审计报告已保存, 303881 非缓存输入和 59829 输出 token 包含三个子任务. 已按原字节启动外部盲审, c=1/4, C=10^10, t0=32 尚待外审; 不将内部通过替代正常进程返回或外部评分.
- 2026-09-08 T2 A 外部盲审正常返回, 621.203151 秒, PASS 100/100, 19 项检查无实质缺口或补证. 全交付 351744 非缓存输入和 76412 输出 token; 数学通过不改写求解器限时停止状态. 已启动最后的空白 C 组, 完成后汇总本轮两题三组对照.
- 2026-09-08 T2 C 正常返回并封存, 1266.552126 秒, 106041 非缓存输入和 45056 输出 token, 包含两个子任务. c=1/(2 sqrt(2)), C=2^43, t0=16 已按原字节送入最后一次外部盲审; 六份求解交付均已冻结, 不再重跑求解器.
- 2026-09-08 用户要求的本轮 L1 已完成. T2 C 外审正常返回, 597.610152 秒, PASS 100/100, 16 项论证无实质缺口或补证. 六份证明全部通过外审; 空白组两题均以较低实际成本达到相同评分. 新版 B/A 求解非缓存输入中位比 1.448519, 时间中位比 0.937393, 均未达到预设目标. CONCLUSIONS.md 和 comparison-l1.json 保存完整结论; 12 阶段哈希与 285 个唯一响应用量复核通过, 所有运行进程已退出. 保留账号/额度/缓存限制, 后续文献工具库和受控恢复验收单独开展, 本轮不自动运行 L2.
