# Examples

Stack-specific Project presets for PatchPilot. Each example shows the
repository shape, the skill roster, the validation pipeline, and the
task brief that should be used the first time a ChatGPT Project is set
up for a repository of that kind.

The examples are starting points, not contracts. Treat them as the
default wiring and adjust to match the actual repository.

## Available presets

- [Node.js CLI](./node-cli.md) - TypeScript CLI with vitest, eslint,
  prettier, and changesets
- [Python library](./python-lib.md) - Public package on PyPI with
  pytest, ruff, mypy, and python-semantic-release
- [Monorepo](./monorepo.md) - TypeScript monorepo with pnpm
  workspaces, turborepo, and changesets

## Adding a new preset

1. Create a new Markdown file in this directory.
2. Follow the same skeleton: repository shape, runtime and tooling
   summary, default skills, optional skills, task starter, common
   follow-ups, validation mapping, recommended task brief, and
   handoff checklist.
3. Add the file to `MANIFEST.json` and the README examples table.
4. Run `python3 scripts/validate_pack.py`.

A preset should fit on a few screens. If it would be longer, link out
to a deeper guide in `docs/` instead.
