"""
Generate ivolve_netlify_manifest_vN.txt by walking this folder.

Auto-increments the version number: finds the highest existing
ivolve_netlify_manifest_v*.txt and writes v(N+1).

Each line is:    relative/path/filename.ext | filename.ext

A blank line is inserted whenever the parent directory changes,
so files group naturally by folder.

System/cache files (Thumbs.db, .DS_Store, desktop.ini, .gitignore-style
hidden files) are excluded. The manifest itself, this script, and the
.bat that runs it are also excluded so they never appear in the output.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Files we never want in the manifest.
EXCLUDE_NAMES = {
    "Thumbs.db",
    ".DS_Store",
    "desktop.ini",
    "generate_netlify_manifest.py",
    "run_netlify_manifest.bat",
    "netlify_manifest_run_log.txt",
}

# Folders to skip entirely (anywhere in the tree)
EXCLUDE_DIRS = {".git", "node_modules", ".vscode", ".idea", "__pycache__"}


def is_excluded(p: Path) -> bool:
    if p.name in EXCLUDE_NAMES:
        return True
    if p.name.startswith("."):
        return True
    # Don't list previously-generated manifests
    if re.match(r"ivolve_netlify_manifest_v\d+\.txt$", p.name):
        return True
    # Skip anything inside an excluded folder
    for part in p.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def next_version_number() -> int:
    """Find ivolve_netlify_manifest_vN.txt files and return N+1."""
    pattern = re.compile(r"^ivolve_netlify_manifest_v(\d+)\.txt$")
    highest = 0
    for f in ROOT.iterdir():
        if not f.is_file():
            continue
        m = pattern.match(f.name)
        if m:
            n = int(m.group(1))
            if n > highest:
                highest = n
    return highest + 1


def collect_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if is_excluded(p):
            continue
        files.append(p)
    return files


def sort_key(p: Path) -> tuple:
    """Sort by directory path (case-insensitive), then filename (case-insensitive).
    Files in the root come before files in subfolders."""
    rel = p.relative_to(ROOT)
    parts = rel.parts
    depth = len(parts)
    folder = "/".join(parts[:-1]).lower()
    name = parts[-1].lower()
    return (folder, depth, name)


def main() -> None:
    version = next_version_number()
    output_path = ROOT / f"ivolve_netlify_manifest_v{version}.txt"

    print(f"Scanning: {ROOT}")
    files = collect_files()
    print(f"Found {len(files)} files. Writing v{version}...\n")

    if not files:
        print("ERROR: No files found.")
        sys.exit(1)

    files.sort(key=sort_key)

    lines: list[str] = []
    prev_folder: str | None = None

    for p in files:
        rel = p.relative_to(ROOT)
        rel_str = rel.as_posix()  # forward slashes
        folder = "/".join(rel.parts[:-1])
        if prev_folder is not None and folder != prev_folder:
            lines.append("")
        lines.append(f"{rel_str} | {p.name}")
        prev_folder = folder

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Brief summary
    folder_counts: dict[str, int] = {}
    for p in files:
        rel = p.relative_to(ROOT)
        parts = rel.parts
        if len(parts) == 1:
            key = "(root)"
        elif parts[0] == "images" and len(parts) >= 3 and parts[1] == "projects":
            key = f"images/projects/{parts[2]}"
        elif len(parts) >= 2:
            key = "/".join(parts[:2])
        else:
            key = parts[0]
        folder_counts[key] = folder_counts.get(key, 0) + 1

    print(f"Wrote {output_path.name} with {len(files)} files:")
    for key in sorted(folder_counts):
        print(f"  {folder_counts[key]:3d}  {key}")
    print()
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
