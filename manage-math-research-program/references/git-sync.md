# Automatic git repository sync

Conventions for keeping a research-program repository synchronized with its
remote from inside the agent.

## When to check

- At session start (workflow step 0): verify the working tree and remote state before building new work.
- At every stage close (workflow step 9): commit and push the stage.
- Before delegating a run: ensure the task packet and indexes are committed so the run root is reproducible.

## Commands

Status and sync check:

```bash
git status --porcelain   # uncommitted and untracked files
git fetch                # update remote refs
git status -sb           # ahead/behind vs upstream
```

Commit and push a stage:

```bash
git add -A
git commit -m "<descriptive stage summary>"
git push
git status -sb           # expect: working tree clean, up to date with origin
```

## Proxy note (Windows)

If the global git configuration points to a local proxy that is not running
(for example `http.proxy=127.0.0.1:7897`), override it per command:

```bash
git -c http.proxy= -c https.proxy= fetch
git -c http.proxy= -c https.proxy= push
```

Do not change the user's global proxy configuration without asking.

## Hygiene rules

- Keep secrets, credentials, tokens, and API keys out of commits; add them to `.gitignore` or keep them outside the repository.
- Ignore generated caches: `__pycache__/`, `*.pyc`, `.DS_Store`, `Thumbs.db`.
- Update `AGENTS.md` session records before committing so history is traceable.
- Commit after each substantial stage; small incremental commits are preferred over one giant commit.
- On push failure (network or proxy), keep the local commit, record the failure in the activity log, and retry; never silently drop local work.
- A clean synchronized repository is part of stage completion, not optional bookkeeping.
