# Math Research Workflow 插件

管理-研究-验证一体化的数学研究流水线编排插件。

## 组成

- `.codex-plugin/plugin.json` -- 插件清单
- `skills/math-research-workflow/SKILL.md` -- 编排协议 (三阶段流水线 + 子 agent 分工)
- `skills/math-research-workflow/references/workflow-design.md` -- 设计文档 (角色/交接/并行/失败处理)
- `assets/pipeline-handoff.template.md` -- 阶段交接记录模板

## 依赖的 skill

| Skill | 阶段 | 职责 |
| --- | --- | --- |
| `$manage-math-research-program` | A 管理 | 程序上下文、任务包、工具库、git 同步 |
| `$rigorous-open-math-research` | B 研究 | 契约、多路线、对抗审计、候选证明 |
| `$lean-verify` | C 验证 | Lean 形式化、机器验证、义务级审计 |

## 安装

```text
codex plugin add math-research-workflow@personal
```

## 使用

用户请求数学项目全流程 (研究 + 形式化验证 + 同步) 时, 本插件编排三阶段流水线;
各阶段内部按子 agent 分工并行, 阶段边界强制交接契约与 git 同步.
