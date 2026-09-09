# Prove2Me / FLT 一手来源笔记

访问日期: 2026-09-09, Asia/Shanghai. 本次访问为匿名网页读取及 GitHub REST / raw 文件 GET. 阅读平台论文和官方案例等入口, 并沿一手链接读取 FLT 证明仓库, 固定版本验证配置和脚本, Prove2Me workspace 文档及两个 Lean 提取脚本. 未登录 Prove2Me, 未调用注册, 投稿, 修改或付费接口, 未安装工具, 未克隆巨型仓库, 未运行 Lean / comparator / nanoda. 本笔记由后台 researcher 提供, 主协调器另行复核关键来源, 汇总报告并维护仓库文档.

证据口径: "本次查到"指实际读取的源文件, 配置或公开元数据. "发布方记录"指作者公布的结果, 不是本次独立执行成功. "推论"给出其前提, "未知"保留未访问或未证实的部分.

关键区别: 平台的根目标标记 Proved, 按其文档表示至少有一条 proof-sketch 路线的全部依赖递归闭合; 根下仍可能存在未采用的开放备选路线. 后续补证明是添加独立 proof 对象并建立依赖关联, 不是原地改写不可变定理卡. 这类平台状态与独立 kernel 的完整根证明重放属于不同证据. FLT 仓库提供了后者的运行入口及作者成功记录, 本次没有重放. [平台状态规范](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/prove.md), [声明与证明分离](https://prove2.me/about), [FLT 验证摘要](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/README.md).

## 1. 入口, 版本和对象

| 对象 | 本次查到的身份与版本 | 一手来源 |
| --- | --- | --- |
| FLT 公告 | Anthropic, 2026-09-04. 声称首次完整计算机检查的 FLT 形式化. 公告中的 first 是发布方的优先权主张, 本次未做全历史优先权审查. | [正式公告](https://www.anthropic.com/research/formalizing-fermats-last-theorem) |
| 平台论文 | Chen, Marwaha, Lu, Yuen, Peng. arXiv 2608.28433, v1 为 2026-08-28, 本次读 v2, 2026-08-31. 这是平台设计及案例论文, 不能单独当作 FLT 构建收据. | [版本记录](https://arxiv.org/abs/2608.28433), [v2 全文](https://arxiv.org/html/2608.28433v2) |
| 实际 FLT 证明 | `anthropics/fermats-last-theorem`, 本次 main 为 `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`, 提交时间 `2026-09-03T19:12:20Z`. tags / releases 均返回空列表. 仓库自述为不维护的研究工件. | [固定提交](https://github.com/anthropics/fermats-last-theorem/commit/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef), [tags](https://api.github.com/repos/anthropics/fermats-last-theorem/tags), [releases](https://api.github.com/repos/anthropics/fermats-last-theorem/releases), [README](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/README.md) |
| Prove2Me workspace | `6b46503a65c3a4252170ed5ca984a796b5a5b6b4`, `v0.9.8`, 提交时间 `2026-09-07T14:11:11Z`. 下文 workspace 文件均固定此提交. 不能据此认定 FLT 运行当时使用同一 harness 或生产服务端版本. | [固定提交](https://github.com/prove2me/prove2me_workspace/commit/6b46503a65c3a4252170ed5ca984a796b5a5b6b4), [tag 元数据](https://api.github.com/repos/prove2me/prove2me_workspace/tags) |
| 在线平台 | Prove2Me 是任务协作, 定理库和验证服务平台. 模型由贡献者的 agent 提供, Lean kernel 执行形式证明检查. 平台不是模型, 也不是新的 kernel. 在线 about / FAQ 未给固定发布哈希. | [about](https://prove2.me/about), [FAQ](https://prove2.me/faq) |

## 2. 完整 FLT 的目标与保真范围

本次直接读取 `Theorems/Thm_fermat_last_theorem.lean` 第 128 行: `fermat_last_theorem` 对任意自然数 `n >= 3` 和任意正自然数 `a,b,c` 断言 `a^n + b^n != c^n`. 目标没有指数上界, 不是某些有限指数或 regular primes 的结论. 该文件导入实际证明模块, 末尾调用 `P2MW.S_fermat_last_theorem.solution`, 已不是平台的 `sorry` 定理卡. 抽查的 solution 再调用 `FLT.fermatLastTheorem`. [目标声明](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/Theorems/Thm_fermat_last_theorem.lean#L128), [实际 solution](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/P2M/Sol/S_fermat_last_theorem.lean#L129).

`FinalCheck.lean` 声明 `flt_pinned` 和 `flt_mathlib : FermatLastTheorem`, 后者显式把 Mathlib 的非零自然数条件转成正数条件. 本次另读固定 Mathlib 的 `FermatLastTheoremWith`, `FermatLastTheoremFor`, `FermatLastTheorem` 定义, 与上述全称目标一致. 这是目标字面与桥接代码的静态核对, 本次未独立执行类型检查. [FinalCheck](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/FinalCheck.lean), [Mathlib 定义](https://github.com/leanprover-community/mathlib4/blob/db584cd6d46c92f209a44c0f1c829460d327499d/Mathlib/NumberTheory/FLT/Basic.lean#L52).

环境由 `lean-toolchain` 固定为 Lean `4.33.1`, `lakefile.lean` 与 `lake-manifest.json` 固定 Mathlib 为 `db584cd6d46c92f209a44c0f1c829460d327499d`, 即发布方标注的 `v4.33.0`. 提交说明称这是从 Lean `4.30.0` 移植而来, 本次未比较两个版本的全部源码. [toolchain](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/lean-toolchain), [Lake 配置](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/lakefile.lean), [依赖锁](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/lake-manifest.json), [移植说明](https://github.com/anthropics/fermats-last-theorem/commit/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef).

完整 FLT 不意味着每个著名中间定理的一般版本都已形式化. `PROOF-PATH.md` 明确限定: Mazur 部分针对 Frey 曲线的不可约性, Langlands-Tunnell 是 octahedral 情形, 模提升带指定素数及 level 条件, Ribet 部分针对 Frey 表示及 trace congruence. 正确表述是这些版本被用于完整 FLT; 不能扩写为一般 Mazur / Langlands / Ribet 理论全部完成. [证明路径与精确强度](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/PROOF-PATH.md).

## 3. 构建, 公理与第二 kernel 的证据等级

| 项目 | 发布方记录 | 本次实际查证与限制 |
| --- | --- | --- |
| Lean 构建 | 从源码编译 Mathlib 并完成 60,475 个模块, 公理只有 `propext`, `Classical.choice`, `Quot.sound`. | `FinalCheck` 确有 `#guard_msgs` 包围的 `#print axioms fermat_last_theorem`, 预期恰为三个公理. `formalization.yaml` 声称 `sorry_count: 0`, `literature_dependencies: []`, 但 `review.status` 同时是 `self-assessed`, `reviewers: []`. 本次没有全库扫描或重放. [检查入口](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/FinalCheck.lean), [自述元数据](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/formalization.yaml), [构建记录摘要](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/README.md) |
| comparator | 报告目标及所用常量与 Mathlib-only challenge 一致, 公理白名单通过, 整个环境经 Lean kernel 重放. | 已读 Challenge, Solution 和配置, 检查两个 FLT 声明, `enable_nanoda: false`. Challenge 的 `sorry` 是可信目标模板, 不应误计入已完成证明. 检查语义由 comparator 官方说明支持, 成功结果仍是作者记录. [Challenge](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/verification/comparator/Challenge.lean), [Solution](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/verification/comparator/Solution.lean), [配置](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/verification/comparator/config.json), [comparator 固定版说明](https://github.com/leanprover/comparator/blob/3927ad383f208ae977c340a91c48ac9b497d2097/README.md) |
| nanoda | 作者记录 Rust 独立 kernel nanoda `0.4.13` 检查 `1,052,234` 个声明无错误. | 单独的脚本导出同一 Solution 环境, 固定 nanoda `418320295890faed83a96fd97907b12a3b6728c2`, 公理白名单外项为 hard error. 这是独立 kernel 实现, 不是本次独立复现, 也不能据此称由独立第三方执行. [nanoda 运行脚本](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/verification/nanoda/run.sh), [配置](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/verification/nanoda/nanoda-config.json), [版本元数据](https://github.com/ammkrn/nanoda_lib/blob/418320295890faed83a96fd97907b12a3b6728c2/Cargo.toml), [作者结果摘要](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/README.md) |

必须随结果保留的限制:

- comparator 脚本默认获取 `v4.33.0` 的 comparator 与 lean4export, 并改用本项目 Lean toolchain. 本次解析 tag 分别得到 `3927ad383f208ae977c340a91c48ac9b497d2097` 和 `15f6055e299ad5b89345e533cc2192f4cc00f659`. 脚本记录说明实际运行使用 `fake-landrun.sh`, 没有构建沙箱. 这不等于证明不成立, 但不能把该运行描述为隔离的不可信输入审计. [运行脚本](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/verification/comparator/run.sh), [comparator tag](https://api.github.com/repos/leanprover/comparator/git/ref/tags/v4.33.0), [lean4export tag](https://api.github.com/repos/leanprover/lean4export/git/ref/tags/v4.33.0).
- nanoda 应用了作者的四个补丁. 本次读到的修改分别涉及逐声明日志, 参数比较次序, 缓存重置, 以及含 eager-mode 的失败比较缓存. 作者称不改类型规则, 本次只核实 diff 内容, 未证明这些补丁保持健全性, 未核实其上游合入状态. [四个补丁](https://github.com/anthropics/fermats-last-theorem/tree/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/verification/nanoda/patches).
- 固定提交的 `verification/` 完整树只有 11 个脚本, 配置和补丁文件, 未含原始成功日志. 公开 Actions 查询只返回一次成功的网页部署, 不是 Lean 构建 CI. 未查到可独立对账的完整运行收据; 不将摘要当作本次执行结果. [verification 树元数据](https://api.github.com/repos/anthropics/fermats-last-theorem/git/trees/0a5f551747b8111285488c705ae9c24251c3c35e?recursive=1), [公开 Actions](https://api.github.com/repos/anthropics/fermats-last-theorem/actions/runs?per_page=5), [网页部署记录](https://github.com/anthropics/fermats-last-theorem/actions/runs/33887573561).
- 作者报告构建为 96 jobs, 5 h 32 min, 内存峰值 153 GB; comparator 为 14 h 46 min, 峰值约 230 GB; nanoda 前需约 37.8 GB 导出, 检查约 30 min / 16 threads / 40 GB. 这些是特定运行的资源记录, 不能当作日常小任务默认成本. [资源说明](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/README.md), [comparator 资源说明](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/verification/comparator/run.sh), [nanoda 资源说明](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/verification/nanoda/run.sh).

## 4. Prove2Me 的证明组织与验证边界

| 机制 | 一手材料给出的具体行为 | 本次判断 |
| --- | --- | --- |
| Immutable definitions / statements / proofs | 平台定理卡保存类型和 `:= by sorry` 占位体, 证明是另外的 `theorem solution`. 已发布 Lean 声明及证明不可原地改写, 描述等元数据可改. | 这是稳定接口的设计. 不可变不等于已证明, 也不等于已部署内容寻址哈希体系. [about](https://prove2.me/about), [FAQ](https://prove2.me/faq) |
| Typed theorem stubs | solution 要匹配目标全部 binders 和结论, 自己的代码不能含 `sorry`, 不能导入自己的目标. 允许导入其他 Open 定理作为待完成子问题. | 本地或局部编译成功仍可依赖未证假设. 不能把 stub 的预期 `sorry` 与最终根证明的 `sorryAx` 混为一谈. [提交规范](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/prove.md) |
| 证明 DAG / 递归闭合 | 一个目标可有多份 proof-sketch. 对某一 sketch, 所有依赖均已证明才使它闭合; 任意一条完整路线可完成目标. `SKETCH_ACCEPTED` 区别于 `ACCEPTED`. | 逻辑上是备选证明之间的 OR, 每份证明的依赖之间的 AND. 根可达依赖要递归闭合, 无需证明全部废弃备选节点. 文档给出该设计, 本次没有服务端代码来验证跨节点循环检测及完整闭包实现. [about](https://prove2.me/about), [状态和归约规范](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/prove.md) |
| 定义内部依赖 | 定义文件必须没有 `sorry`, 服务端按文档获取传递 imports. 全项目导入指南特别指出, def 的证明依赖若接到 sorry stub 会污染消费者的 `sorryAx`, 必须在定义包内提供该证明. | 审计必须覆盖定义和 statement 的依赖, 不能只检查 solution 文件末尾. [定义规范](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/contribute.md), [导入指南 Phase 2](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/upload_full_project.md) |
| 公理和逃逸限制 | about 声称检查公理白名单, FAQ 声称阻断 escape hatches. | 本次能核实其文档承诺, 没有查到公开服务端 whitelist / validator 实现. 不把 FLT 导出工件的三个公理自动当作所有平台提交的已核事实. [about 信任说明](https://prove2.me/about), [FAQ 信任说明](https://prove2.me/faq) |
| 环境和缓存 | workspace 默认 Lean `4.33.1`, Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`. 文档使用 `lake exe cache get`, 区分共享下载缓存与每 workspace 的 `.lake`, 按环境隔离镜像定理. | 此 Mathlib pin 与 FLT 工件不同. 编译缓存用于开发加速, 不构成根定理独立验证收据. 服务端缓存键, 失效策略及缓存命中数据未知. [本地环境规范](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/lean-setup.md) |

本次还在 FLT 导出工件的 `P2M/Util.lean` 中看到 `#p2m_type_eq` 的定义相等检查和 universe 特化拒绝, 以及另一个只报 warning 的命令. 这是可读的具体实现例子, 不是已证明所有平台节点都调用相同强制门禁. [P2M 工具源码](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/P2M/Util.lean).

## 5. 审计职责, 协调和恢复

- 人工审计集中于 mission 目标, 相关定义和 milestones. 论文描述 captain 逐项确认后由 moderator 审核公开 mission. 中间 lemma 的推导正确性由形式证明闭合保证. 这一设计不保证中间定理的名称, 自然语言注释或一般数学解释都忠实. [论文 Sections 3.3, 4.4](https://arxiv.org/html/2608.28433v2), [FLT 强度边界](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/PROOF-PATH.md).
- Read-back auditor 只看 Lean 声明和依赖定义, 不看作者意图或原文, 要展开量词, typeclass 前提, 自定义概念和退化情形. 人类再将回译与原文比较. 文档还要求 Lean 声明修改后重做回译. 这是陈述保真审查, 不替代 kernel. [auditor 规范](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/mission_auditor.md).
- 文档差异: FAQ 说进行两次审计, 但 v0.9.8 captain API 文档将 `readback` 标为 optional, strongly recommended. 因此不能声称每个已发布对象都已强制接受独立回译. [FAQ](https://prove2.me/faq), [captain 的 read-back 字段和流程](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/mission_captain.md).
- 协调入口包括 canonical milestones, `graph`, `open-leaves`, decomposition, milestone 修改历史, 讨论和 backlinks. solver 被要求先读原文与失败路线, 搜索可复用声明, 再接入目标. 本次未找到通用任务 lease, exactly-once 调度器或 agent 故障恢复实现. [solver](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/mission_solver.md), [mission API](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/missions.md), [讨论规范](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/communicate.md).
- 异步接口返回 `job_id` / `submission_id`, 提交后的工作按文档可独立于断开的连接继续. 导入指南要求自写幂等 uploader, 调用前后记录状态, 先记 id 再轮询, 恢复时继续轮询, 不重新投稿; `202` 只代表入队, `PUBLISHED` 才代表发布完成. 这是可复用协议说明, 本次未找到已交付的完整 uploader 或进行中断实验. [导入指南 Phase 7](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/upload_full_project.md), [publish-job 规范](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/contribute.md).
- 弃用语义需按对象区分. FAQ 称弃用 proof 会使它退出默认 decomposition 并重开目标; contribute 文档称弃用 node 保留旧 imports 和证明状态. 本次没有调用接口确认对象差别和级联行为, 不能总结成统一的自动撤销保证. [FAQ](https://prove2.me/faq), [deprecation 规范](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/references/contribute.md).

## 6. 人工输入与实际规模

FLT 公告记录: 11 天, 数十个 agent, 约 60 亿 output tokens, 约 1,300 万 Lean 行; 生成约 30,300 个定理, 最终使用约 29,500 个. 所用模型为内部研究模型, 仅描述为能力大致相当于 Claude Fable 5.1, 不是公开模型的固定可复现版本. 作者称数学指导主要是偶尔的高层指令, 但还使用了已有的 DDT 论述, Mathlib, Imperial FLT 与 flt-regular 成果. 不能写成人工输入为零, 也不能称它发现了新的 FLT 数学证明. 精确 agent 数, 完整提示与人工交互量, 总输入 tokens, 缓存, 全运行硬件和总费用未知. [FLT 公告](https://www.anthropic.com/research/formalizing-fermats-last-theorem), [上游贡献 NOTICE](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/NOTICE).

论文的其他平台案例不是 FLT 统计, 作者明确承认案例间模型代际, 题目与收费口径混杂, 不能据此证明 harness 的因果加速. 其中 Bandit Algorithms 在论文为 6 agents, 本次 FAQ 为 4, 差异原因未知. [论文 Table 1 及限制](https://arxiv.org/html/2608.28433v2), [FAQ](https://prove2.me/faq).

## 7. API 与公开部分的简要边界

- workspace 提供 `/api/v1` REST 接口说明, 含查询 graph / open-leaves, 异步 verify 和 publish-job. 本次未访问需要鉴权的接口. 生产服务端版本, 循环检测, 实际公理过滤与缓存实现未知. [文档索引](https://github.com/prove2me/prove2me_workspace/blob/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/SKILL.md).
- 可读 workspace 包括 agent 文档, 示例和两个 Lean 元程序. 前者提取 `typeDeps` / `valueDeps`, 后者提取 elaboration 中的声明及 proof 边界和引用位置. 本次未执行它们. 固定树未见 LICENSE / COPYING, GitHub license 查询为 404; 后端源码和明确复用许可证未知. 不把官网的 open source 表述扩写为已核实可完整自托管. [固定文件树](https://api.github.com/repos/prove2me/prove2me_workspace/git/trees/6b46503a65c3a4252170ed5ca984a796b5a5b6b4?recursive=1), [提取脚本](https://github.com/prove2me/prove2me_workspace/tree/6b46503a65c3a4252170ed5ca984a796b5a5b6b4/scripts), [license 查询](https://api.github.com/repos/prove2me/prove2me_workspace/license).
- FLT 工件有明确 Apache-2.0 LICENSE, 包含 Lean 源码, 检查脚本和 nanoda 补丁; 上游贡献及网页第三方依赖需另看 NOTICE. 这些并非完整的 agent 运行 harness. 本次还查到 comparator, lean4export 和 nanoda 对应版本的 Apache-2.0 许可. [FLT LICENSE](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/LICENSE), [NOTICE](https://github.com/anthropics/fermats-last-theorem/blob/aa2d8b34692b16c70f699536de0d8e75b9a3e9ef/NOTICE), [comparator](https://github.com/leanprover/comparator/blob/3927ad383f208ae977c340a91c48ac9b497d2097/LICENSE), [lean4export](https://github.com/leanprover/lean4export/blob/15f6055e299ad5b89345e533cc2192f4cc00f659/LICENSE), [nanoda](https://github.com/ammkrn/nanoda_lib/blob/418320295890faed83a96fd97907b12a3b6728c2/LICENSE).

可供主协调器据此评估的事实边界: 稳定的目标和定义, 陈述保真审查, 条件证明 DAG, 根依赖闭合, 公理检查, 独立 kernel 重放, 缓存和任务恢复是不同层面的保证. 本次材料支持逐层区分它们; 没有提供一个可直接替换现有 2.0 方案的, 已独立复现的完整平台实现.

复查锚点: 本次下载的根定理文件 SHA-256 为 `b678bb152910351b3c968a1ae59829fe7bcde15157856d5740bf799bfd5127db`; 对应 solution 为 `a922fd533ad7a4a156092587f2eed1b2cb9a63f9d11675ab413a029ed59c5f1b`. 这两个哈希只标识抽查文件, 不是完整证明或运行收据哈希.
