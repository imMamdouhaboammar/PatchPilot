#!/usr/bin/env python3
"""
validate_pack.py
================

Validates the PatchPilot kit.

Checks performed:
  1. Every file listed in MANIFEST.json exists on disk.
  2. SYSTEM_PROMPT.txt is at most 8000 characters.
  3. No Markdown file under the kit contains the em dash character
     (U+2014) outside of code blocks.
  4. Every repository-relative Markdown link in the kit resolves to a
     real file.
  5. The kit contains the expected directories (skills, templates,
     prompts, examples, docs, scripts, .github).
  6. The system prompt does not claim merge authority, does not
     instruct the agent to push to a default branch, and does not
     contain fabricated validation language.

When run without flags, the script regenerates VALIDATION_REPORT.md
in the repository root. When run with --check, it prints the report to
stdout, does not write to disk, and exits non-zero on any failure.

Usage:
  python3 scripts/validate_pack.py          # regenerate report
  python3 scripts/validate_pack.py --check  # CI mode
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "MANIFEST.json"
SYSTEM_PROMPT_PATH = REPO_ROOT / "SYSTEM_PROMPT.txt"
REPORT_PATH = REPO_ROOT / "VALIDATION_REPORT.md"

MAX_PROMPT_CHARS = 8000
EM_DASH = "\u2014"

# Phrases that must never appear as POSITIVE claims in the system
# prompt. Negated occurrences ("you never merge", "do not enable
# auto-merge") are allowed because they reinforce the contract. The
# check below splits the prompt into sentences and inspects each
# sentence for a positive assertion.
FORBIDDEN_PROMPT_PHRASES = [
    ("merge authority", "claim authority to merge pull requests"),
    ("push to main", "instruct the agent to push to a default branch"),
    ("push to master", "instruct the agent to push to a default branch"),
    ("enable auto-merge", "allow enabling auto-merge"),
    ("all tests pass", "fabricate test results"),
    ("build succeeded", "fabricate build results"),
    ("ci passed", "fabricate CI results"),
]

NEGATION_MARKERS = (
    "never",
    "do not",
    "don't",
    "must not",
    "shall not",
    "no ",
    "forbid",
    "prohibit",
    "without",
    "out of scope",
    "not allow",
)

REQUIRED_DIRECTORIES = [
    "skills",
    "templates",
    "prompts",
    "examples",
    "docs",
    "scripts",
    ".github",
]

LINK_RE = re.compile(r"\[[^\]]*\]\((?!https?://|#|mailto:)([^)\s#]+)(?:#[^)]*)?\)")
FENCE_RE = re.compile(r"^```")


def iter_markdown_files() -> Iterable[Path]:
    for path in REPO_ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in path.relative_to(REPO_ROOT).parts):
            continue
        yield path


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        fail(f"MANIFEST.json not found at {MANIFEST_PATH}")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def warn(message: str) -> None:
    print(f"WARN: {message}", file=sys.stderr)


def check_manifest_files(manifest: dict) -> list[str]:
    declared = manifest.get("files", [])
    missing = []
    for entry in declared:
        path = REPO_ROOT / entry
        if not path.exists():
            missing.append(entry)
    return missing


def check_prompt_length() -> int:
    text = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    if len(text) > MAX_PROMPT_CHARS:
        fail(
            f"SYSTEM_PROMPT.txt is {len(text)} characters, "
            f"exceeds the {MAX_PROMPT_CHARS} limit"
        )
    return len(text)


def check_em_dashes() -> list[str]:
    offenders: list[str] = []
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        in_fence = False
        for line_no, line in enumerate(text.splitlines(), 1):
            if FENCE_RE.match(line.strip()):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if EM_DASH in line:
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{line_no}")
                break
    return offenders


def strip_code_blocks(text: str) -> str:
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def check_internal_links() -> list[str]:
    broken: list[str] = []
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        in_fence = False
        for line_no, line in enumerate(text.splitlines(), 1):
            if FENCE_RE.match(line.strip()):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_RE.finditer(line):
                target = match.group(1)
                # Skip anchors, remote URLs, and absolute paths
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                resolved = (path.parent / target).resolve()
                try:
                    resolved.relative_to(REPO_ROOT)
                except ValueError:
                    # Link points outside the repo; allowed but noted
                    continue
                if not resolved.exists():
                    rel = path.relative_to(REPO_ROOT)
                    broken.append(f"{rel}:{line_no} -> {target}")
    return broken


def check_required_directories() -> list[str]:
    missing: list[str] = []
    for entry in REQUIRED_DIRECTORIES:
        path = REPO_ROOT / entry
        if not path.is_dir():
            missing.append(entry)
    return missing


def split_sentences(text: str) -> list[str]:
    # Light-weight sentence splitter that preserves the original casing
    # of each sentence. Good enough for system-prompt prose, which is
    # written in short, full-stop-terminated sentences.
    sentences: list[str] = []
    buf: list[str] = []
    for char in text:
        buf.append(char)
        if char in ".!?":
            chunk = "".join(buf).strip()
            if chunk:
                sentences.append(chunk)
            buf = []
    tail = "".join(buf).strip()
    if tail:
        sentences.append(tail)
    return sentences


def check_prompt_red_lines() -> list[str]:
    text = strip_code_blocks(SYSTEM_PROMPT_PATH.read_text(encoding="utf-8"))
    bad: list[str] = []
    for sentence in split_sentences(text):
        lower = sentence.lower()
        for phrase, why in FORBIDDEN_PROMPT_PHRASES:
            if phrase not in lower:
                continue
            if any(marker in lower for marker in NEGATION_MARKERS):
                # The phrase appears in a sentence that already
                # forbids or negates the action. Allowed.
                continue
            bad.append(f"'{phrase}' ({why}) in: {sentence}")
            break  # one finding per sentence is enough
    return bad


def render_report(
    manifest: dict,
    prompt_chars: int,
    missing_files: list[str],
    em_dash_files: list[str],
    broken_links: list[str],
    missing_dirs: list[str],
    red_line_violations: list[str],
) -> str:
    status = "passed" if not (missing_files or em_dash_files or broken_links or missing_dirs or red_line_violations) else "failed"
    lines: list[str] = []
    lines.append("# Validation Report")
    lines.append("")
    lines.append(f"- Package name: {manifest.get('name', 'PatchPilot')}")
    lines.append(f"- Package version: {manifest.get('version', 'unknown')}")
    lines.append(f"- System prompt characters: {prompt_chars}")
    lines.append(f"- Character limit: less than {MAX_PROMPT_CHARS:,}")
    lines.append(f"- Total declared files: {len(manifest.get('files', []))}")
    md_files = sorted({p for p in manifest.get('files', []) if p.endswith('.md')})
    lines.append(f"- Markdown skills, templates, prompts, examples, docs: {len(md_files)}")
    lines.append(f"- README internal links checked: {manifest.get('total_readme_links', 'n/a')}")
    lines.append(f"- Missing declared files: {len(missing_files)}")
    lines.append(f"- Files with forbidden em dash characters: {len(em_dash_files)}")
    lines.append(f"- Broken internal Markdown links: {len(broken_links)}")
    lines.append(f"- Missing required directories: {len(missing_dirs)}")
    lines.append(f"- System prompt red-line violations: {len(red_line_violations)}")
    lines.append(f"- ZIP integrity: n/a (use scripts/build_zip.py to produce a release zip)")
    lines.append("")
    if status == "passed":
        lines.append("All structural checks passed.")
    else:
        lines.append("Validation FAILED. See details below.")
    if missing_files:
        lines.append("")
        lines.append("## Missing declared files")
        for entry in missing_files:
            lines.append(f"- `{entry}`")
    if em_dash_files:
        lines.append("")
        lines.append("## Em dash offenders")
        for entry in em_dash_files:
            lines.append(f"- `{entry}`")
    if broken_links:
        lines.append("")
        lines.append("## Broken internal links")
        for entry in broken_links:
            lines.append(f"- {entry}")
    if missing_dirs:
        lines.append("")
        lines.append("## Missing required directories")
        for entry in missing_dirs:
            lines.append(f"- `{entry}`")
    if red_line_violations:
        lines.append("")
        lines.append("## System prompt red-line violations")
        for entry in red_line_violations:
            lines.append(f"- {entry}")
    lines.append("")
    lines.append(
        "Run `python3 scripts/validate_pack.py --check` in CI to fail "
        "fast on any of the conditions above."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write VALIDATION_REPORT.md; exit non-zero on failure",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    prompt_chars = check_prompt_length()
    missing_files = check_manifest_files(manifest)
    em_dash_files = check_em_dashes()
    broken_links = check_internal_links()
    missing_dirs = check_required_directories()
    red_line_violations = check_prompt_red_lines()

    report = render_report(
        manifest=manifest,
        prompt_chars=prompt_chars,
        missing_files=missing_files,
        em_dash_files=em_dash_files,
        broken_links=broken_links,
        missing_dirs=missing_dirs,
        red_line_violations=red_line_violations,
    )

    if args.check:
        sys.stdout.write(report)
        if any([missing_files, em_dash_files, broken_links, missing_dirs, red_line_violations]):
            return 1
        return 0

    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"VALIDATION_REPORT.md regenerated ({len(report.splitlines())} lines).")
    if missing_files or em_dash_files or broken_links or missing_dirs or red_line_violations:
        warn("Report contains failures. Run with --check for CI mode.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
