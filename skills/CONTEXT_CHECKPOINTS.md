---
name: context-checkpoints
use_when: the chat is long, work spans many commits or PRs, or a task moves to a new chat
---
# Context Checkpoints

## Purpose
A checkpoint is compact working memory, not a replacement for live repository inspection.

## Create one when
- a PR is opened
- a development wave is completed
- the default branch moves materially
- the task is paused or blocked
- the chat is becoming crowded
- work will continue in a new chat

## Required fields
Use `templates/SESSION_CHECKPOINT.md` and record repository, default branch, starting and current SHAs, working branch, task scope, decisions, inspected paths, commits, PRs, checks, failures, risks, and exact next action.

## Conservation rules
Do not paste full diffs or files. Store paths, symbols, summaries, and evidence. On resume, refresh GitHub state before trusting the checkpoint.

## Multiple PR programs
Maintain a short ledger: PR, theme, branch, base SHA, commit count, CI state, reviewer priority, and overlap with other PRs. Avoid parallel PRs editing the same core files unless coordinated.
