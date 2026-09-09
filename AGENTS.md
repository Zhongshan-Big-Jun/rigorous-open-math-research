# AGENTS.md

## 仓库与当前工作

Codex marketplace `math-research`, 包含四个可独立使用的数学研究插件. 2.0 将默认行为改为简短工作引导, 核心是长期研究知识, 可批注文献工具库, 实际证据与中断续接.

当前版本字段统一为 `2.0.0`. 版本化实施和验证记录见 [docs/v2.0-implementation-status.md](docs/v2.0-implementation-status.md); 远程执行查对应提交的 CI, 本机安装查实际 plugin list 和缓存哈希. 方案记录在 docs/v2.0-refactor-plan.md.

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

普通研究不要求固定阶段, 角色, 台账或默认 Lean 验证. `validate_pipeline.py` 默认只检查当前续接数据; `--legacy-v1` 明确进入历史协议检查. 旧 proof, audit, source, annotation, sealed checkpoint 保持身份, 现有 Blueprint receiver 仍保护实际 canonical 写入.

已完成 L1/Q9 实验不得自行续跑. 原报告保留为 1.x 证据, 不用于宣称 2.0 的新发现或普遍提速. 新研究实验与已知证明的工程回放分开记录. 用户明确不关注额度, 不恢复额度查询, 保留线或重置流程.

## 同步与安装

- 父仓库: `xsoc1/rigorous-open-math-research`, fork: `Zhongshan-Big-Jun/rigorous-open-math-research`.
- 按 `project.json` 先推父仓库, 再同步 fork. 不强推或覆盖远程新增工作.
- DSH canonical clone 为 `~/.dsh/_math-research-upstream/rigorous-open-math-research`, 不把 `_xsoc1_work` 当它的长期替代源.
- 父仓库发布后, 在 `C:/Users/HuangZY/.dsh/math-research-dsh` 运行 `scripts/sync-from-parent.py` 单向继承, 按该仓库规则验证和发布.
- Codex 安装后核对实际 marketplace, 版本, 入口路径与脚本哈希. 本任务加载的旧技能不会自动变成新版; 新任务加载已安装版本.

## 会话摘要

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
