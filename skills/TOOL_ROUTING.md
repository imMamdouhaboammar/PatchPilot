---
name: tool-routing
use_when: choosing GitHub, web, sandbox, Project files, or batching strategy
---
# Tool Routing

## GitHub tools
Use for live repository facts and repository actions: metadata, permissions, branches, commits, code search, exact file reads, issues, PRs, checks, comments, branch creation, commits, and PR creation.

Refresh live state before every branch creation, push, or PR update. Do not rely on an earlier chat summary when the repository may have moved.

## Sandbox and Python
Use for isolated logic where the runtime language is not essential: regex, parsers, data transformations, ranking, JSON manipulation, archive inspection, and artifact generation.

A Python recreation does not verify TypeScript, JavaScript, Go, Rust, React, database, framework, build, or integration behavior. Label it as a logic experiment.

## Web research
Use when correctness depends on current external facts, including framework APIs, dependency behavior, supported versions, CVEs, standards, or vendor documentation. Prefer official docs, specifications, release notes, and primary sources.

## Project files
Use as persistent process guidance and templates. Search them by task rather than loading the entire pack.

## Batching
Batch independent read-only calls. Examples: repository metadata, several file reads, issue search, PR search, and recent commits.

Sequence operations that depend on earlier output or can conflict: edits, commits, branch updates, commands, rebases, and PR writes.

## Failure behavior
If a tool is missing, blocked, or returns incomplete data, state the limitation. Use the safest available route. Never invent tool output or validation evidence.
