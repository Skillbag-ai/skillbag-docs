#!/usr/bin/env python3
"""Create a markdown transcript from a local document source.

This is a conservative local extractor used by resource pipelines. It prefers
native text layers and local command-line tools, marks extraction caveats, and
never modifies the original source file.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".csv", ".json", ".jsonl", ".yaml", ".yml"}
PDF_SUFFIXES = {".pdf"}
WORD_SUFFIXES = {".docx", ".doc", ".odt", ".rtf"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_command(args: list[str]) -> tuple[str, str]:
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return result.stdout, result.stderr


def extract_pdf(path: Path) -> tuple[str, str]:
    if not shutil.which("pdftotext"):
        return "", "pdftotext not available; PDF transcript not generated"
    stdout, _ = run_command(["pdftotext", "-layout", str(path), "-"])
    return stdout, "pdftotext -layout"


def extract_word(path: Path) -> tuple[str, str]:
    if shutil.which("pandoc"):
        stdout, _ = run_command(["pandoc", str(path), "-t", "markdown"])
        return stdout, "pandoc markdown"
    if shutil.which("textutil"):
        stdout, _ = run_command(["textutil", "-convert", "txt", "-stdout", str(path)])
        return stdout, "textutil txt"
    return "", "no pandoc or textutil available; document transcript not generated"


def extract_image(path: Path, language: str) -> tuple[str, str]:
    if not shutil.which("tesseract"):
        return "", "tesseract not available; image transcript not generated"
    stdout, _ = run_command(["tesseract", str(path), "stdout", "-l", language])
    return stdout, f"tesseract {language}"


def extract_text(path: Path, language: str) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        return path.read_text(errors="ignore"), "text copy"
    if suffix in PDF_SUFFIXES:
        return extract_pdf(path)
    if suffix in WORD_SUFFIXES:
        return extract_word(path)
    if suffix in IMAGE_SUFFIXES:
        return extract_image(path, language)
    return "", f"unsupported source type: {suffix or '<none>'}"


def write_transcript(
    input_path: Path,
    output_markdown: Path,
    text: str,
    method: str,
    include_metadata: bool,
) -> None:
    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    if include_metadata:
        header = "\n".join(
            [
                "---",
                f"source_path: {input_path}",
                f"source_sha256: {sha256(input_path)}",
                f"generated_at: {datetime.now(timezone.utc).isoformat()}",
                f"extraction_method: {method}",
                "---",
                "",
            ]
        )
    else:
        header = ""
    output_markdown.write_text(header + text.strip() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_markdown", type=Path)
    parser.add_argument("--language", default="eng")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--include-metadata", action="store_true", default=True)
    args = parser.parse_args()

    if args.output_markdown.exists() and not args.overwrite:
        print(f"reused existing transcript: {args.output_markdown}")
        return

    text, method = extract_text(args.input_path, args.language)
    if not text.strip():
        raise SystemExit(f"no transcript text extracted for {args.input_path}: {method}")
    write_transcript(args.input_path, args.output_markdown, text, method, args.include_metadata)
    print(f"wrote transcript: {args.output_markdown} ({method})")


if __name__ == "__main__":
    main()
