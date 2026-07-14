# AGENTS.md

This file is the operating contract for any AI agent or human maintainer
working on the PatchPilot repository. It applies to ChatGPT, Claude, Codex,
Copilot, Cursor, Aider, Gemini CLI, and any other agent that reads
`AGENTS.md` per the [agents.md](https://agents.md/) convention.

PatchPilot is a documentation and prompt-engineering kit. There is no
application code, no runtime, and no shipped binary. Every contribution is
a Markdown, JSON, or small Python helper-script change. Despite that, the
project follows strict engineering discipline because the kit itself teaches
that discipline.

## Operating mode

PR-only. No agent or maintainer writes directly to `main`. Every change
goes through a dedicated branch, an atomic commit set, a documented pull
request, and an independent review.

## Authority order

1. Explicit user instructions
2. `AGENTS.md` (this file) and the kit's own `SYSTEM_PROMPT.txt`
3. Repository governance files (`README.md`, `CONTRIBUTING.md`,
   `SECURITY.md`, `CODE_OF_CONDUCT.md`)
4. Current Markdown, JSON, and Python source in the repository
5. The validation report and CI output
6. Backlog items, future-ideas lists, and roadmaps
7. General assumptions

## Repository layout

```text
patchpilot/
  AGENTS.md                 # this file
  README.md                 # human-facing project description
  CHANGELOG.md              # version history
  CONTRIBUTING.md           # how to contribute
  CODE_OF_CONDUCT.md        # community standards
  SECURITY.md               # security reporting channel
  LICENSE                   # MIT license
  MANIFEST.json             # machine-readable file inventory
  VALIDATION_REPORT.md      # output of scripts/validate_pack.py
  SYSTEM_PROMPT.txt         # the kit's main system prompt
  SKILLS_INDEX.md           # dispatcher for the skills
  skills/                   # 9 Markdown skills
  templates/                # 5 Markdown templates
  prompts/                  # 7 Markdown task starters
  examples/                 # stack-specific Project presets
  docs/                     # deep-dive guides
  scripts/                  # validate_pack.py and build_zip.py
  .github/                  # issue templates, PR template, CI
```

## File budgets

- `SYSTEM_PROMPT.txt` must stay below 8,000 characters (ChatGPT Project
  Instructions limit). Add to skills, not to the prompt, when something
  does not fit.
- Each skill file is kept short on purpose. If a skill grows beyond what
  fits in a single focused read, split it.
- The system prompt, every skill, and every template must avoid em dash
  characters. Use a regular hyphen or a colon.
- Internal links must use repository-relative paths and resolve to real
  files.

## Build and validation

There is no application to build. There is one validation script and one
release helper:

```bash
# Regenerate VALIDATION_REPORT.md and check the pack
python3 scripts/validate_pack.py

# Produce a clean release zip (used by maintainers, not by CI)
python3 scripts/build_zip.py
```

CI runs `validate_pack.py` on every push and pull request. PRs that fail
validation cannot be merged.

## Task flow for an agent working on this repository

1. Read this file first. Then read `README.md`, `CONTRIBUTING.md`, and
   the relevant skill under `skills/`.
2. Inspect the current `main` branch and any open pull requests that
   touch the same area. Do not duplicate work.
3. Classify the change: skill, prompt, template, example, docs, CI,
   infrastructure, or release. Open or claim an issue describing the
   problem and the intended change.
4. Branch from a fresh `main`. Use a descriptive name:
   `skill/...`, `prompt/...`, `example/...`, `docs/...`, `ci/...`.
5. Make the smallest complete change. Match existing style. Do not
   refactor unrelated files. Do not edit generated output by hand.
6. Run the validation script. Fix anything it reports.
7. Commit atomically using Conventional Commits. Do not manufacture
   commit boundaries.
8. Push the branch and open a pull request using
   `.github/PULL_REQUEST_TEMPLATE.md`. Fill in the evidence, the
   unverified areas, the risks, and the independent verification
   steps.
9. Wait for a reviewer. Do not merge your own pull request.

## What is forbidden

- Force-push, history rewrite, or bypass of branch protection
- Auto-merge, auto-publish, auto-release, or auto-tag
- Adding dependencies without justification
- Weakening the trust or security rules in `skills/SECURITY_AND_TRUST.md`
- Pasting full files into a chat or pull request description when only
  a targeted diff is requested
- Skipping the validation script on a pull request
- Claiming a check passed when it was not actually executed
- Closing an issue without verified acceptance criteria

## Release flow for maintainers

1. Cut a `release/vX.Y.Z` branch
2. Update `MANIFEST.json`, `CHANGELOG.md`, and `VALIDATION_REPORT.md`
3. Run `python3 scripts/build_zip.py` to produce a clean archive
4. Open a pull request titled `Release vX.Y.Z`
5. After independent review and merge, create a GitHub release from the
   merged commit and attach the zip from step 3
