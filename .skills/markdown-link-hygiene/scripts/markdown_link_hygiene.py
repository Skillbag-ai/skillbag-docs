#!/usr/bin/env python3
"""Audit or rewrite workspace-absolute markdown file links."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote


LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")


def split_target(target: str) -> tuple[str, str]:
    path_part, sep, fragment = target.partition("#")
    if sep:
        return path_part, f"#{fragment}"
    return path_part, ""


def is_external_target(target: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target))


def candidate_files(scope: Path, patterns: list[str]) -> list[Path]:
    if scope.is_file():
        return [scope]
    files: set[Path] = set()
    for pattern in patterns:
        files.update(path for path in scope.rglob(pattern) if path.is_file())
    return sorted(files)


def rewrite_text(text: str, source_file: Path, root: Path) -> tuple[str, list[tuple[str, str]]]:
    changes: list[tuple[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        if is_external_target(target):
            return match.group(0)

        path_part, fragment = split_target(target)
        if not path_part.startswith("/"):
            return match.group(0)

        absolute_path = Path(unquote(path_part)).resolve()
        try:
            absolute_path.relative_to(root)
        except ValueError:
            return match.group(0)

        relative = os.path.relpath(absolute_path, start=source_file.parent)
        relative = relative.replace(os.sep, "/")
        relative = quote(relative, safe="/.-_~")
        new_target = f"{relative}{fragment}"
        changes.append((target, new_target))
        return f"{prefix}{new_target}{suffix}"

    return LINK_RE.sub(replace, text), changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-path", default=".", help="Workspace root path.")
    parser.add_argument("--scope-path", help="File or directory to scan. Defaults to root path.")
    parser.add_argument(
        "--mode",
        choices=("audit", "rewrite"),
        default="audit",
        help="Audit only or rewrite matching links.",
    )
    parser.add_argument(
        "--include-pattern",
        action="append",
        default=[],
        help="Glob pattern to include. May be passed more than once.",
    )
    args = parser.parse_args()

    root = Path(args.root_path).resolve()
    scope = Path(args.scope_path).resolve() if args.scope_path else root
    patterns = args.include_pattern or ["*.md", "*.mdx"]

    if not root.exists():
        raise SystemExit(f"root path does not exist: {root}")
    if not scope.exists():
        raise SystemExit(f"scope path does not exist: {scope}")

    changed: dict[Path, list[tuple[str, str]]] = {}
    for file_path in candidate_files(scope, patterns):
        text = file_path.read_text(encoding="utf-8")
        updated, changes = rewrite_text(text, file_path.resolve(), root)
        if not changes:
            continue
        changed[file_path] = changes
        if args.mode == "rewrite":
            file_path.write_text(updated, encoding="utf-8")

    action = "Would rewrite" if args.mode == "audit" else "Rewrote"
    print(f"{action} {len(changed)} file(s).")
    for file_path, changes in changed.items():
        print(file_path)
        for old, new in changes:
            print(f"  {old} -> {new}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
