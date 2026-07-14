# scripts/

Helper Python scripts for working with the PatchPilot kit.

## `validate_pack.py`

```bash
# Regenerate VALIDATION_REPORT.md
python3 scripts/validate_pack.py

# CI mode: print report, exit non-zero on failure
python3 scripts/validate_pack.py --check
```

Checks:

- Every file declared in `MANIFEST.json` exists on disk
- `SYSTEM_PROMPT.txt` is at most 8,000 characters
- No Markdown file under the kit contains the em dash character
  outside of fenced code blocks
- Every repository-relative Markdown link resolves to a real file
- The required directories (`skills`, `templates`, `prompts`,
  `examples`, `docs`, `scripts`, `.github`) all exist
- The system prompt does not claim merge authority, does not
  instruct the agent to push to a default branch, and does not
  contain fabricated validation phrases

## `build_zip.py`

```bash
# Default: writes patchpilot.zip into the repository root
python3 scripts/build_zip.py

# Custom destination
python3 scripts/build_zip.py --output dist/patchpilot-v1.1.0.zip
```

Produces a clean release archive without:

- `.git` directory contents
- `__pycache__` and `*.pyc`
- macOS metadata (`.DS_Store`, `.AppleDouble`)
- Editor backups (`*.swp`, `*.swo`, `*.bak`)
- `node_modules`, virtualenvs, build outputs

Use this to attach a clean zip to a GitHub release. The build is
deliberately separate from CI; the validation workflow only checks the
kit, not the archive.

## Requirements

- Python 3.9 or newer
- No third-party dependencies
