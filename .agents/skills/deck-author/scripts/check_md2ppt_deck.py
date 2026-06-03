#!/usr/bin/env python3
"""Check and optionally compile an md2ppt Markdown deck."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path


EMBED_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+\.md)\)\s*$", re.IGNORECASE)
IMAGE_RE = re.compile(
    r"^!\[[^\]]*\]\(([^)]+\.(?:png|jpg|jpeg|gif|svg|webp|bmp))\)\s*$",
    re.IGNORECASE,
)
LAYOUT_RE = re.compile(r"^\[layout\]:\s*#\s*\(([^)]+)\)\s*$")
NOTE_RE = re.compile(r"^\[note\]:\s*#\s*\((.+)\)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
KNOWN_LAYOUTS = {
    "title_slide",
    "comparison",
    "title_and_content",
    "section_header",
    "two_content",
    "image_first",
    "two_images",
    "blank",
    "content_with_caption",
    "toc",
    "examples",
}


def decode_path(raw: str) -> str:
    return urllib.parse.unquote(raw.strip())


def has_frontmatter(lines: list[str]) -> bool:
    return bool(lines and lines[0].strip() == "---" and any(line.strip() == "---" for line in lines[1:]))


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def scan_file(path: Path, root_dir: Path, is_root: bool, seen: set[Path], stats: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    resolved = path.resolve()

    if resolved in seen:
        warnings.append(f"Skipped repeated embed: {path}")
        return errors, warnings
    seen.add(resolved)

    if not path.exists():
        errors.append(f"Missing file: {path}")
        return errors, warnings

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"Not UTF-8: {path} ({exc})")
        return errors, warnings

    lines = text.splitlines()
    stats["files"] += 1
    if is_root and not has_frontmatter(lines):
        warnings.append(f"{rel(path, root_dir)}: root deck has no YAML frontmatter")
    if not is_root and has_frontmatter(lines):
        warnings.append(f"{rel(path, root_dir)}: child frontmatter will be ignored by flatten.py")

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        location = f"{rel(path, root_dir)}:{lineno}"

        heading = HEADING_RE.match(stripped)
        if heading:
            stats[f"h{len(heading.group(1))}"] += 1

        if stripped in {"---", "___"}:
            stats["slide_breaks"] += 1
        if stripped == "***":
            stats["placeholder_breaks"] += 1

        layout = LAYOUT_RE.match(stripped)
        if layout:
            value = layout.group(1).strip()
            stats["layouts"] += 1
            if value not in KNOWN_LAYOUTS:
                warnings.append(f"{location}: layout '{value}' is not in refs/default.pptx known layout list")

        if NOTE_RE.match(stripped):
            stats["notes"] += 1

        embed = EMBED_RE.match(stripped)
        if embed:
            stats["embeds"] += 1
            child = (path.parent / decode_path(embed.group(1))).resolve()
            child_errors, child_warnings = scan_file(child, root_dir, False, seen, stats)
            errors.extend(child_errors)
            warnings.extend(child_warnings)
            continue

        if ".md)" in stripped.lower() and not embed:
            warnings.append(f"{location}: Markdown embed should be a standalone image-style link")

        image = IMAGE_RE.match(stripped)
        if image:
            stats["images"] += 1
            target = (path.parent / decode_path(image.group(1))).resolve()
            if not target.exists():
                errors.append(f"{location}: missing image {image.group(1)}")
            continue

        if re.search(r"!\[[^\]]*\]\([^)]+\.(?:png|jpg|jpeg|gif|svg|webp|bmp)\)", stripped, re.IGNORECASE):
            warnings.append(f"{location}: image should be on its own line for reliable md2ppt insertion")

    return errors, warnings


def compile_deck(args: argparse.Namespace) -> int:
    command_path = shutil.which(args.md2ppt_command)
    if not command_path:
        print(f"ERROR: md2ppt CLI not found on PATH: {args.md2ppt_command}", file=sys.stderr)
        return 2

    out = Path(args.out).resolve() if args.out else args.input.with_suffix(".pptx").resolve()
    cmd = [
        command_path,
        "-i",
        str(args.input),
        "-o",
        str(out),
    ]
    if args.ref:
        cmd.extend(["--ref", str(Path(args.ref).resolve())])
    elif args.template:
        cmd.extend(["--template", args.template])
    if args.debug_dir:
        cmd.extend(["--debug", "--debug-dir", str(Path(args.debug_dir).resolve())])

    print("Running:", " ".join(f'"{part}"' if " " in part else part for part in cmd))
    completed = subprocess.run(cmd, cwd=str(args.input.parent))
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Check and optionally compile an md2ppt Markdown deck.")
    parser.add_argument("input", type=Path, help="Root Markdown deck file")
    parser.add_argument("--compile", action="store_true", help="Run md2ppt after structural checks pass")
    parser.add_argument("--md2ppt-command", default="md2ppt", help="md2ppt CLI command name on PATH")
    parser.add_argument("--out", help="Output PPTX path for --compile")
    parser.add_argument("--template", default="default", help="Built-in template name for md2ppt --template")
    parser.add_argument("--ref", help="Explicit reference PPTX path for md2ppt --ref; overrides --template")
    parser.add_argument("--debug-dir", help="Pass --debug and this debug directory to md2ppt")
    args = parser.parse_args()

    args.input = args.input.resolve()
    root_dir = args.input.parent
    stats = {
        "files": 0,
        "embeds": 0,
        "images": 0,
        "layouts": 0,
        "notes": 0,
        "slide_breaks": 0,
        "placeholder_breaks": 0,
        "h1": 0,
        "h2": 0,
        "h3": 0,
        "h4": 0,
        "h5": 0,
        "h6": 0,
    }
    errors, warnings = scan_file(args.input, root_dir, True, set(), stats)

    print("md2ppt deck check")
    print(f"  root: {args.input}")
    print(f"  files: {stats['files']}  embeds: {stats['embeds']}  images: {stats['images']}")
    print(f"  headings: h1={stats['h1']} h2={stats['h2']} h3={stats['h3']} h4={stats['h4']} h5={stats['h5']} h6={stats['h6']}")
    print(f"  breaks: slides={stats['slide_breaks']} placeholders={stats['placeholder_breaks']}")
    print(f"  directives: layouts={stats['layouts']} notes={stats['notes']}")

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        return 1
    if args.compile:
        return compile_deck(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
