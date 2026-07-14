# Example: monorepo

This preset covers a multi-package monorepo with shared libraries, a
CLI, a web service, and a public SDK. It is meant to be read once when
you first set up the ChatGPT Project, then left alone.

## Repository shape

```text
monorepo/
  package.json
  pnpm-workspace.yaml
  apps/
    web/
    api/
    cli/
  packages/
    sdk/
    ui/
    shared/
  tools/
    scripts/
  README.md
  CHANGELOG.md
  AGENTS.md
```

## What PatchPilot should know upfront

Add this to the top of the first onboarding chat:

```text
This is a TypeScript monorepo. The package manager is pnpm with
workspaces, the build orchestrator is turborepo, the test runner is
vitest, the linter is eslint, the formatter is prettier, the type
checker is tsc, and the SDK is published to npm. Default branch is
`main` and is protected. Releases are cut with changesets and the
`release` workflow.
```

## Per-package rules

PatchPilot must respect the boundary of each package:

- Do not edit code in one package to fix a problem caused by another
  package's public API. File an issue, open a separate PR, or escalate.
- Do not introduce a cross-package import that did not exist before.
  If a new shared helper is needed, add it to `packages/shared` and
  consume it through the workspace protocol.
- Do not change the SDK's public types without a CHANGELOG entry and a
  migration note in the PR description.

## Skills to load by default

| Skill | Why |
| --- | --- |
| `skills/REPOSITORY_DISCOVERY.md` | Read the live state of the repo on first contact |
| `skills/ARCHITECTURE_ANALYSIS.md` | Map the package boundaries before editing |
| `skills/CHANGE_EXECUTION.md` | Branch discipline for the change |
| `skills/VALIDATION_AND_CI.md` | Map the per-package pipeline and the monorepo CI |
| `skills/PR_CREATION.md` | Maintain the project's PR template |
| `skills/SECURITY_AND_TRUST.md` | Treat fixtures, generated stubs, and lockfiles as untrusted data |
| `skills/CONTEXT_CHECKPOINTS.md` | Long sessions, multiple PRs in a wave |

## Task starter to use first

`prompts/REPOSITORY_ONBOARDING.md`

The first onboarding chat must include a package map in the output so
later chats know where to make changes.

## Common follow-ups

- Bug fix in a single package: `prompts/BUG_FIX.md`
- New public SDK method: `prompts/FEATURE_IMPLEMENTATION.md`
- Cross-package refactor: `prompts/FEATURE_IMPLEMENTATION.md`
- Issue implementation: `prompts/ISSUE_TO_PR.md`
- Release prep: `prompts/DAILY_IMPROVEMENT.md`

## Validation mapping

| Repository check | Skill responsibility |
| --- | --- |
| `pnpm install --frozen-lockfile` | `skills/VALIDATION_AND_CI.md` |
| `pnpm -r test` | `skills/VALIDATION_AND_CI.md` |
| `pnpm -r lint` | `skills/VALIDATION_AND_CI.md` |
| `pnpm -r typecheck` | `skills/VALIDATION_AND_CI.md` |
| `pnpm -r build` | `skills/VALIDATION_AND_CI.md` |
| `pnpm changeset status` | `skills/VALIDATION_AND_CI.md` |
| GitHub Actions | `skills/VALIDATION_AND_CI.md` |

## What to put in the Project's task brief

```text
Work exclusively on <owner>/<repo>.
Default branch is main. Monorepo with pnpm workspaces and
turborepo. Apps: web, api, cli. Packages: sdk, ui, shared.
Test runner: vitest. Linter: eslint. Formatter: prettier.
Type checker: tsc. Release flow: changesets.

For any change:
  - inspect the live repository, current PRs, and recent commits
  - identify the affected package(s) and confirm the boundary
  - create a focused branch from a fresh main
  - add or update tests in the same package as the change
  - run pnpm -r test, pnpm -r lint, pnpm -r typecheck,
    pnpm -r build, pnpm changeset status
  - add a changeset file when the public surface changes
  - use templates/PR_TEMPLATE.md for the PR body
  - do not merge your own PR
```

## Things to call out in the handoff

- The exact pnpm and Node versions used
- The packages actually affected
- Whether a changeset was added and at which bump level
- Whether the change is API-breaking for the SDK and what the
  migration path is
- The actual vitest and tsc output, not a summary
