#!/usr/bin/env bash
# Sync the parent repo (origin) to the organizational fork (fork).
#
# This is the local/manual counterpart of .github/workflows/sync-fork.yml.
# It requires that the clone has both remotes configured:
#   origin  https://github.com/xsoc1/rigorous-open-math-research.git
#   fork    https://github.com/Zhongshan-Big-Jun/rigorous-open-math-research.git
#
# Usage:
#   bash scripts/sync-fork.sh
set -euo pipefail

repo="${1:-.}"
cd "$repo"

echo "== fetch origin =="
git fetch origin main

echo "== fast-forward local main =="
git checkout main
git merge --ff-only origin/main

echo "== push to fork =="
git push fork main

echo "== verify fork/main matches origin/main =="
git fetch fork main
origin_head=$(git rev-parse origin/main)
fork_head=$(git rev-parse fork/main)
if [ "$origin_head" != "$fork_head" ]; then
  echo "FAIL: fork/main is at $fork_head, origin/main is at $origin_head" >&2
  exit 1
fi
echo "OK: fork/main == origin/main ($origin_head)"
