---
name: validation-and-ci
use_when: testing changes, using the sandbox, interpreting GitHub Actions, or repairing CI
---
# Validation and CI

## Evidence levels
1. Repository command executed successfully in a suitable environment
2. GitHub Actions check passed for the branch SHA
3. Focused static review or isolated sandbox experiment
4. Not verified

Never present levels 3 or 4 as a passing repository test.

## Select checks from the repository
Use manifest scripts, contributor docs, workflow files, and existing test conventions. Relevant checks may include unit, integration, end-to-end, build, lint, type-check, formatting, schema, migration, architecture, package dry-run, and security scans.

## Sandbox boundary
Use Python or a generic sandbox for pure logic and deterministic input/output examples. Do not claim it renders a React UI, starts the real service, connects to production data, or proves another language runtime.

## GitHub Actions
Push a safe branch to trigger CI when appropriate. Inspect checks for the exact branch SHA. If CI is pending, say pending. If no workflow run exists, say unavailable. Fix regressions caused by the branch when possible.

## Prohibited shortcuts
Do not disable checks, remove failing tests, reduce assertions, add broad ignores, suppress type errors, hide warnings, or edit expected outputs merely to obtain green status.

## PR evidence
List every command exactly, its result, relevant counts, warnings, and unavailable checks with reasons. Include the independent reviewer steps needed for full validation.
