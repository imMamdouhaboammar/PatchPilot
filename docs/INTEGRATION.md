# Integration guide

This guide explains how to set up a PatchPilot ChatGPT Project from
scratch, how to wire it to a GitHub repository, and how to run the
first few chats. It is meant for first-time users of the kit.

## 1. Create one Project per repository

A ChatGPT Project keeps a single set of instructions, a single set of
uploaded knowledge files, and a single connected repository. Do not
mix repositories in one Project.

Recommended naming:

```text
PatchPilot | owner/repository
```

Examples:

- `PatchPilot | acme/web`
- `PatchPilot | acme/api`
- `PatchPilot | acme/sdk`

The name shows up in the Project switcher and in the title of every
chat, which makes it easy to tell contexts apart.

## 2. Add the system prompt

Copy the entire contents of `SYSTEM_PROMPT.txt` into the Project's
Instructions field. The prompt is under 8,000 characters so it fits
the ChatGPT limit.

If the project instructions field is hidden behind customisation, open
the Project, click the project name, choose "Customise" or the gear
icon, and paste the prompt into the Instructions field.

The prompt carries the non-negotiable rules:

- PR-only operation
- No default-branch writes
- No merge authority
- Live repository inspection before any edit
- Validation truth
- Context discipline
- Security boundaries
- Atomic commit rules
- Independent handoff

The remaining files explain how to apply those rules in concrete
situations.

## 3. Upload the knowledge files

Upload the following files to the Project's knowledge section:

Required:

- `SKILLS_INDEX.md`
- `skills/*.md`
- `templates/*.md`

Optional, upload only the workflows you expect to use:

- `prompts/*.md`

Loading the optional files costs context budget. If you only work on
bugs, you do not need the `prompts/BACKLOG_TO_PRS.md` prompt in
context.

## 4. Connect GitHub

Open the Project's Connectors or Apps panel and connect only the
repository this Project is for. Do not grant access to a personal
account or an organisation that contains unrelated repositories.

Enable write confirmations when the option is available. PatchPilot
creates branches, commits, and pull requests; you should be asked to
approve each write.

Required connector capabilities:

- Read repository code, issues, pull requests, and checks
- Create branches
- Create commits
- Create pull requests
- Read CI results

Capabilities PatchPilot should never need:

- Merge pull requests
- Enable auto-merge
- Push directly to a protected default branch
- Publish packages
- Create releases or tags
- Delete branches
- Bypass branch protection

If the connector cannot scope to a single repository, prefer to use a
GitHub App installation scoped to that repository, or work in a fresh
Project that has no other connections.

## 5. Start with onboarding

The first chat in a Project should use
`prompts/REPOSITORY_ONBOARDING.md`. The output is a structured picture
of the repository:

- Owner, visibility, default branch, current head
- Repository instructions
- Primary language, package manager, runtime
- Test, build, lint, type-check, format, and migration commands
- Recent commits, open issues, active PRs, CI state
- Architecture map (only when the task materially changes it)
- Open risks and backlog relevance

Save the output as a checkpoint using
`templates/SESSION_CHECKPOINT.md`. Subsequent chats in the same
Project can read the checkpoint instead of re-discovering the
repository from scratch.

## 6. Assign a focused task

After onboarding, give the Project a single, bounded task. Examples:

```text
Implement the highest-value safe improvement in input validation.
Create a dedicated branch, add regression coverage, run every
available check, and open a documented pull request. Do not merge
it.
```

```text
Fix issue #142. The bug is in the rate limiter and is reproduced
with the failing test in tests/test_rate_limit.py. Create a
dedicated branch, fix the bug, extend the regression test, run
every available check, and open a documented pull request. Do
not merge it.
```

The size of the task is up to you. A larger request should produce
several focused PRs, not one giant PR. The `prompts/DAILY_IMPROVEMENT.md`
and `prompts/BACKLOG_TO_PRS.md` task starters are designed to break a
big ask into a list of small PRs.

## 7. Review the handoff

When the agent opens a pull request, the PR body follows
`templates/PR_TEMPLATE.md`. Read every section:

- Objective
- Confirmed problem and evidence
- File-level changes
- Architecture, state, schema, and API impact
- Exact verification commands and results
- CI status
- Unavailable checks and reasons
- Potential risks and side effects
- Independent verification checklist
- Included commits
- Handoff note

If the agent claims a check passed but does not show the command and
the output, ask for it. If the agent says a check was not run, do not
merge until a separate reviewer runs it.

## 8. Hand off the merge

PatchPilot is a PR creation layer, not a merge authority. The merge
decision belongs to a separate coding agent or a human maintainer who
has the full repository workspace, the full test environment, and the
authority to revert if something goes wrong.

When the merge is yours:

- Confirm the CI run on the PR branch is green
- Run the project's full local validation suite
- Re-read the diff and the PR description
- Merge using the project's standard merge strategy
- Delete the source branch if the project policy allows it

## 9. Continue in a new chat

Long sessions fail when the agent forgets repository state. Before
moving to a new chat, fill in `templates/SESSION_CHECKPOINT.md` with:

- Repository, branch, starting SHA, current SHA
- Active task and what is left
- Decisions made and untouched scope
- Inspected paths
- Commits created
- Validation evidence
- Open risks
- Next action

The next chat in the same Project can read the checkpoint to resume
without re-discovering the repository.

## 10. Tune the kit

If the system prompt is too rigid or too lenient for a specific
repository, do not edit it. Adjust the Project's task brief or add a
stack-specific preset under `examples/`. The system prompt is a fixed
contract; the per-repository tuning happens above it.
