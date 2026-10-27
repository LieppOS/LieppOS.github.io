#!/usr/bin/env python3
"""Validate the mdBook source tree: navigation, links, anchors and assets.

Read-only. Never writes to ``src/`` or ``book/``, and never fetches remote
URLs: external links are syntax-checked only, so CI stays offline-safe.

Checks
------
1. Every ``SUMMARY.md`` target exists on disk.
2. Every Markdown page (other than ``SUMMARY.md``) appears in the navigation.
3. No duplicate navigation entries.
4. Every relative Markdown link resolves to an existing page or asset.
5. Every ``#fragment`` resolves to a heading anchor in the target page.
6. Fenced code blocks are balanced.

Exit status 0 when clean, 1 when problems are found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SUMMARY = "SUMMARY.md"
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
FENCE = re.compile(r"^\s*```", re.MULTILINE)
LINK = re.compile(r"!?\[(?P<label>[^\]]*)\]\((?P<dest>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
REMOTE = ("http://", "https://", "mailto:")


def slugify(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[^\w\s-]", "", text.strip().lower())
    return re.sub(r"\s+", "-", text).strip("-")


def headings(text: str) -> set[str]:
    found: dict[str, int] = {}
    for match in HEADING.finditer(text):
        base = slugify(match.group(2))
        if not base:
            continue
        seen = found.get(base, 0)
        found[base] = seen + 1
        if seen:
            found[f"{base}-{seen}"] = 1
    return set(found)


def normalise(rel: str, dest: str) -> str:
    parts: list[str] = []
    for segment in (Path(rel).parent / dest).as_posix().split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if parts:
                parts.pop()
            continue
        parts.append(segment)
    return "/".join(parts)


def check(src: Path) -> list[str]:
    errors: list[str] = []
    pages = {p.relative_to(src).as_posix(): p for p in src.rglob("*.md") if p.name != SUMMARY}

    summary_path = src / SUMMARY
    if not summary_path.is_file():
        return [f"{SUMMARY} is missing from {src}"]
    summary = summary_path.read_text(encoding="utf-8")
    targets = [m.group("dest") for m in LINK.finditer(summary)]
    local = [t for t in targets if not t.startswith(REMOTE)]

    for dest in local:
        if normalise(SUMMARY, dest) not in pages:
            errors.append(f"{SUMMARY}: navigation target does not exist: {dest}")

    for dup in sorted({t for t in targets if targets.count(t) > 1}):
        errors.append(f"{SUMMARY}: duplicate navigation entry: {dup}")

    listed = {normalise(SUMMARY, d) for d in local}
    for rel in sorted(pages):
        if rel not in listed:
            errors.append(f"orphan page not reachable from {SUMMARY}: {rel}")

    anchors = {rel: headings(p.read_text(encoding="utf-8")) for rel, p in pages.items()}

    for rel, path in sorted(pages.items()):
        text = path.read_text(encoding="utf-8")
        if len(FENCE.findall(text)) % 2:
            errors.append(f"{rel}: unbalanced fenced code block")

        for match in LINK.finditer(text):
            dest = match.group("dest")
            if dest.startswith(REMOTE):
                continue
            if dest.startswith("#"):
                frag = dest[1:]
                if frag and frag not in anchors[rel]:
                    errors.append(f"{rel}: broken local anchor: {dest}")
                continue

            target, _, frag = dest.partition("#")
            resolved = normalise(rel, target)

            if resolved in pages:
                if frag and frag not in anchors[resolved]:
                    errors.append(f"{rel}: broken anchor {dest} (no such heading in {resolved})")
                continue
            if (src / resolved).is_file():
                continue
            errors.append(f"{rel}: broken link or missing asset: {dest}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, default=Path(__file__).resolve().parent.parent / "src")
    args = parser.parse_args(argv)

    if not args.src.is_dir():
        print(f"error: source directory not found: {args.src}", file=sys.stderr)
        return 2

    errors = check(args.src)
    if errors:
        print(f"FAILED: {len(errors)} problem(s)", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    count = len([p for p in args.src.rglob("*.md") if p.name != SUMMARY])
    print(f"OK: {count} pages, navigation complete, no broken links, anchors or assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
