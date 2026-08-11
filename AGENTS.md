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
