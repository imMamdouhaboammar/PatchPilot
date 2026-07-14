---
name: repository-discovery
use_when: starting work on a repository, changing repositories, or resuming after stale context
---
# Repository Discovery

## Establish the baseline
Record:
- owner/repository and visibility
- default branch and current head SHA
- read/write permissions
- branch protection when visible
- primary language, package manager, and runtime versions
- repository instructions and architecture docs
- build, test, lint, type-check, formatting, package, and migration commands
- recent commits, open issues, active PRs, recently merged PRs, and CI state
- relevant backlog, roadmap, TODO, or milestone entries

## Read in this order
1. `AGENTS.md` or equivalent governance
2. README and contributor guidance
3. package manifests and lockfiles
4. current architecture documentation
5. target code, direct consumers, types, schemas, and tests
6. relevant issues, PRs, recent commits, and CI
7. backlog only after shipped behavior is understood

## Avoid duplicate work
Search code symbols and filenames. Compare the request with active PRs, recent commits, and closed issues. Do not rebuild a feature already present or collide with an active branch.

## Baseline output
Before writes, retain a compact note with starting SHA, requested scope, current behavior, likely files, validation commands, overlapping PRs, and known risks. Use `templates/TASK_BRIEF.md`.

## One repository per chat
Do not transfer package managers, branch names, paths, architectural rules, or conventions between repositories. Start a new chat or reset the baseline when the repository changes.
