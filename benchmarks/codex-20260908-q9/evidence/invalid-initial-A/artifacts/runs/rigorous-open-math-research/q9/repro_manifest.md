# Reproducibility manifest
Input: TASK.md. Restrictions: statement/workspace/tools only; no network or other projects.
Tools: Python 3.14.4 standard library; no scipy, numpy, sympy, mpmath, Lean, or lake.
Git status unavailable: observed /dev/null permission denial. Git metadata is read-only; no remote sync authorized or attempted.
Workflow doctor.py was statically inspected: it reads global Codex configuration and invokes plugin/marketplace commands outside the task. Those operations are omitted under the user's scope and filesystem restrictions. Installed dependency SKILL.md files were directly confirmed readable. This is a restricted-environment adaptation, not a doctor PASS.
Lean decision: machine verification unavailable; independent mathematical audit will be used. No formal-verification claim.
