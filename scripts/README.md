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

## `build_social_preview.py`

```bash
python3 scripts/build_social_preview.py
```

Regenerates the 1280x640 GitHub social preview image at
`.github/social-preview.png`. The image uses a dark navy background
with the brand mark, a one-line subtitle, a workflow pill, and a
small pull-request diagram on the right.

GitHub does not expose the social preview upload via the REST API, so
the file is committed to the repo and uploaded manually from
`Settings -> General -> Social preview`. Re-running the script
overwrites the file in place.

The script depends only on Pillow. It hardcodes paths to
`/System/Library/Fonts/Helvetica.ttc`; on Linux or Windows you should
swap the font path in the script or set the `PIL` font search path.

## Requirements

- Python 3.9 or newer
- Pillow (only for `build_social_preview.py`)
- No third-party dependencies for the other scripts
