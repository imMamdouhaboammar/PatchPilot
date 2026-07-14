# Skills Index

Use this file as a dispatcher. Read only the skill files needed for the current task. Repository instructions and current code override these general workflows.

## Always load

- `skills/TOOL_ROUTING.md` when deciding how to inspect, test, or write.
- `skills/SECURITY_AND_TRUST.md` before any write action.
- `skills/PR_CREATION.md` before opening or updating a PR.

## Load by task

| Situation | Read |
|---|---|
| First contact with a repository or a new chat | `skills/REPOSITORY_DISCOVERY.md` |
| Bug, feature, refactor, docs, CI, maintenance, or PR repair | `skills/TASK_MODES.md` |
| Branching, edits, commits, remote drift | `skills/CHANGE_EXECUTION.md` |
| Tests, sandbox checks, GitHub Actions, CI failures | `skills/VALIDATION_AND_CI.md` |
| Architecture docs, modules, routes, schemas, public interfaces | `skills/ARCHITECTURE_ANALYSIS.md` |
| Long sessions, many PRs, or a new continuation chat | `skills/CONTEXT_CHECKPOINTS.md` |

## Templates

- `templates/TASK_BRIEF.md`: establish scope before edits.
- `templates/PR_TEMPLATE.md`: mandatory PR body.
- `templates/SESSION_CHECKPOINT.md`: continuation memory.
- `templates/ARCHITECTURE_MAP_TEMPLATE.md`: use only when architecture mapping is justified.
- `templates/VERIFICATION_HANDOFF.md`: guide the independent reviewer.

## Skill invocation rule

Before acting, identify the task type, search Project files for the matching skill, read it, then apply it. Do not load every file by default. If a skill conflicts with repository governance, follow the repository.
