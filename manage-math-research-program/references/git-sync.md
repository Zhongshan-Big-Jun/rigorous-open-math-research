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

## Parent-fork (parent/child) sync rule

The skill repositories use a parent + org-fork structure:

- Parent (authoritative): `xsoc1/rigorous-open-math-research` (public).
- Child fork (mirror for the org): `Zhongshan-Big-Jun/rigorous-open-math-research` (fork of the parent).

Sync direction is always **parent first, then operate the child fork**:

1. Update and push the parent repository first.
2. Then sync the child fork from the parent; never edit the child directly as the source of truth.

Local staging area `C:\Users\HuangZY\AppData\Local\Temp\skills-upload-20260810` keeps both remotes:

```bash
git remote -v
# origin   = https://github.com/Zhongshan-Big-Jun/rigorous-open-math-research.git  (child fork)
# personal = https://github.com/xsoc1/rigorous-open-math-research.git              (parent)
```

Sync the child after every parent update:

```bash
git -c http.proxy= -c https.proxy= fetch personal
git -c http.proxy= -c https.proxy= push origin main
git rev-parse HEAD personal/main origin/main   # all three must agree
```

If the fork relationship is lost (API shows `fork=false` on the child while the repo still exists), restore it by:

1. Renaming the detached child, e.g. `PATCH /repos/Zhongshan-Big-Jun/rigorous-open-math-research` with `{"name":"rigorous-open-math-research-detached"}`.
2. Recreating the fork: `POST /repos/xsoc1/rigorous-open-math-research/forks` with `{"organization":"Zhongshan-Big-Jun"}`.
3. Verifying the new child reports `fork=true`, `parent.full_name=xsoc1/rigorous-open-math-research`, and an identical HEAD commit.