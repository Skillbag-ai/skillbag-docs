#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Ensure a PDF has a usable text layer, creating an OCR-backed copy "
            "only when needed."
        )
    )
    parser.add_argument("input_pdf", help="Path to the source PDF")
    parser.add_argument(
        "--language",
        default="eng",
        help="OCR language expression for ocrmypdf/Tesseract, such as eng+deu",
    )
    parser.add_argument(
        "--output-path",
        help="Optional explicit output PDF path. Defaults next to input PDF.",
    )
    parser.add_argument(
        "--output-suffix",
        default="_OCR",
        help="Suffix used when output path is omitted. Default: _OCR",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Recreate OCR output even when it exists or input text seems usable.",
    )
    parser.add_argument(
        "--min-text-chars",
        type=int,
        default=50,
        help="Minimum stripped text length considered usable. Default: 50",
    )
    parser.add_argument(
        "--min-alnum-chars",
        type=int,
        default=20,
        help="Minimum alphanumeric character count considered usable. Default: 20",
    )
    return parser.parse_args()


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def require_command(name: str) -> None:
    if shutil.which(name):
        return
    raise SystemExit(f"Missing required tool: {name}")


def default_output_path(pdf_path: Path, suffix: str) -> Path:
    return pdf_path.with_name(f"{pdf_path.stem}{suffix}.pdf")


def extract_text_sample(pdf_path: Path) -> str:
    require_command("pdftotext")
    with tempfile.NamedTemporaryFile(prefix="skillbag-pdf-ocr-", suffix=".txt", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        result = run(["pdftotext", str(pdf_path), str(tmp_path)])
        if result.returncode != 0:
            return ""
        return tmp_path.read_text(encoding="utf-8", errors="ignore").strip()
    finally:
        tmp_path.unlink(missing_ok=True)


def has_usable_text_layer(
    pdf_path: Path, min_text_chars: int, min_alnum_chars: int
) -> bool:
    sample = extract_text_sample(pdf_path)
    if len(sample) >= min_text_chars:
        return True
    alnum_count = sum(char.isalnum() for char in sample)
    return alnum_count >= min_alnum_chars


def ensure_parent_exists(output_path: Path) -> None:
    parent = output_path.parent
    if parent and not parent.exists():
        raise SystemExit(f"Output directory does not exist: {parent}")
    if parent and not parent.is_dir():
        raise SystemExit(f"Output parent is not a directory: {parent}")


def create_ocr_pdf(
    input_path: Path, output_path: Path, language: str, force: bool
) -> None:
    require_command("ocrmypdf")
    ensure_parent_exists(output_path)
    if output_path.exists() and force:
        output_path.unlink()
    cmd = [
        "ocrmypdf",
        "--skip-text",
        "--language",
        language,
        str(input_path),
        str(output_path),
    ]
    result = run(cmd)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "OCR failed"
        raise SystemExit(message)


def resolve_output_path(args: argparse.Namespace, input_path: Path) -> Path:
    if args.output_path:
        return Path(args.output_path)
    return default_output_path(input_path, args.output_suffix)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_pdf)
    if not input_path.exists():
        raise SystemExit(f"PDF not found: {input_path}")
    if not input_path.is_file():
        raise SystemExit(f"Input path is not a file: {input_path}")
    if input_path.suffix.lower() != ".pdf":
        raise SystemExit("Input file must be a PDF")
    if args.min_text_chars < 0 or args.min_alnum_chars < 0:
        raise SystemExit("Text-layer thresholds must be zero or greater")

    output_path = resolve_output_path(args, input_path)
    if output_path.resolve() == input_path.resolve():
        raise SystemExit("Output path must not be the same as the input PDF")
    if output_path.suffix.lower() != ".pdf":
        raise SystemExit("Output path must end with .pdf")

    if output_path.exists() and not args.force:
        print(f"existing-ocr: {output_path}")
        return

    if not args.force and has_usable_text_layer(
        input_path, args.min_text_chars, args.min_alnum_chars
    ):
        print(f"original-readable: {input_path}")
        return

    create_ocr_pdf(input_path, output_path, args.language, args.force)
    print(f"created-ocr: {output_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted")
