# Codex research plugin optimization plan

Date: 2026-09-05.
Status: APPROVED_IN_PROGRESS. 用户已批准实施, 并追加文献读取/工具库注记与指针表, 以及额度中断续接两项核心优化.

## Approved implementation scope

- 先交付确定性文献内容缓存和分段读取, 现有工具卡的可重建指针表, hash 绑定的 agent 注记及过期提示. 保留现有卡片, 人工索引内容和数学状态.
- 在现有 checkpoint 引擎上增加最新恢复点发现, 幂等 receipt 恢复, 未封存 draft 和已执行状态不确定的显式提示, 以及可配置的额度快照检查. 不等待硬中断才保存已有进展.
- 同步修正性能字段/unknown/可比较性和 skill 来源诊断, 收紧按需读取与审计调度.
- 当前执行以确定性回归和有界独立行为检查为先. 长时数学 A/B 在代码质量门禁通过后分级运行, 不将未运行实验描述为完成.
- 开始时五小时 used 38%, 周 used 6%. 阶段边界检查共享额度, 接近耗尽时写清实际完成项和下一步, 不自动兑换 reset credit.
- 当前维护恢复记录: `docs/optimization-20260905-progress.md`.

建议先建立可比较的当前基线, 修复指标口径与多来源 skill 选择问题, 再收紧已有 closure-first 协议的执行路径. 保留独立数学审计, 严格状态标签, 不可变恢复链和 Blueprint 确定性接收. 模型分层与 reasoning effort 调整放在同模型插件 A/B 之后单独检验.

## 1. 核查范围与当前基线

本轮读取两个仓库的 AGENTS.md, 插件维护历史, 当前 SKILL 与关键 reference, 性能告警实现, CI 配置, 历史 benchmark 预注册与结果, 本地安装入口和 Codex 配置. 对两个工作仓库执行 fetch 后核对, 没有合并或切换分支.

| 对象 | 当前核查结果 |
| --- | --- |
| BVE 项目 | 本地 HEAD 与 origin/main 均为 `cae1b2dd6e0a9a27078d5de27c433ed72bf94168` |
| 插件项目 | `_xsoc1_work` 的 HEAD 与 origin/main 均为 `516037f14f340107da8448b6e42df17317d9fc63` |
| DSH 使用的父仓库 canonical clone | 本地 HEAD 同为 `516037f14f340107da8448b6e42df17317d9fc63`; 本轮未修改该目录 |
| 插件版本 | workflow `1.14.1`, rigorous `1.11.0`, manage `1.7.0`, lean-verify `1.6.0` |
| 本机 PATH 中的 Codex | `codex-cli 0.153.1` |
| 用户默认配置 | `model = "gpt-6-astra"`, `model_reasoning_effort = "max"` |
| 旧主 benchmark | `gpt-5.6-sol / xhigh`, Codex CLI `0.149.0-alpha.4.3` |
| 工作区状态 | 插件仓库开始时干净. BVE 有已有修改和未跟踪的 sequence-21 至 sequence-26 等研究工件 |

CLI 版本是 PATH 中命令的实测值, 配置是用户默认值, 两者不自动证明任意桌面任务或历史子 agent 的实际运行配置. 新 benchmark 必须从实际运行记录核对 model, effort, binary hash, 插件 hash 和工具暴露情况. 本轮未测 GPT-6 Astra 的数学正确率或相对 GPT-5.6 Sol 的速度.

## 2. 历史证据支持什么

| 证据 | 已观察到的结果 | 对本轮方案的约束 |
| --- | --- | --- |
| A6 reuse-gate 实验 | 相同范围的 partial result, uncached input 增加 101.5%, tool calls 增加 45.7% | 避免每条路线反复检索和强制生成复用记录. 该实验还受脚本超时与并发产物可见性影响 |
| v1.6 静态入口优化 | 四个入口合计 124,443 -> 97,802 bytes, 减少 21.4% | 静态字节节省不能直接解释为运行 token 或时间节省 |
| v1.7 U2 matched regression | root wall 4052 -> 1881.050 s; uncached input 1,108,074 -> 338,812; tool calls 216 -> 58; child sessions 7 -> 3 | closure-first 和减少重复调度具有同题实测支持. 原目标仍 OPEN, 收益针对已审计 partial package |
| Pilot v6 Hs-domain | A plugin: 99/PASS/1514.327 s. B blank: 94/REPAIRABLE_GAP/602.092 s. C QED: 97/math PASS/1438.300 s, system FAILED | 强模型能较快找到结论, 独立审计仍有价值. 优化目标包含证明完整性与可交付性 |
| v1.9 recovery drill | 5 次确定性操作合计 1294.558 ms, 0 模型调用, 0 子 agent, 0 网络调用 | 恢复应由程序维护. 这不是数学端到端加速实验 |
| v1.10 至 v1.14.1 | 维护记录覆盖 advance, scoped validation, formalization handoff/consumption, Blueprint gateway, checkpoint-current 修复 | 这些机制已经存在. 下一轮应测量实际使用成本和兼容性 |

来源: [A6 报告][a6], [v1.6 报告][v16], [v1.7 matched regression][v17], [Pilot v6 结果][v6], [恢复演练][recovery], [插件维护记录](../AGENTS.md).

v1.7 的 uncached input 降幅为 69.42%, root wall 降幅为 53.58%. 这是一道复用任务的回归结果, 不能外推为所有数学问题或当前模型的收益. Pilot v6 每臂只跑一次, 不构成模型或插件的统计排名. 历史 cost 是 API-equivalent proxy, 不是真实 ChatGPT 账单.

已有 fast-close certificate, 按需工件 profile, 最小 context slice, claim-local audit 和 quota recovery 都应作为当前对照组的组成部分. 不能把这些旧功能再次作为新优化的贡献.

## 3. 当前发现的具体问题

### 3.1 同名 skill 有多个不同来源

当前会话的可用技能列表同时包含本地 skill 与 math-research 插件 skill. 文件核查结果如下.

| 入口 | 本地旧副本 bytes | math-research 当前副本 bytes | 当前插件版本 |
| --- | ---: | ---: | --- |
| rigorous | 44,978 | 13,731 | 1.11.0 |
| manage | 22,605 | 39,094 | 1.7.0 |
| lean-verify | personal 入口 10,339 | math-research 入口 19,218 | 1.6.0 |

rigorous, manage, workflow 的当前安装缓存 hash 与本次读取的插件源码入口 hash 一致. 旧 rigorous 与当前版本 hash 不同, 旧文件包含早期多路线编排和内联历史, 没有检索到 closure-first/fast-close/recovery 入口文字.

这说明存在选择不同协议的风险, 并不说明每次调用都读取全部副本. 官方文档说明 skill 初始只暴露元数据, 选中后才读取完整 SKILL.md. 因此应分别统计技能目录元数据, 实际选中的入口, 阶段 reference 和继承上下文. [OpenAI skills documentation][skills-doc]

建议在 doctor 中报告同名来源, 版本, hash 和本次选择结果. benchmark 的隔离配置只安装冻结版本. 日常环境中先保留可恢复副本, 再处理冗余入口; 本轮没有删除或禁用任何 skill.

### 3.2 上下文预算覆盖范围不足

当前四个插件入口为 13,731 + 28,269 + 39,094 + 19,218 = 100,312 bytes. 此数值只是四个文件的静态总和, 不是一次任务的实际输入量. 现有 validate_all.py 对每个入口设置 byte budget, 尚不能度量一次真实路径加载了多少 reference 或向子 agent 继承了多少内容.

另外, BVE AGENTS.md 在本轮修改前为 37,999 bytes, 插件 AGENTS.md 为 44,737 bytes. 其中有大量长期维护历史. 后续应按现有归档约定保存完整内容, 入口保留现行规则, 当前状态和条件明确的历史指针. 不把历史删除当作压缩手段.

优化优先级应由实际读取路径决定. 不要求所有 skill 一起缩短, 也不通过遗漏必要证明定义达成字节指标.

### 3.3 仍有可能重新引入旧调度方式的表述

- `references/subagent-delegation.md` 的 Scheduling 第 6 条要求 verifier throughout active. closure-first 已规定局部检查按需进行, 全包审计放在边界. 应明确前者指持续保留检查责任, 而非购买常驻 verifier 调用.
- workflow 要求每个 planner step 重写并重读 whiteboard. 这与已持有状态时只处理变化量的做法存在额外读写机会, 需要 trace 验证其实际成本.
- workflow Stage B 的 mandatory intermediate Lean checkpoints 与 Stage C 的 Tier 0/scaffold 分层应具有统一适用条件. 应按任务声明的形式化范围执行, 同时保留未证明义务和强制状态区分.
- rigorous 的 minimal invocation 仍直接要求 diverse research portfolio. 示例应与 closure-first 的单目标默认路径一致.

这些是源码中的规则或歧义, 本轮未通过新运行证明它们已经造成多少浪费. GPT-6 Astra 官方指导强调其对技能和 AGENTS.md 指令更敏感, 因而先消除冲突比继续叠加通用提示更有依据. [OpenAI model guidance][model-doc]

### 3.4 性能指标和告警实现需要先修正

当前 [performance_alert.py](../plugins/math-research-workflow/skills/math-research-workflow/scripts/performance_alert.py) 存在以下静态可确认问题.

- 读取缺失的成本字段时使用 `get(key, 0)`. 缺失数据会被当成零消耗.
- 比较字段为 `wall_ms`, `cache_read_tokens`, `steps`. Pilot v6 的真实 metrics 使用 `root_active_wall_seconds`, `cached_input_tokens`, `model_responses`. 当前脚本没有统一适配层.
- `output_tokens` 没有进入实际成本比较循环. `artifact_count` 减少 20% 会被直接视为文档退化, 无法识别 fast-close 中合法减少工件的情况.
- 比较前没有强制核对 task/prompt/model/effort/plugin/runtime 身份. 当前 reference 允许同类或相近难度 baseline, 适合提示性观察, 不足以支持因果归因.
- 告警报告的数学收益部分仍需人工填写. 它没有读取审计过的 root closure 和实际剩余缺口.

建议先修指标再优化, 否则减少日志和工件可能被错误判断为性能退化. 新版保留 advisory 模式, 严格 A/B 模式对不匹配的输入返回 INCOMPARABLE.

### 3.5 当前实战数据不足以支持新的端到端性能结论

KP-DET 的本地 sequence-26 state 标为 RIGOROUS_PARTIAL_RESULT, experiment_integrity.enabled 为 false. sequence-00 至 sequence-03 的 recovery_metrics.md 明确说每 agent 的 tokens, responses 和 cost 不可用. 该早期 metrics 文件也不是 sequence-26 的累计成本报告.

因此, sequence-26 适合作为后续复制到隔离目录的恢复回归材料, 不能直接作为完整计分 arm. 本轮只读取记录, 未重新验证其整条 checkpoint lineage, 未修改已绑定工件, 未续跑 Q9.

## 4. 建议实施顺序

| 优先级 | 工作包 | 具体交付 | 验收方式 |
| --- | --- | --- | --- |
| P0 | 冻结环境与统一指标 | 环境清单, skill 来源诊断, metrics adapter/schema, 可比较性检查, benchmark 索引 | 历史 metrics 重放可追溯; 缺失值不变成 0; actual/requested 配置可区分 |
| P1 | 收紧协议与按角色读取 | 单一审计调度规则, 条件清楚的阶段指针, 更新 invocation 示例, AGENTS 历史归档 | 必要义务和门禁不丢失; 原版与候选版可独立运行 |
| P1 | 程序承担状态整理 | 基于现有工具的状态摘要, packet/manifest 准备, 工件视图生成 | 状态转换有来源和 hash; 数学结论仍由证明与独立审计决定 |
| P2 | 同模型端到端 A/B | 当前插件与候选插件的预注册回归 | 质量先过门槛, 再判断速度和成本 |
| P3 | 分层模型和 effort 消融 | 只改变模型分工或 effort 的单独实验 | 单独归因, 不混入插件文本改动收益 |

建议第一批只完成 P0 和 P1 的明确问题. checkpoint 大规模重构和模型自动路由应等待新 trace 指明瓶颈.

### 4.1 指标与 benchmark 资产归属

插件仓库新增可移植的 benchmark 协议目录, 包含 schema, parser, 小型脱敏 fixtures, 预注册模板和报告模板. BVE 保留数学题目, 证明, 历史原始工件和真实研究数据. 两侧使用 commit/path/hash 引用, 避免复制整套研究历史或将隐藏金标准带入插件包.

建议记录以下外部可观察数据, 不要求读取或保存模型私有推理.

- Identity: task/prompt/source hashes, requested/observed model 和 effort, CLI/runtime hash, plugin/skill hashes, tool allowlist/schema 摘要, 网络与隔离条件.
- Usage: uncached input, cached input, output, reasoning output 的独立可用字段, model responses, outer orchestration calls, 实际 nested tool calls, root active wall, elapsed wall, aggregate agent time.
- Work: first proof 时间, first audited delta 时间, required root closure, 精确缺口, 各角色审计次数, unchanged-package re-audit, duplicate dispatch, NO_RETURN 和 artifact retention.
- Accounting: solver, internal audit, formalization, deterministic integration, infrastructure-invalid attempts, retries, quota resume 和外部评审分账; 另给总投入视图.
- Provenance: 每项值绑定原始日志和提取规则. unavailable 使用 null/unknown. 累计 usage 与单次增量不混加, 跨段按稳定 session/call ID 去重.

root wall 与并行 agent 时间总和分开. nested tools 与 functions.exec 外层调用分开. output tokens 是成本, 不用证明篇幅或文件数量代理数学质量. 成本 proxy 使用冻结价目版本, 与实际可取得的账单字段分开. 账户共享额度的百分比只作背景, 不反推单任务 token 消耗.

### 4.2 让程序生成必要状态视图

复用现有 checkpoint_resume.py, validate_pipeline.py 和 formalization_handoff.py. 先添加薄的调用与摘要层, 不建立第二套接收器或第二份 canonical research state.

- 根据已验证 state 输出 current obligation, exact next action, minimal read set 和已有失败记录.
- 由已有结构化状态生成 whiteboard/research-map 的可读视图和 packet 的 hash 字段, 避免模型在多个文件中重复手抄同一状态.
- 当前模型只提交可检查的 claim, proof, gap 和 decision_delta. 程序可校验与整理, 不自行判定数学已证.
- 对独立只读查询或检查进行有界批处理, 每个成员的错误均保留. 依赖动作, 写入, 数学综合与审计判定保持顺序.
- checkpoint seal/resume/advance 仍保留原子创建, 原始不可变字节, 全谱系验证和 STALE 拒绝. Blueprint canonical 操作继续通过 active runtime 的 blueprintctl.py.

目前从源码可见 checkpoint 验证会回溯 predecessor, 但没有本轮性能剖析证明它是主要瓶颈. 先记录实际读取/哈希次数及耗时. 若需要缓存, 优先限于一次明确快照内的重复读取, 并保留写入与跨进程边界的新鲜性检查. 不以路径或 mtime 单独认定内容可信.

### 4.3 对当前 Codex 的适配

当前会话暴露 4 个 agent 并发槽, 含主 agent. 单目标路径先由主 agent 直接研究, 只有 closure gate 允许时才派出具体 worker. 通常先开一个 prover, 在有独立证伪价值时再加一个 falsifier. reviewer 在候选结果出现时启动, 保留独立上下文和资源余量. 这些是本轮环境的建议配置, 不能写成所有运行时通用常数.

worker 只接收任务契约, 已接受依赖, 必要来源和自己的输出路径. auditor 接收冻结候选及可核验依赖, 不继承作者的探索对话. 返回稳定 ID, artifact path/hash, status, exact gap 和 decision_delta. 本轮环境支持用不继承对话的子 agent 来隔离输入, 具体 adapter 必须探测能力后再使用.

初轮 A/B 固定实际可用的 GPT-6 Astra 和同一 effort, 以当前 max 配置作为候选基线. 此后才单独比较 max 与较低 effort, 或让较低成本模型承担非承重的信息提取. 证明综合, 关键 lemma 与独立数学审计先保持同等级能力. 官方说明子 agent 默认继承 model/effort, 可显式配置; 这不意味着 skill 可以自行改变正在运行的主任务配置. [OpenAI subagents documentation][agents-doc]

## 5. 新 benchmark 方案

### 5.1 对照定义

- A: 当前稳定插件, commit 516037f, 在干净且唯一的冻结安装来源下运行.
- B: 单一候选补丁集合, 同模型, effort, CLI, task/prompt 内容, source, 工具权限和预算.
- C: 同模型的 task-only 对照, 只作为少量诊断. 如需比较可信交付成本, 也给它计算统一外部审计的成本.

旧 v1.6/v1.7 结果只作历史参考. 不把跨模型或跨 CLI 的新旧差值归因于插件. 环境去重效果先单独测试, A/B 都使用唯一安装来源, 避免与协议变化混淆. 首轮不重新部署五个外部系统, QED 等可在内部改动验证后另立横向协议.

### 5.2 分级运行, 通过后再增加成本

| 层级 | 样本与规模 | 目标与停止条件 |
| --- | --- | --- |
| L0 | 无模型的 metrics fixtures, 现有 smoke, 历史恢复工件隔离副本, 不同链长的合成 fixture | 字段映射, hash/lineage, 并发和路径错误必须可重复检出 |
| L1 | 2 个已知开发题 x A/B 各 1 次, 共 4 个 solver runs | 检验启动成本, first proof, 审计与收口. 已读过答案的 U2/Hs 只标 REGRESSION |
| L2 | 3 个保留题 x 2 次独立重复 x A/B, 共 12 个 solver runs | 覆盖有界可闭合题, 含假引理的证伪题, 难题或开放目标的 partial/recovery 路径 |
| 可选 C | 每个保留题 1 个 task-only run, 共 3 次 | 估计额外协议相对裸模型的成本与质量差异 |

L2 仍是小样本确认, 不据此宣称普适优越. 后续增题或增重复必须重新预注册. A/B 顺序在题目和重复之间平衡或随机化, 记录服务与缓存条件. 同一账户一次运行一个计分 arm.

建议 L1 每 run 30 分钟上限; L2 的两个有界题各 30 分钟, hard/partial 题 60 分钟. A/B 共用对应上限. 按此计算, L1 的 solver active wall 上限为 2 小时, L2 为 8 小时, 都是预算上界, 不是耗时预测. 评审与基础设施投入另行计量, 总预算须在正式预注册时包含这些部分. 本轮没有执行这些实验.

保留题与隐藏金标准由独立输入准备流程冻结, solver 不继承当前已读过历史答案的会话. 使用新 work root 和 CODEX_HOME, 测试进程可访问的数据与工具须与声明一致. offline arm 在任何数学调用前做 prompt/tool leakage probe, 不仅检查配置开关. 基础设施失败保留全部成本, 只有满足预注册条件才能用新目录替换, 不事后改算数学失败.

### 5.3 质量口径

沿用 Pilot v6 六轴: correctness 40, fidelity 20, strict progress 15, calibration 10, evidence 10, reproducibility 5. 保留分数至少 70, correctness 至少 32/40 的历史门槛, 同时单独保留 PASS/REPAIRABLE_GAP/FATAL_GAP 等标签. 高总分不能将有缺口证明改称 PASS.

所有强结论都接受身份盲审. 完成目标按相同 contract 的 required roots 判断. partial 任务比较固定承重义务上的已审计进展, 精确反例和剩余缺口; 将一个 lemma 拆成许多个不增加得分. 新颖性和 bonus 单列, 不补偿目标缺失.

候选发布不得引入错误完成, 错题, 数值证据冒充证明, fabricated source, 自我审计替代独立审核, 或旧审计错误应用于新 proof/dependency. 缺口的实质变化仍需要新审计.

### 5.4 建议预注册的效率门槛

以下全部为待验证目标, 不是预计已经实现的收益.

- 质量门禁通过, 逐题比较的 root completion/独立审计结果不退化, 六轴分数平均下降不超过 2 分且不能掩盖承重缺口.
- 新候选相对同模型当前插件, uncached input 的逐题配对比值中位数 <= 0.75.
- solver root active wall 的配对比值中位数 <= 0.80, 包含内部审计与实际交付的 total active wall 不出现超过 10% 的回退.
- 每个审计通过结果的完整成本另表报告. 困难开放题按同题进展比较, 不对未完成 run 编造 time-to-solution.
- 有效路径读取总量和首个数学动作前的输入量均下降, 同时确认没有漏读必要条件. 不把所有 SKILL.md 字节简单求和作为运行门槛.
- zero duplicate dispatch, zero lost returned artifact, zero unauthorized replay, zero extra Stage B research calls after certified STOP.

L1 只作 go/no-go, L2 报告全部 run 和离散程度. 样本不足时将收益标为尚未确认. 任何对门槛的修改均写入下一轮预注册, 不在看见结果后追改本轮目标.

## 6. 代码与发布落点

| 位置 | 后续建议变更 |
| --- | --- |
| workflow/scripts/doctor.py | 增加重复 skill 来源与 runtime 绑定诊断, 输出可复核安装清单 |
| workflow skill/scripts/performance_alert.py 与 performance-observability.md | 统一 schema, comparable/INCOMPARABLE, unknown 字段, proof quality 与工件 profile |
| rigorous SKILL 与 closure-first/agent-orchestration/subagent-delegation references | 消除调度歧义, 统一示例和最小 packet 条件 |
| workflow SKILL 与按阶段 references | 按任务阶段披露, 明确 Tier 0 与完整 formalization 适用条件 |
| 现有 checkpoint/pipeline/handoff 脚本 | 测量真实热点后复用其状态摘要与生成能力, 保留现有信任边界 |
| scripts/validate_all.py 与 tests | 增加入口指针/场景行为回归和 metrics fixtures, 避免仅做文本 marker 匹配 |
| .github/workflows/validate.yml | 当前枚举 11 项 smoke, 仓库存在 14 个 smoke 文件. 核对另 3 项适用条件后补齐, 增加 Windows 路径与换行覆盖 |
| docs/pipeline-full-flow.md, README 中英版, changelog, AGENTS | 每次实际协议变更同步更新, 方案文档不改写已发布协议 |

未来可把第一批实际 workflow 改动作为 1.15.0 候选, rigorous 若修改其内容则按自己的版本序列升级, 不能把 marketplace 中四个插件误称为统一版本. manage 若改文件需重生成 MANIFEST.sha256. 发布前执行仓库要求的 validate_all, 相关行为 smoke 和缓存 hash 核对; 独立审查状态机或审计门禁的变更.

发布阶段沿用父仓库与 fork 的既有同步规范, 然后更新 DSH 的 canonical parent clone, 运行适配同步与验证, 最后验证本机实际安装来源. 保留稳定版本和隔离 benchmark 配置便于回退. 现有 accepted Blueprint, 不可变 checkpoint 和研究结果不因性能优化重写.

## 7. 本轮交付与限制

本轮交付为此方案和 AGENTS 会话索引. 新增结论均来自当前文件或已冻结历史报告, 没有新增数学证明, 没有新模型 benchmark, 没有发布或改变用户配置. 主要待验证假设是: 唯一协议来源, 精确阶段读取, 程序整理状态和一致调度规则能否在 GPT-6 Astra 上降低可信研究产出的成本.

## Evidence index

[a6]: https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research/blob/cae1b2dd6e0a9a27078d5de27c433ed72bf94168/reports/plugin-performance-a6-ab.md
[v16]: https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research/blob/cae1b2dd6e0a9a27078d5de27c433ed72bf94168/reports/plugin-performance-v1.6-codex-context.md
[v17]: https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research/blob/cae1b2dd6e0a9a27078d5de27c433ed72bf94168/runs/three-arm-pilot-v2/pilot-v5-codex-u2/v17-regression/RESULTS.md
[v6]: https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research/blob/cae1b2dd6e0a9a27078d5de27c433ed72bf94168/runs/three-arm-pilot-v2/pilot-v6-hs-domain/RESULTS.md
[v6-prereg]: https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research/blob/cae1b2dd6e0a9a27078d5de27c433ed72bf94168/runs/three-arm-pilot-v2/pilot-v6-hs-domain/PREREGISTRATION.md
[recovery]: https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research/blob/cae1b2dd6e0a9a27078d5de27c433ed72bf94168/runs/plugin-benchmark-20260829-v19-recovery-drill/RESULTS.md
[skills-doc]: https://learn.chatgpt.com/docs/build-skills
[agents-doc]: https://learn.chatgpt.com/docs/agent-configuration/subagents
[model-doc]: https://developers.openai.com/api/docs/guides/latest-model

历史预注册完整口径见 [Pilot v6 preregistration][v6-prereg]. 插件源码发现绑定本轮 `516037f` 快照, 日后以候选补丁及其新测试结果更新, 不回写历史 benchmark 分数.
