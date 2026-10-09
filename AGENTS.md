# AGENTS.md

## 仓库与当前工作

Codex marketplace `math-research`, 包含四个可独立使用的数学研究插件. 2.0 将默认行为改为简短工作引导, 核心是长期研究知识, 可批注文献工具库, 实际证据与中断续接.

当前版本字段为 `2.0.1`, 用于第二轮审计后的检验与纠错修补, 已完成本轮有范围的验收. 2026-09-20 用户授权同步两个云端主仓库; 本机安装状态另行核对. 2.0 基线实施记录见 [docs/v2.0-implementation-status.md](docs/v2.0-implementation-status.md); 新修订见 [docs/v2.0.1-verification-corrections.md](docs/v2.0.1-verification-corrections.md). 远程执行查对应提交的 CI, 本机安装查实际 plugin list 和缓存哈希. 原方案记录在 docs/v2.0-refactor-plan.md.

## 工作方法

1. 修改前读取本文件, 检查 Git 状态与相关代码调用. 保留无关用户变更.
2. 修改 skill 或元数据时更新相应版本; 本轮用户指定 2.0, 不使用日期 cachebuster.
3. 修改 manage skill 内文件后运行 `python3 scripts/regen_manifest.py plugins/manage-math-research-program/skills/manage-math-research-program`.
4. 每批修改后运行 `python3 -X utf8 scripts/validate_all.py`, 再运行与行为有关的 tests. 发布前完成 CI 所列检查与真实 Lean 正负对照. 测试数学范围与执行状态, 不用提示词关键词充当行为测试.
5. 文本使用 UTF-8 无 BOM 与 LF. 新代码用 tab 缩进, snake_case 函数名和 PascalCase 多词变量名, 使用英文标点.
6. 每次维护在此保留简短的具体对话与方法摘要, 长记录写入专门报告或 AGENTS_HISTORY.md.
7. 如实记录实际验证. 入口缩短不等于研究提速, 数据迁移不等于数学结论升级.

## 结构与兼容性

- `.agents/plugins/marketplace.json`: 四包顺序与 Codex 渲染顺序, 保持既有 ID.
- `plugins/<name>/`: manifest, 简短 SKILL, 按需参考与可执行工具.
- `tests/`, `.github/workflows/validate.yml`: 行为与发布验证.
- `benchmarks/`: 不可改写的实验输入, 回答, 证书, 审计与成本原件.
- `docs/`: 当前实施与指南, 方法调研和历史设计.

探索不要求固定阶段或台账. 2026-09-20 用户要求正式检验由无状态隔离子 agent 执行: 新会话, 不继承作者上下文, 冻结最小证据包; 作者自检不算独立验收. 研究中融入 Lean 反馈, 明示未形式化步骤; 外部错误报告先保全证据并暂停受影响复用, 修订与独立复核后恢复. `validate_pipeline.py` 默认只检查当前续接数据; `--legacy-v1` 明确进入历史协议检查. 旧 proof, audit, source, annotation, sealed checkpoint 保持身份, 现有 Blueprint receiver 仍保护实际 canonical 写入.

已完成 L1/Q9 实验不得自行续跑. 原报告保留为 1.x 证据, 不用于宣称 2.0 的新发现或普遍提速. 新研究实验与已知证明的工程回放分开记录. 用户明确不关注额度, 不恢复额度查询, 保留线或重置流程.

## 同步与安装

- 父仓库: `xsoc1/rigorous-open-math-research`, fork: `Zhongshan-Big-Jun/rigorous-open-math-research`.
- 按 `project.json` 先推父仓库, 再同步 fork. 不强推或覆盖远程新增工作.
- DSH canonical clone 为 `~/.dsh/_math-research-upstream/rigorous-open-math-research`, 不把 `_xsoc1_work` 当它的长期替代源.
- 父仓库发布后, 在 `C:/Users/HuangZY/.dsh/math-research-dsh` 运行 `scripts/sync-from-parent.py` 单向继承, 按该仓库规则验证和发布.
- Codex 安装后核对实际 marketplace, 版本, 入口路径与脚本哈希. 本任务加载的旧技能不会自动变成新版; 新任务加载已安装版本.

## 会话摘要

- 2026-09-20 云端候选 `6b8b0d6` 的 Windows job 在 checkout 阶段因归档检验包路径超过 MAX_PATH 失败, 行为测试尚未执行. 保存真实 CI 日志, 在 maintenance-runtime 的 Git 进程环境中设置 core.longpaths, 保留冻结包的原路径和字节, 不修改已获独立批准的运行时代码. Linux 同矩阵任务的取消记录与这次检出失败分开; 修复后以新提交的完整 CI 为准.

- 2026-09-20 用户要求同步 `xsoc1/rigorous-open-math-research` 与成果仓库. 本次按 2.0.1 修缮清单提交源码、使用说明、真实隔离检验回执与测试证据, 先核对远端基线, 再按 `origin`、`fork` 顺序同步. 暂存逐文件清点并核对实际 Git blob 与冻结哈希; 未关联的本地 benchmark 和研究草稿保留. 精确候选提交执行云端 CI, 不以旧测试结果代替本次远端状态; 不改写历史未发布记录, 本机安装及 DSH 迁移不属于这次两仓库同步.

- 2026-09-20 软件最终复核完成: Bohr 新会话仅接收冻结包, 批准当前两个软件义务, 83 项所供测试与另写 10 组独立检查通过. 协调器完整套件 Linux/Windows 各 84 项通过 (额外含 1 项 Q9 复用). 原 WSL 回执不能在原生 Windows 路径直接消费, 该限制保留; 真实项目恢复使用原 WSL 路径, 不改写调度记录. 本轮仍是未发布的 2.0.1 工作树.

- 2026-09-20 CL7 补修: 新检验确认 CL6 后发现同一路径的多个依赖版本被检验输入字典覆盖. 已在登记、旧记录读取和完整输入汇集处拒绝冲突; 新增旧版本库及修订本体被依赖覆盖的两个回归, Linux 84 项通过. 新会话 Bohr 验收中, 数学检验包及原问题/修订身份不变.

- 2026-09-20 第二轮修补的后续独立复核: 先修正日志截短漏检、格式损坏卡片旁路、中断登记与路径别名; 实际进程退出测试及显式旧日志迁移通过. 新检验又发现 CL6: 上游单卡批准会自动解除下游义务. 已改为先计算完整受影响闭包再逐卡应用批准, 增加直接/传递依赖复现, Linux 82 项通过, 新无状态会话继续验收. 不把作者测试或旧软件批准用于恢复当前卡片.

- 2026-09-20 用户输入 `proof_audit_round2_20260920.md`, 要求修缮数学内容并增强隔离检验、过程内形式化和工具库纠错. 读取前轮修订后另存两仓库基线, 保留未提交 benchmark 与数学变更. 分离作者处理谱域、比值证明、纠错代码与局部 Lean 桥; 验收另启无上下文 agent. 新检验包/回执模块首批 11 个正负行为测试通过. 真实 K1 首轮隔离检验发现工具卡遗漏有限公式范围与极限归一化, 已据此修订并保留否决回执; 不把该轮标成全体通过. 最终范围与验证见本轮报告.

- 2026-09-09 用户要求依据已讨论方案先落地 2.0, 改善插件与成果仓库 README, 整理内容并清理冗余代码, 将 Sturm-Liouville 项目标识为使用插件的成果仓库. 方法: 先备份成果仓库 68 个既存变更文件及哈希; 在独立分支实施, 分离 Lean, 文献经验库和成果仓库写入范围; 协调器改短入口, 续接, 兼容检查, 文档与发布. 首批 81 项结构校验和旧 sealed checkpoint/closure 测试通过. 新续接 13 项行为测试通过, 覆盖实际进程中断, 重复执行防护, 旧结果失效和过期写入. 最终集成结果持续记入实施报告, 不据此提前宣称发布完成.
- 历史决策与实验细节见 [AGENTS_HISTORY.md](AGENTS_HISTORY.md), 按问题检索.
- 2026-09-09 用户澄清 "继续, 刚刚是意外暂停". 已从保留的工作树和外部证据续接, 核对原任务状态后继续最终验证和发布. 丢失的 agent 会话不视为任务成功或数学失败. 26 项文献/经验测试与 7 项旧文献兼容测试通过, 最终运行时与发布状态仍见实施报告.
- 2026-09-09 最终验收: 新会话经卡片/批注/原文指针完成实际论文的有范围复用, 并据其反馈补齐 query 的 scope 字段. 独立续接检查复现的并发保存, 启动后误报, 输入变化再还原等问题已修复; Windows 24 项通过, Linux 22 项通过及 2 项平台跳过. Lean 11 项真实编译/交互测试及 12 项便携测试通过, 18 个兼容脚本与 81 项仓库校验通过. 两个独立最终复核与实际发布尚待完成, 不把数据健康或进程成功等同于数学证明.
- 2026-09-09 续接复核补修: 对损坏 observations 的形状逐记录隔离, 子进程超时改由独立 watcher 从创建时计时, 不受状态写入重试拖延. 26 项测试在 Windows 全部通过, Linux 24 项通过及 2 项平台跳过. Lean 审查的三项依赖/模块解析问题继续修复, 冻结原始反例供独立复核. 成果仓库只暂存清单指定的 157 个路径, 逐个比较实际 blob, 44 项无关既存变更保留原字节.
- 2026-09-09 独立续接复核已关闭全部已报告缺陷; 两平台复现与成功对照见 docs/v2.0-evidence/recovery-review.json. 成果仓库清理提交 ee90dcc 已同步到主仓库和 fork. 插件本体仍待 Lean 修复及最终发布, 不混用两仓库的交付状态.
- 2026-09-09 最终集成: Lean 三项修复已冻结并通过真实负例和成功对照; 81 项结构检查, 18 个兼容脚本与 12 项便携检查再次通过. 按 lean-action 官方配置补齐最小 Lake fixture, 实际 Lake 4.31.0 生成 manifest, action 配置检查通过. 完整真实 Lean 回归和独立复核仍在运行.
- 2026-09-09 Lean 14 项完整集成在上一冻结版本通过, 独立复核确认原三项缺陷关闭, 又发现普通记号提供者可在 elaboration 后消失于类型依赖, 使旧收据错误保持 current. 现改为绑定全部实际载入模块并核对数量, 语义复核仍保留较小的类型/定义依赖身份. 新增预期类型和源类型的记号变化对照. 首次新测试因测试期望标签写错而主动中止并留档, 修正为实际 incomplete 后改用 Windows 原生 Python 验证; 不降低哈希或依赖范围. 发布仍待这次修复复核.
- 2026-09-09 完整模块版本的本机正负对照通过: 协调器的两种记号用例和四次实际验证通过, 独立 agent 的九项断言及另外四次验证全部通过, 13 个源码哈希保持冻结. 当前 15 项真实 Lean 套件由 CI 对具体提交执行. 上述摘要保留各阶段状态; 不把旧通过记录或磁盘中新版本目录视为当前 CI 与安装状态的替代.
- 2026-09-09 最终独立 Lean 报告已封存, 受审范围 PASS 且无剩余实质性发布阻塞. 候选版本按精确提交运行当前 CI, 再同步主分支, DSH 和实际 Codex 安装; 用真实回执核对来源与哈希.
- 2026-09-09 候选 c7c632e 的首次 CI 中, 结构检查, 兼容测试及 Linux 工具测试通过, Windows 续接和真实 Lean 失败. 已下载实际日志及编译产物定位. 续接底层入口统一解析根目录, 测试同时覆盖非规范根路径与 Windows 短路径, 并等待完成结果对应的 supervisor 关闭后清理临时目录. 27 项测试在 Windows 全部通过, Linux 25 项通过及 2 项平台跳过. 该次 CI 的失败记录保留, 修复后继续按新提交验证.
- 2026-09-09 真实 Lean 的失败定位为检查文件在项目外运行时丢失 Elan 的项目版本选择. 生成文件仍存入独立证据目录, 编译和检查的工作目录保留在原项目, 不修改全局默认版本. 实际命令目录加入现有真实测试断言; 81 项结构和 12 项便携检查通过. 修复候选分支的完整 CI 与剩余针对性复核并行, 主分支发布仍以完成结果为准.
- 2026-09-09 候选 edc5b3a 的 Windows 续接 27 项全部通过, 独立复核也未发现剩余问题. 随后文献库测试暴露同一短路径环境下的测试夹具比较问题: 故障注入未命中目标 README. 仅将该测试根目录归一化, 文献库运行时代码保持原身份, 并重建对应 skill 的文件清单. Lean 的无全局默认版本对照, direct/Lake 两种运行与两个真实回归测试已通过, 完整云端测试继续核对.


## 2026-10-09 联合 Lean 开发本地修订 (核验中)

用户本次明确授权在既有 lean-verify 中增加实际证明开发入口, 结合真实研究工程检索/候选/反馈/修订/保存/最终根并适配原workflow与独立审查. 本次新授权优先于更早单轮不改插件及2.0版本边界. 四组件及marketplace ID保持. 当前本地冻结v3为lean-verify2.1.2/manage与workflow2.0.2/rigorous2.0.1; 不代表全局已安装skill升级. 新入口lean_develop.py复用原工具, 新研究定义只在研究仓库. 原v1/v2真实独审退回完整保留; v3拒绝输出与项目重叠, 完整绑定严格验证工具, 将终末慢读取置于共同时序边界, 长类型无省略导出仍失败时返回未完成. 通用512叶working smoke、便携21及validator81已执行, 冻结版真实/便携/续接套件与研究三根正在执行, 独立新身份修补验收待完成. 用户后续要求cmd隐式调用, 所有新增子进程采用隐藏窗口选项并已有原生GetConsoleWindow=0实测. 本轮不提交/推送/发布/全局安装或canonical写入; 保留原dirty/benchmark和冻结回执.


## 2026-10-09 联合 Lean 开发本地验收完成

用户本次要求在既有lean-verify实现证明开发并与真实SL数学相互验证, 后续要求cmd隐藏调用. 新lean_develop复用原反馈/验证/路线/workflow, 增加项目与固定mathlib检索、真实接口probe、warm候选trial/save、非空目标清单和durable start/status, 宿主负责证明候选. 同前缀共享导入库、Windows UTF8/隐藏进程及真实task_name/fork_turns=none review适配均有实测. 原v1/v2负审查及复现保留; 输出覆盖、完整工具身份、末尾慢读取共同epoch及无省略类型修补完成.

最终v4冻结241文件SHA4715506ebda0a77c5db14f8a77fa2deceba3d882b35543b268b811931bb2efc7, lean-verify2.1.2/manage与workflow2.0.2/rigorous2.0.1. v4开发11、便携21+12、workflow28、validate81实际通过; v3 oldreal15实际通过且30运行脚本/template/schema与v4相同, v4只改测试注入fixture; manage87仅此前源相同执行. 不伪称全部v4重跑. 真实研究10模块/3合取根严格v3执行通过, 最终v4同字节trial/save/status通过; 完整类型盲读和不同原文语义审查分别通过. fresh /root/plugin_review_v4修补审查APPROVED并由既有receiver真实接收, 限制与检查范围保留原件.

实际源码配对/命令/原生回执集中在F:/LaTeX/BVE research/research/artifacts/lean-development-20261008/README.md及SOURCE-PAIRING.json, 软件全测试在F:/tools/lean-joint-20261008/plugin/TESTS-v4.json. 研究专用对象未硬编码进插件, 全局已安装缓存未改. 本轮只本地, 未提交/推送/发布/安装或canonical/工具库接收, 原dirty/benchmark/历史前缀保留. 原机器字段不因后来的语义审查重写, 原受保护全库build失败和数学完整幂域/完整谱缺口继续明确.


## 2026-10-09 manage 问题知识复用改进 (本地验证中)

用户要求从既有卡片/文献/批注/纠错/路线比较增量实现面向当前问题的检索、完整条件、紧凑知识包及 Lean 真实结果消费. 当前 manage 开发版本2.1.0, 沿用 tool-pointers/v2、原 issue/revision/review/release 和前轮唯一 research_review 原生适配; 后者源码不改. 不复制验证器或另建调度器. 新 research_context.py 由原 research_library CLI 暴露 query --context/read/context, 检索相关性不证明数学适用性; 当前字段/历史字段、未知依赖、语义/精确根/开放连接/接收分开.

真实 SL 只用隔离的少量原文和本轮非冻结候选区, 另有无 SL 名称/不同布局 fixture. 原 dirty/benchmark/冻结 Lean 字节保留; 安装缓存未改. cmd 子进程隐藏. 当前在验证冻结源码、同语料五问及新无状态独审; 作者回归不算独立验收. 不提交/推送/发布/全局安装/canonical 写入. 具体记录追加 AGENTS_HISTORY.md, 交接入口为研究工程 research/artifacts/manage-context-20261009/README.md.


## 2026-10-09 manage 独立退回与 v5 修补

真实 v3 独审退回继承条件上下文命中、等价引用路径及关系依据门禁三处; v4 全新两人确认三处修正, 又独立复现正文单词命中被泛化上下文挤掉及 warm Python 将新磁盘源码误记为旧代码生产者. 原始 v3/v4 packet、完整 native FINAL_ANSWER、receiver 负面回执在 F:/tools/manage-context-20261009/review-project 保留, 不覆盖为批准.

当前 v5 按实际查询词、目标词、纯上下文分层选择, 在 Python 载入时绑定源码/版本并在生成与导出重查, 源更新要求新进程. 实际28项 context 回归通过; 冻结244文件 SHA3b06bac8d04ff29048a1cdd7d34e767c834d24b3b8ea7b7335d2b459f5e73b8e, manage2.1.0, 便携115项为114通过/1可选Q9跳过, 源仓库Q9另实跑通过, 库7项/gateway/validate81通过. 新原生独审 /root/manage_software_review_v5 与 /root/manage_forward_review_v5 已实际 fork_turns=none 派发, 完成结果待后续追加. 五问同一12卡语料重跑, 不把旧检索已有正确命中归功于新增能力.


## 2026-10-09 manage 捕获来源门禁修补 (v6)

fresh /root/manage_forward_review_v5 对所供五问及同语料增量 APPROVED, 限定研究复用而非重批证明. 独立 /root/manage_software_review_v5 又复现 source_id 不查捕获组成文件的 P1 旁路并 CHANGES_REQUIRED, 已由原 receiver 接收完整真实回执, v5 不作为最终软件批准. v6 将 source.json/raw.bin/text.txt 的精确实时门禁聚合到 source_id, 当前比较/理解页、关系/影响与导出一致; 原 source_id/捕获字节/纠错 release 协议不改.

29项 context 及最终冻结116项实际通过(115通过/1可选Q9跳过); 源仓库Q9另执行通过, 库7/gateway/validate81通过. 测试最初将三个组成文件案例用相同原文字节串联, 第三案因之前 raw 隔离正确拦截而失败; 保留原失败log, 用不同字节区分三案并另加同字节新捕获ID不可逃逸检查, 没有弱化门禁. 冻结v6 244文件 SHA d0bf6ee821769d5050d74faf8277a7af9209bdf49f98db6f3c8459afef4e7764. fresh /root/manage_software_review_v6 的原生最小包10项输入已实际派发, 最终结果待后续追加. SL原文/12卡语料不变, v6五问重跑与v5取回相同材料, 原34项门禁阻断保留.


## 2026-10-09 manage 捕获标题别名修补 (v7, 独审中)

fresh /root/manage_software_review_v6 确认三份捕获文件各自门禁修补, 又实际复现仅改标题产生新 source_id 可绕过旧 source.json 隔离, 因而 CHANGES_REQUIRED. 原完整负面 native 完成及 receiver 回执保留. v7 以原 URL/version/raw/text 的精确四元组查已登记元数据版本快照, 对 source_id 和等价 source.json 路径统一门禁; 标题/阅读标注不解除旧义务, 不同来源或版本的元数据不合并. 原 source_id 计算、捕获字节及 release 协议不变.

30项 context 实际通过, 冻结244文件 SHA 2f7a4740dcb7bc9a78b19c0b8318b636524b587c055218d916923d2c103ce049; 117项便携为116通过/1可选Q9跳过, 源仓库Q9另实跑通过, 库7/gateway/validate81通过. 同一12卡/11原文五问已用v7重跑; 主库原34项阻断、历史替代及默认Lean未知实查通过. 实际 fork_turns=none 派发 /root/manage_software_review_v7, 原生最小包11项输入, 当前软件最终结果待完成; v5五问正向批准的版本/范围另保留. 本轮仍只本地, 原数学/冻结证据不改.


## 2026-10-09 manage 双重选择与登记身份修补 (v8, 独审中)

fresh /root/manage_software_review_v7 确认捕获标题/路径与耐久快照修补, 又实际退回两项: path优先使source_id聚合门禁被压制; 元数据正常登记后共同隐式文件名source被误作工具身份. 完整negative native完成及原receiver回执保留. v8对path/source_id独立绑定并拒绝矛盾, 对捕获元数据按原URL/version/raw/text投影身份, 不改旧登记字节或release义务. 相同捕获别名及其精确依赖仍受影响, 不同来源/版本正常登记后及其消费者不再误合并.

最终冻结244文件 SHA872931bf222dc54915d80ffd412c8a98d3d1a987781c05e71847257fa0de5aa3, manage2.1.0. 实际119项便携=118通过+1缺材料Q9跳过, 含32项context; source Q9另实跑通过, 库7/gateway/validate81通过. 本轮两项新回归覆原/标题别名的source_id+自身raw/text、错误sha/矛盾路径、比较读回/理解页/关系impact/导出, 以及登记前后不同URL/version、同捕获别名依赖及旧记录字节. 五问v8同原语料已重跑. fresh /root/manage_software_review_v8 实际fork_turns=none派发, 原生12项输入, 当前最终软件结果仍待完成; v5正向批准限其当时范围. v7全量保护检查已通过, 本轮新修补后的最终保护另核对. 没有新数学证明、全局安装/发布或canonical/原工具release.


## 2026-10-09 manage 捕获成员与首次纠错导出修补 (v11, 独审中)

作者实际复现v8缓存identity投影字段可压制已知隔离, v9改由绑定材料重建. fresh v8独审随后真实退回两项: path-only raw/text逃逸捕获metadata/别名义务; 首个issue未改变预登记catalog/自定义index时旧知识包仍可导出reuse/impact. 完整negative native回执已由原receiver接收, 不以测试通过解除退回. 当前v11统一识别三个捕获成员路径, 绑定纠错状态的存在/缺失及版本, 导出重查来源与关系许可; 旧导出与纠错协议保持原字节. 两项新回归实跑通过, 新冻结244项SHA9312ce7ae3abb217a7808df9e348c96289b874efe9bdcea5e28e73dfb8ddc088. full测试/最终软件独审正在完成; v9/v10的真实派发已中止且没有完成/批准, 不能据此宣称验收.


## 2026-10-09 manage 当前声明与耐久身份修补 (v13, 独审中)

fresh v11独审完整CHANGES_REQUIRED已由原receiver接收: cache.tool_id覆盖当前声明, 正常reindex还会登记错误耐久ID, 随后无缓存read仍放行. 当前读取/增量刷新以源码显式tool_id/slug优先; live gate另从精确Markdown快照同时保留原耐久ID与源码声明ID的各项义务, 不改旧绑定字节或自动release. 缓存计算字段均不能替代该投影; 仅索引声明的旧ID兼容继续保留. 三项针对性回归4.566s通过, 冻结v13为244项SHA3a18b98aefb24764b4d038aa705a1787316cc7a82c6543d1d5894dd9b5087f74. 全122项及新上下文软件独审正在完成, v12只有作者中间冻结、没有审查派发/完成. 本条不作提前验收; 数学范围/本地边界与原34项隔离不变.


## 2026-10-09 manage 问题知识复用本地增量完成

manage2.1.0最终冻结v13与工作树244文件逐字节配对; 实际便携122项为121通过/1缺材料Q9跳过, source Q9另实跑通过, 库7/gateway/validate81通过. 同12卡/11原文五问、原34项阻断、精确历史替代导航和默认Lean未知实查. fresh五问正向v5及最终软件v13分别APPROVED并经原receiver接收, 所审版本/范围分开, v3-v8/v11真实退回及v9/v10未完成中止保留. `F:/LaTeX/BVE research/research/artifacts/manage-context-20261009/README.md` 为当前入口. 最终源码、原文、测试、真实回执与未做检查见SOURCE-PAIRING; 未将软件批准当新数学证明/完整形式化. 只本地, 未提交/推送/发布/全局安装/canonical或解除原纠错义务. 已有续接与理解页保留人的原字节和开放连接; 最终保护结果单独链接.


本轮最终保护检查实跑通过: 研究21782份、插件1233份起点文件逐项SHA核对, 原文件无丢失及范围外变化; 原正文/人的前缀与续接历史字节、主index、唯一review适配器、canonical/inventory和Git HEAD/分支/暂存均保持. 当前244份源码与v13冻结配对. [实际保护结果](<F:/tools/manage-context-20261009/preservation-final-v13.json>) 单列; 最后追加的说明另做小范围字节/链接检查, 不据此增加数学批准或发布.


## 2026-10-09 最新插件与研究仓库上传授权

用户在两项本地开发验收后明确要求"上传推送最新版本插件与研究仓库", 授权发布本轮Lean/manage联合增量. 按原origin-first/fork顺序, 精确清单提交, 候选CI与远端读回另留实际证据. 不纳入原benchmark文件及AGENTS中更早未提交记录, 不修改全局安装或canonical. v13冻结244源码身份保持, 新发布指南/证据仅作引用, 不继承数学批准. 实际结果以F:/tools/joint-publication-20261009/DELIVERY.json及远端为准; 本条不提前报告推送完成.
