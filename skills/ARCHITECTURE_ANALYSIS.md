---
name: architecture-analysis
use_when: changing modules, routes, schemas, global state, public interfaces, dependencies, or architecture documentation
---
# Architecture Analysis

## Existing truth first
Read repository governance, current architecture docs, dependency rules, source layout, and tests. Verify architecture documents against the code before relying on them.

## Reuse before creation
Search existing symbols, services, components, validators, utilities, hooks, stores, schemas, and routes. Prefer extending an established boundary over introducing a second implementation.

## Change assessment
Identify affected modules, consumers, state, data flow, persistence, APIs, error paths, tests, build output, and compatibility. For complex flows, provide a Mermaid diagram before coding when explanation is needed.

## Architecture map
If `ARCHITECTURE_MAP.md` exists, use it as an index. Update it only for material changes. If absent, create it only when no equivalent exists and the repository will gain lasting value. Use `templates/ARCHITECTURE_MAP_TEMPLATE.md` and keep it lightweight.

## Guardrails
Do not perform a broad rewrite merely to improve theoretical structure. Use behavior-preserving, test-backed slices. Keep placeholder directories unwired unless the change fully connects runtime, build, tests, packaging, and docs.

## PR disclosure
State whether architecture, global state, schema, routes, dependencies, or public APIs changed. Provide migration and independent verification steps where relevant.
