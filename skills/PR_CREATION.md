---
name: pr-creation
use_when: preparing, opening, updating, or handing off a pull request
---
# Pull Request Creation

## Scope
One PR should represent one coherent theme. Separate unrelated bugs, features, refactors, docs, and infrastructure work.

## Before opening
- refresh the target branch and inspect drift
- review the complete diff and commit list
- remove debug artifacts and unrelated changes
- confirm no secret values are present
- run available validation
- verify docs and tests match behavior
- confirm the branch does not target or modify the default branch directly

## Body
Use `templates/PR_TEMPLATE.md` exactly. Include evidence, precise file-level changes, architecture and state impact, commands and results, CI state, risks, commit list, and independent verification steps.

## After opening
Inspect checks. Repair branch-caused regressions when possible. Do not merge, enable auto-merge, close verified issues automatically, publish, release, or tag.

## Final chat handoff
State PR link, branch, commit count, validation status, CI status, and important risks. Keep it concise, but never omit a failed or unavailable check.
