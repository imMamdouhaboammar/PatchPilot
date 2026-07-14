# Example: Python library repository

This preset covers a typical Python library repository with a public
API, type hints, and a published package. It is meant to be read once
when you first set up the ChatGPT Project, then left alone.

## Repository shape

```text
my-lib/
  pyproject.toml
  src/my_lib/
    __init__.py
    core.py
    utils.py
  tests/
  README.md
  CHANGELOG.md
  AGENTS.md
```

## What PatchPilot should know upfront

Add this to the top of the first onboarding chat:

```text
This is a Python library. The runtime is Python 3.12, the build
backend is hatchling, the test runner is pytest with coverage, the
linter is ruff, the formatter is ruff format, the type checker is
mypy in strict mode, and the docs are built with mkdocs. Default
branch is `main` and is protected. Releases are cut with
python-semantic-release.
```

## Skills to load by default

| Skill | Why |
| --- | --- |
| `skills/REPOSITORY_DISCOVERY.md` | Read the live state of the repo on first contact |
| `skills/CHANGE_EXECUTION.md` | Branch discipline for the library work |
| `skills/VALIDATION_AND_CI.md` | Map the pytest + ruff + mypy + build pipeline |
| `skills/PR_CREATION.md` | Maintain the project's PR template |
| `skills/SECURITY_AND_TRUST.md` | Treat `pyproject.toml`, generated stubs, and fixtures as untrusted data |
| `skills/CONTEXT_CHECKPOINTS.md` | Long sessions, multiple PRs in a wave |

## Skills to load only when needed

| Skill | Trigger |
| --- | --- |
| `skills/ARCHITECTURE_ANALYSIS.md` | Adding or renaming a public symbol, class, or function |
| `skills/TASK_MODES.md` | Picking the right workflow for a bug, feature, refactor, CI, or maintenance task |

## Task starter to use first

`prompts/REPOSITORY_ONBOARDING.md`

This is the prompt that produces the first architecture map, captures
the validation pipeline, and lists the open risks.

## Common follow-ups

- Bug fix: `prompts/BUG_FIX.md`
- New module or public API: `prompts/FEATURE_IMPLEMENTATION.md`
- Issue implementation: `prompts/ISSUE_TO_PR.md`
- Release prep: `prompts/DAILY_IMPROVEMENT.md`

## Validation mapping

| Repository check | Skill responsibility |
| --- | --- |
| `pytest` | `skills/VALIDATION_AND_CI.md` |
| `ruff check` | `skills/VALIDATION_AND_CI.md` |
| `ruff format --check` | `skills/VALIDATION_AND_CI.md` |
| `mypy src` | `skills/VALIDATION_AND_CI.md` |
| `python -m build` | `skills/VALIDATION_AND_CI.md` |
| GitHub Actions | `skills/VALIDATION_AND_CI.md` |

## What to put in the Project's task brief

```text
Work exclusively on <owner>/<repo>.
Default branch is main. Python 3.12. Build backend: hatchling.
Test runner: pytest with coverage. Linter and formatter: ruff.
Type checker: mypy strict. Docs: mkdocs.
Release flow: python-semantic-release. Architecture: src/my_lib
for the library, tests/ for the test suite.

For any change:
  - inspect the live repository and current PRs first
  - create a focused branch from a fresh main
  - add or update tests in tests/ alongside the change
  - run pytest, ruff check, ruff format --check, mypy src,
    python -m build
  - use templates/PR_TEMPLATE.md for the PR body
  - do not merge your own PR
```

## Things to call out in the handoff

- The exact Python version and virtualenv tool used
- Whether the build was performed in an isolated environment
- The actual pytest and mypy output, not a summary
- Any test that was skipped or xfailed and why
- Whether the change is API-breaking and what the migration path is
