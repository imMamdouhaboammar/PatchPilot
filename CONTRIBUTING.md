# Contributing to PatchPilot

PatchPilot is a documentation and prompt-engineering kit. Most contributions
are changes to Markdown, JSON, and small Python helper scripts. The project
follows its own PR-only operating contract: nothing reaches `main` without
a reviewed pull request, and the agent or maintainer who opens a PR is not
the one who merges it.

## Quick checklist

1. Open an issue first for any non-trivial change. Skill additions, scope
   changes to the system prompt, and CI changes all benefit from a short
   discussion before code lands.
2. Fork the repository and create a topic branch off `main`.
3. Match the existing tone: direct, evidence-based, no marketing language,
   no emoji in final copy.
4. Run `python3 scripts/validate_pack.py` locally before pushing.
5. Push the branch and open a pull request using the provided template.
6. Wait for an independent reviewer. Do not merge your own PR.

## What kinds of contributions are welcome

- New skills that fit the existing dispatcher model
- New task-starter prompts that follow the same template as the existing
  seven in `prompts/`
- Improvements to existing skills, prompts, or templates when backed by
  a concrete example of the problem they solve
- New stack-specific example presets under `examples/`
- Bug fixes for typos, broken links, formatting, or character-limit issues
- CI improvements that strengthen validation without adding flakiness
- Documentation that explains how to use the kit in real workflows

## What is not a good fit

- Additions that bloat the system prompt past the 8,000-character limit
- Brand new workflow paradigms that do not fit the PR-only model
- Heavy frameworks, build systems, or runtime dependencies
- Marketing copy, promotional sections, or emoji-driven formatting
- Auto-merge, auto-publish, or auto-release features
- Anything that weakens the trust and security rules in
  `skills/SECURITY_AND_TRUST.md`

## Style guide

The kit reads as a focused engineering handbook. Match that voice:

- Short paragraphs, short sentences
- Imperative mood for instructions
- Direct claims supported by evidence
- No emoji in the body of any file
- No em dash characters; use a regular hyphen or a colon
- Sentence-case headings inside the body, Title Case only for top-level
  document titles
- Code blocks fenced with the language tag (`bash`, `text`, `mermaid`)
- Internal links use repository-relative paths

## Validation

Before opening a pull request, run the local validation script:

```bash
python3 scripts/validate_pack.py
```

The script regenerates `VALIDATION_REPORT.md`, counts files, checks the
system prompt length, scans for forbidden em dash characters, and verifies
every internal link target exists. It exits non-zero on any failure.

The same script runs in CI on every push and pull request via
`.github/workflows/validate-pack.yml`. Pull requests that fail validation
cannot be merged.

## Adding a new skill

1. Decide which task types the skill covers. Read `SKILLS_INDEX.md` first.
2. Create the file under `skills/` with a YAML frontmatter block:

   ```yaml
   ---
   name: short-skill-name
   use_when: one or two sentences describing the trigger
   ---
   ```

3. Add the skill to the "Load by task" table in `SKILLS_INDEX.md`.
4. Add the file name to `MANIFEST.json`.
5. Run the validation script.

## Adding a new task-starter prompt

1. Create a Markdown file under `prompts/` with a clear, action-oriented
   title in the first heading.
2. Use the same skeleton as existing prompts: context, goal, what to
   inspect, what to produce, handoff expectations.
3. Add the file to `MANIFEST.json` and the README prompt table.
4. Run the validation script.

## Adding a new example

1. Create the file under `examples/` with a stack-specific slug.
2. Explain which skills the example turns on by default and which
   task-starter prompts to use first.
3. Add the file to `MANIFEST.json` and the README.

## Pull request review

Reviewers should:

- Check the diff against the style guide above
- Run the validation script
- Verify the system prompt character count remains under 8,000
- Confirm the change does not relax the trust or security rules
- Confirm internal links resolve
- Leave concrete suggestions instead of blanket approvals

Reviewers should not:

- Merge a PR they opened themselves
- Merge a PR that has failing CI
- Merge a PR that adds a dependency without justification
- Merge a PR whose description does not state what was verified

## Release process

1. Cut a release branch named `release/vX.Y.Z`
2. Update `MANIFEST.json`, `CHANGELOG.md`, and `VALIDATION_REPORT.md`
3. Run `python3 scripts/build_zip.py` to produce a clean release archive
4. Open a pull request titled `Release vX.Y.Z`
5. After merge, create a GitHub release from the merged commit and attach
   the zip produced in step 3

PatchPilot does not auto-publish releases and does not auto-tag commits.
The maintainer who prepares the release is not the one who approves it.
