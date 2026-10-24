#!/usr/bin/env python3
"""Export a Markdown-only skills bundle for chat interfaces that reject executable files.

This is a content export, not a runnable copy of EES. It intentionally excludes
scripts, tests, workflows, JSON schemas, configuration, and all non-Markdown files.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import zipfile

DEFAULT_INCLUDE = ("SKILL.md", "skills", "references/decision-and-failure-patterns.md")

def collect_markdown(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for rel in DEFAULT_INCLUDE:
        path = root / rel
        if path.is_file() and path.suffix.lower() == ".md":
            candidates.append(path)
        elif path.is_dir():
            candidates.extend(p for p in path.rglob("*.md") if p.is_file())
    # Also include module markdown files stored in the canonical skill tree.
    for p in (root / "skills").rglob("MODULE.md") if (root / "skills").exists() else []:
        candidates.append(p)
    return sorted(set(candidates), key=lambda p: p.relative_to(root).as_posix())

def export(root: Path, output: Path) -> int:
    root = root.resolve()
    files = collect_markdown(root)
    if not files:
        raise RuntimeError("No eligible Markdown files found; refusing to create an empty bundle")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            rel = path.relative_to(root).as_posix()
            # Defensive allowlist: only Markdown and no hidden or traversal paths.
            if path.suffix.lower() != ".md" or rel.startswith("/") or ".." in Path(rel).parts:
                continue
            zf.write(path, rel)
        zf.writestr("CHAT-SAFE-EXPORT-NOTICE.md",
                    "# Chat-safe skills export\n\n"
                    "This archive contains Markdown knowledge files only. It excludes executable code, "
                    "tests, CI workflows, schemas, and runtime configuration. It is not a runnable EES "
                    "package and does not provide runtime enforcement or sandboxing.\n")
    with zipfile.ZipFile(output) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"Export archive integrity check failed: {bad}")
        unsafe = [n for n in zf.namelist() if not n.lower().endswith(".md")]
        if unsafe:
            raise RuntimeError(f"Non-Markdown files found in export: {unsafe}")
    return len(files)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path("dist/EES_Gemini_Chat_Safe_Markdown.zip"))
    args = parser.parse_args()
    count = export(args.root, args.output)
    print(f"Exported {count} Markdown knowledge files to {args.output}; executable files excluded.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
