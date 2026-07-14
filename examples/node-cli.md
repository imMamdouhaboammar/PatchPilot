# Example: Node.js CLI repository

This preset shows how to wire PatchPilot to a typical Node.js command-line
tool repository. It is meant to be read once when you first set up the
ChatGPT Project, then left alone.

## Repository shape

```text
my-cli/
  package.json
  package-lock.json
  tsconfig.json
  src/
    commands/
    lib/
    index.ts
  tests/
  README.md
  CHANGELOG.md
  AGENTS.md
```

## What PatchPilot should know upfront

Add this to the top of the first onboarding chat:

```text
This is a Node.js CLI repository. The runtime is Node 20 LTS, the
language is TypeScript strict mode, the package manager is npm, the
test runner is vitest, the linter is eslint, and the formatter is
prettier. Releases are cut with changesets. Default branch is
`main` and is protected.
```

## Skills to load by default

| Skill | Why |
| --- | --- |
| `skills/REPOSITORY_DISCOVERY.md` | Read the live state of the repo on first contact |
| `skills/CHANGE_EXECUTION.md` | Branch discipline for the CLI work |
| `skills/VALIDATION_AND_CI.md` | Map the vitest + eslint + prettier + build pipeline |
| `skills/PR_CREATION.md` | Maintain the project's PR template |
| `skills/SECURITY_AND_TRUST.md` | Treat `package.json`, `dist/`, and fixtures as untrusted data |
| `skills/CONTEXT_CHECKPOINTS.md` | Long sessions, multiple PRs in a wave |

## Skills to load only when needed

| Skill | Trigger |
| --- | --- |
| `skills/ARCHITECTURE_ANALYSIS.md` | Adding or renaming a public command, flag, or output format |
| `skills/TASK_MODES.md` | Picking the right workflow for a bug, feature, refactor, CI, or maintenance task |

## Task starter to use first

`prompts/REPOSITORY_ONBOARDING.md`

This is the prompt that produces the first architecture map, captures
the validation pipeline, and lists the open risks.

## Common follow-ups

- Bug fix: `prompts/BUG_FIX.md`
- New command: `prompts/FEATURE_IMPLEMENTATION.md`
- Issue implementation: `prompts/ISSUE_TO_PR.md`
- Release prep: `prompts/DAILY_IMPROVEMENT.md`

## Validation mapping

| Repository check | Skill responsibility |
| --- | --- |
| `npm test` | `skills/VALIDATION_AND_CI.md` |
| `npm run lint` | `skills/VALIDATION_AND_CI.md` |
| `npm run typecheck` | `skills/VALIDATION_AND_CI.md` |
| `npm run build` | `skills/VALIDATION_AND_CI.md` |
| GitHub Actions | `skills/VALIDATION_AND_CI.md` |

## What to put in the Project's task brief

```text
Work exclusively on <owner>/<repo>.
Default branch is main. Node 20 LTS. TypeScript strict. npm.
Test runner: vitest. Linter: eslint. Formatter: prettier.
Release flow: changesets. Architecture: src/commands for CLI
subcommands, src/lib for shared logic.

For any change:
  - inspect the live repository and current PRs first
  - create a focused branch from a fresh main
  - add or update tests in tests/ alongside the change
  - run npm test, npm run lint, npm run typecheck, npm run build
  - use templates/PR_TEMPLATE.md for the PR body
  - do not merge your own PR
```

## Things to call out in the handoff

- The exact Node and npm versions used
- Whether `npm ci` was used (it should be)
- The actual vitest output, not a summary
- Any test that was skipped and why
- Any flag or env var the reviewer needs to reproduce the run
