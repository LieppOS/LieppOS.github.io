#!/usr/bin/env python3
"""Import a PUBLIC research repo into mdBook, keeping raw evidence out.

The importer never modifies the research source. Its allowlist and size
limits reduce accidental overpublication, but are NOT a privacy audit.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import quote, unquote, urlsplit

REPO = "LieppOS/LieppOS-ulefone-gq5012bf1-research"
SOURCE_URL = f"https://github.com/{REPO}"
SOURCE_ROOT_DIRS = (
    "DOCS", "docs", "reports", "hardware", "kernel", "reverse-engineering",
    "usb-research", "slot-b-investigation", "slot-b-invalidation",
)
BLOCKED_DIRS = {"evidence", "raw", "dumps", "private", "backups", ".git", "workspace"}
MAX_MD_BYTES = 1_500_000
CURATED_SUMMARY = "SUMMARY.md"
# The generated archive lives in its own directory so curated pages can keep
# using src/research/ without being deleted by an import run.
ARCHIVE_DIR = "research-archive"
ARCHIVE_MARKER = "# Research archive"
DEFAULT_SUMMARY = "# Summary\n\n[Introduction](README.md)\n[Understanding evidence](evidence.md)"
LINK_PATTERN = re.compile(r'(?P<bang>!?)\[(?P<label>[^\]]*)\]\((?P<dest>[^)\s]+)(?P<suffix>\s+"[^"]*")?\)')
H1_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def eligible(rel: Path) -> bool:
    if any(p.startswith(".") or p.lower() in BLOCKED_DIRS for p in rel.parts):
        return False
    return rel.as_posix() == "README.md" or (len(rel.parts) >= 2 and rel.parts[0] in SOURCE_ROOT_DIRS)


def collect(source: Path) -> dict[Path, Path]:
    result = {}
    candidates = [source / "README.md"]
    for dirname in SOURCE_ROOT_DIRS:
        folder = source / dirname
        if folder.is_dir() and not folder.is_symlink():
            candidates.extend(folder.rglob("*.md"))
    for candidate in candidates:
        if candidate.is_symlink() or not candidate.is_file():
            continue
        try:
            rel = candidate.relative_to(source)
            if eligible(rel) and candidate.stat().st_size <= MAX_MD_BYTES:
                if candidate.resolve().is_relative_to(source.resolve()):
                    result[rel] = candidate
        except (ValueError, OSError):
            continue
    return dict(sorted(result.items(), key=lambda item: item[0].as_posix().casefold()))


def sha_for(source: Path) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "HEAD"


def github_blob(ref: str, rel: Path, raw: bool = False) -> str:
    prefix = f"https://raw.githubusercontent.com/{REPO}/{ref}/" if raw else f"{SOURCE_URL}/blob/{ref}/"
    return prefix + "/".join(quote(s) for s in rel.parts)


def rewrite_links(body: str, rel: Path, included: set[Path], ref: str) -> str:
    # Fenced code blocks are left untouched to preserve command examples.
    chunks = re.split(r"(^```[^\n]*\n.*?^```\s*$|^~~~[^\n]*\n.*?^~~~\s*$)", body, flags=re.MULTILINE | re.DOTALL)

    def rewrite(m: re.Match[str]) -> str:
        original = m.group("dest")
        url = urlsplit(original)
        if url.scheme or url.netloc or original.startswith(("/", "#")):
            return m.group(0)
        from pathlib import PurePosixPath
        import posixpath
        decoded = unquote(url.path)
        normalized = posixpath.normpath(posixpath.join(rel.parent.as_posix(), decoded))
        if normalized == ".." or normalized.startswith("../"):
            return m.group(0)
        target = Path(PurePosixPath(normalized))
        anchor = ("?" + url.query if url.query else "") + ("#" + url.fragment if url.fragment else "")
        if target in included and not m.group("bang"):
            href = os.path.relpath(Path(ARCHIVE_DIR) / target, Path(ARCHIVE_DIR) / rel.parent).replace(os.sep, "/") + anchor
        else:
            href = github_blob(ref, target, raw=bool(m.group("bang"))) + anchor
        return f'{m.group("bang")}[{m.group("label")}]({href}{m.group("suffix") or ""})'

    return "".join(chunk if idx % 2 else LINK_PATTERN.sub(rewrite, chunk) for idx, chunk in enumerate(chunks))


def page_title(text: str, rel: Path) -> str:
    match = H1_PATTERN.search(text)
    name = match.group(1).strip() if match else rel.stem.replace("-", " ").replace("_", " ").title()
    return name.replace("[", "\\[").replace("]", "\\]").replace("\n", " ")[:90]


def import_repo(source: Path, destination: Path) -> int:
    source = source.resolve()
    if not source.is_dir():
        raise ValueError(f"Source checkout not found: {source}")
    docs = collect(source)
    ref = sha_for(source)
    dest_research = destination / ARCHIVE_DIR
    if dest_research.exists():
        shutil.rmtree(dest_research)
    dest_research.mkdir(parents=True)
    included = set(docs)
    titles = {}
    for rel, file in docs.items():
        target = dest_research / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        text = file.read_text(encoding="utf-8", errors="replace")
        titles[rel] = page_title(text, rel)
        text = rewrite_links(text, rel, included, ref)
        text += f"\n\n---\n\n[Original research source]({github_blob(ref, rel)}) · Git revision `{ref}`\n"
        target.write_text(text, encoding="utf-8")
    curated = destination / CURATED_SUMMARY
    head = DEFAULT_SUMMARY
    if curated.is_file():
        # Keep only the curated part so repeated imports do not stack archives.
        existing = curated.read_text(encoding="utf-8").split(ARCHIVE_MARKER, 1)[0].rstrip()
        if existing:
            head = existing
    lines = [head, "", ARCHIVE_MARKER, ""]
    if Path("README.md") in titles:
        lines += [f"- [Project overview]({ARCHIVE_DIR}/README.md)", ""]
    for category in SOURCE_ROOT_DIRS:
        pages = [rel for rel in docs if rel.parts[0] == category and len(rel.parts) > 1]
        if not pages:
            continue
        lines += [f"# {category.replace('-', ' ').replace('_', ' ').title()}", ""]
        for rel in pages:
            path = "/".join(quote(part) for part in rel.parts)
            lines.append(f"- [{titles[rel]}]({ARCHIVE_DIR}/{path})")
        lines.append("")
    (destination / "SUMMARY.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Imported {len(docs)} allowlisted Markdown files from {source} @ {ref}")
    return len(docs)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Local checkout of the public research repository")
    parser.add_argument("--dest", type=Path, default=Path(__file__).resolve().parent.parent / "src")
    args = parser.parse_args()
    import_repo(args.source, args.dest)


if __name__ == "__main__":
    main()
