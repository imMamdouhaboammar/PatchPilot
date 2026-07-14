#!/usr/bin/env python3
"""
build_zip.py
============

Produces a clean PatchPilot release zip without macOS metadata, editor
backups, the .git directory, or the build artefacts listed in .gitignore.

Usage:
  python3 scripts/build_zip.py
  python3 scripts/build_zip.py --output dist/patchpilot.zip
  python3 scripts/build_zip.py --root /path/to/repo
"""

from __future__ import annotations

import argparse
import os
import sys
import zipfile
from pathlib import Path
from typing import Iterable

EXCLUDE_DIRS = {
    ".git",
    ".github/.cache",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".DS_Store",
}

EXCLUDE_FILE_PATTERNS = (
    ".DS_Store",
    ".gitkeep",
    "Thumbs.db",
    "*.swp",
    "*.swo",
    "*.bak",
    "*.orig",
    "*.tmp",
    "*.pyc",
    "*.pyo",
)


def iter_release_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        rel_parts = rel.parts
        if any(part in EXCLUDE_DIRS for part in rel_parts):
            continue
        if any(part.startswith("__pycache__") for part in rel_parts):
            continue
        if rel.name in EXCLUDE_DIRS:
            continue
        if any(rel.name.endswith(pat.lstrip("*")) for pat in EXCLUDE_FILE_PATTERNS):
            continue
        yield path


def build_zip(root: Path, output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    count = 0
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in iter_release_files(root):
            arcname = path.relative_to(root).as_posix()
            zf.write(path, arcname)
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root (default: parent of this script)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="output zip path (default: <root>/patchpilot.zip)",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    if not (root / "MANIFEST.json").exists():
        print(f"error: {root} does not look like a PatchPilot repository", file=sys.stderr)
        return 1

    output = args.output or (root / "patchpilot.zip")
    count = build_zip(root, output)
    size = output.stat().st_size
    print(f"Wrote {count} files to {output} ({size:,} bytes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
