---
name: change-execution
use_when: creating branches, editing files, committing changes, or handling remote drift
---
# Change Execution

## Branch safety
Refresh the default branch immediately before branching. Record its SHA. Use a descriptive branch such as `fix/auth-null-session`, `feat/creator-language-filter`, or `test/mcp-invalid-request`.

Never write to the default branch. Never force-push or rewrite published history.

## Editing discipline
- Make the smallest complete change.
- Read exact target content and enough surrounding context first.
- Inspect direct callers, imports, types, tests, and configuration.
- Match existing style and framework patterns.
- Prefer targeted edits over full-file replacement.
- Do not mix unrelated formatting or refactors.
- Remove debug output, temporary files, dead code, and unused imports.
- Do not hand-edit generated output when a repository command owns it.

## Compatibility
Preserve public APIs and persistent data formats where practical. Breaking changes require explicit approval, migration guidance, tests, and PR disclosure.

## Dependencies
Prefer existing repository utilities and standard-library features. Add a dependency only when its benefit exceeds maintenance, package, compatibility, and security costs.

## Atomic commits
Each commit represents one coherent reviewer decision. Include tests with the behavior they protect when practical. Use Conventional Commits. Do not manufacture commit boundaries.

## Remote drift
Refresh the target branch before pushing. If it moved, inspect the new commits and update safely. Do not overwrite valid work. Report conflicts or stale assumptions.
