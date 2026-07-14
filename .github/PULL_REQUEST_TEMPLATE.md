<!--
This template mirrors templates/PR_TEMPLATE.md in the kit.
Agents and maintainers should fill in every section.
Plain text only. No emoji. No em dash characters.
-->

## Objective

<!-- One paragraph: what does this PR change and why. -->

## Confirmed problem and evidence

<!-- What did you observe? Link the issue, the CI run, the failing
command output, or the user report. If there is no concrete evidence,
say so explicitly. -->

## File-level changes

<!-- Bulleted list of the files touched and what each one does. -->

- `path/to/file`: short description
- `path/to/other`: short description

## Architecture, state, schema, and API impact

<!-- Does this change how skills, prompts, templates, or examples are
loaded? Does it add or rename a file referenced from SKILLS_INDEX.md,
MANIFEST.json, or any other index? Does it change the JSON schema of
MANIFEST.json? -->

## Verification

<!-- Exact commands you ran and their actual output. Do not paste
imagined output. If a check was not run, say so. -->

Commands run:

```text
python3 scripts/validate_pack.py
```

Results:

```text
<!-- paste actual output -->
```

CI status:

<!-- Link the GitHub Actions run. -->

## Unavailable checks and reasons

<!-- List any check that you could not run and explain why. Examples:
no Python runtime locally, no Node toolchain, no permission to push
to a test registry. -->

## Potential risks and side effects

<!-- What could break? What should a reviewer double-check? -->

## Independent verification checklist

<!-- Exact steps a reviewer can run to verify the change. -->

- [ ] `python3 scripts/validate_pack.py` exits 0
- [ ] `MANIFEST.json` lists every added file
- [ ] `SKILLS_INDEX.md` lists every added skill
- [ ] `VALIDATION_REPORT.md` was regenerated
- [ ] Internal links resolve
- [ ] No new dependency without justification
- [ ] No relaxation of `skills/SECURITY_AND_TRUST.md`

## Included commits

<!-- Conventional Commits list. -->

- `type(scope): short summary`

## Handoff

<!-- Required: explicit statement that this PR is handed off for
review and that the author will not merge it. -->

This PR is handed off for independent review. The author will not merge
it and will not enable auto-merge. A separate maintainer is responsible
for the merge decision.
