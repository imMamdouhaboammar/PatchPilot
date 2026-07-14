---
name: task-modes
use_when: classifying and planning bug fixes, features, refactors, docs, CI work, maintenance, or PR repair
---
# Task Modes

## Bug fix
Confirm the failure from code, tests, logs, issue evidence, or a reproducible case. Add a regression test when possible. Fix the root cause, not only the visible symptom. Keep unrelated cleanup out.

## Feature
Define acceptance criteria and the complete user or developer path. Find similar repository patterns first. Deliver a usable vertical slice with types, validation, errors, tests, docs, and wiring. Do not create inactive UI, fake data, or unconnected endpoints.

## Refactor
Preserve behavior. Establish test coverage before structural edits. Keep public interfaces stable unless explicitly approved. Split only along real responsibility boundaries.

## Test improvement
Target behavior and regressions rather than implementation details. Avoid snapshots that hide important changes. Do not weaken existing assertions.

## Documentation
Verify every command, path, option, version, and claim against current code. Documentation-only PRs still require link and example checks when available.

## CI or packaging
Reproduce the failing command or inspect the exact workflow. Keep local scripts and CI commands aligned. Check supported runtime matrices and package contents.

## PR repair
Read the entire PR scope, changed files, review comments, checks, base movement, and related issues. Fix only blockers and regressions inside the PR theme. Do not merge.

## Daily improvement
Audit first, then form a candidate list ranked by evidence, value, risk, effort, and testability. Create separate PRs for separate themes. Commit targets are cumulative. Stop rather than create filler.

## Clarification gate
Ask only when a missing answer changes architecture, persistent data, public API, destructive behavior, production target, security boundary, or acceptance criteria. Otherwise inspect and proceed.
