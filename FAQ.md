# Frequently asked questions

## General

### What is PatchPilot?

PatchPilot is a documentation and prompt-engineering kit that turns a
ChatGPT Web Project into a focused pull-request creation layer. It
defines an operating contract, a skill dispatcher, a set of skills and
templates, and a small Python validation script. It is not a runtime,
not a daemon, and not a hosted service.

### Why PR-only?

PR-only separates the act of writing code from the act of merging it.
The same person or agent that opens a pull request is rarely the
person or agent with the right context, the right test environment,
and the right authority to merge it. Forcing the merge decision onto
a separate reviewer or maintainer catches mistakes that the author
cannot see.

### Does PatchPilot merge pull requests?

No. PatchPilot opens pull requests and hands them off. The merge
decision belongs to a separate coding agent or a human maintainer with
the full repository workspace and the authority to revert.

### Does PatchPilot auto-merge, auto-publish, or auto-tag?

No. Auto-merge, auto-publish, and auto-tag are explicitly out of scope
for the kit. The system prompt forbids them and the validation script
flags system prompts that try to claim them.

### Does PatchPilot work with Claude, Cursor, Aider, or other agents?

The system prompt is written for ChatGPT Web, but the kit's structure
(skills, templates, prompts, validation script) is agent-agnostic.
Other agents that read `AGENTS.md` and the dispatcher in
`SKILLS_INDEX.md` can use the same content. The `AGENTS.md` in this
repository follows the agents.md convention used by OpenCode, Codex,
Cursor, Aider, Devin, and Gemini CLI.

### Does PatchPilot work without ChatGPT?

Yes. The kit is plain Markdown, JSON, and Python. You can read the
skills and templates in any editor, follow the operating contract by
hand, and run `python3 scripts/validate_pack.py` against the kit
itself. The ChatGPT integration is one of several ways to apply the
kit.

## Setup

### How big is the system prompt?

`SYSTEM_PROMPT.txt` is intentionally under 8,000 characters, the
ChatGPT Project Instructions limit. The current size is published in
`MANIFEST.json` and checked by the validation script.

### Do I need to upload every file?

No. Upload `SKILLS_INDEX.md`, the files under `skills/`, and the files
under `templates/`. Upload only the prompts under `prompts/` that you
expect to use. Loading fewer files leaves more context budget for
your actual chat.

### Can I share one Project across multiple repositories?

No. One repository per Project. Architectural rules, branch names,
test commands, and terminology do not transfer between repositories.
Use the Project switcher to move between them.

### The GitHub connector does not let me scope to one repository. What now?

Use a GitHub App installation scoped to the repository, or work in a
fresh Project that has no other connections. Do not grant the
connector access to a personal account or an organisation that
contains unrelated repositories.

## Use

### The agent pushed to `main` even though I told it not to. What do I do?

The system prompt forbids it. If a connected agent or a third-party
tool still allowed the push, revert it, rotate any secrets that may
have been exposed, and tighten the connector scope. The agent
should have stopped before any push to a protected default branch.

### The agent claimed a test passed but did not show the output. What do I do?

Ask for the exact command and the full output. If the agent cannot
produce them, treat the claim as unverified and require the
independent reviewer to run the check before merge. The validation
truth rule in `skills/VALIDATION_AND_CI.md` exists to make this kind
of question easy to ask.

### The agent opened a pull request with a huge diff. What do I do?

Close the pull request and ask the agent to split it. The
`prompts/BACKLOG_TO_PRS.md` task starter is designed to break a large
request into a list of focused PRs. A PR that mixes bug fixes,
features, refactors, docs, and CI work is hard to review and hard to
revert.

### The agent used a dependency I do not want. What do I do?

Reject the PR and ask the agent to implement the change with the
existing repository utilities. New dependencies are allowed when the
benefit clearly exceeds the cost; the cost is part of the PR
description.

## Development

### How do I add a new skill?

Read `CONTRIBUTING.md`. The short version:

1. Create the file under `skills/` with a YAML frontmatter block
2. Add the skill to the "Load by task" table in `SKILLS_INDEX.md`
3. Add the file name to `MANIFEST.json`
4. Run `python3 scripts/validate_pack.py`

### How do I regenerate the validation report?

```bash
python3 scripts/validate_pack.py
```

The script writes `VALIDATION_REPORT.md` in the repository root. CI
runs the same script with `--check` and fails the build on any
validation error.

### How do I produce a release zip?

```bash
python3 scripts/build_zip.py --output dist/patchpilot-vX.Y.Z.zip
```

The script excludes `.git`, `__pycache__`, macOS metadata, editor
backups, virtualenvs, and build outputs. Use the produced zip as the
asset attached to a GitHub release.

### Where do I report a security issue in the kit?

Follow the channel in `SECURITY.md`. Open a private security
advisory rather than a public issue. The contact address is also
listed there.
