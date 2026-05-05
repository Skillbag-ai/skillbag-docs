---
name: skillbag-pdf-ocr
description: Ensure a PDF has a usable OCR text layer, creating an OCR-backed copy only when needed. #use/skillbag-python-ensure
dependencies:
  - name: skillbag-python-ensure
    source: git@github.com:Skillbag-ai/skillbag-utils.git
    version: main
    required: true
allowed-tools: python3 python pdftotext ocrmypdf
metadata:
  author: backupdev
  version: 1.0.0
---

## Parameters

```yaml
required:
  - name: input-path
optional:
  - name: language
    default: eng
  - name: output-path
  - name: output-suffix
    default: _OCR
  - name: force
    default: false
  - name: min-text-chars
    default: 50
  - name: min-alnum-chars
    default: 20
  - name: python-command
    default: python3
```

## Instructions

- Use this skill when a PDF must be readable as text and may be scanned,
  image-only, or missing a useful text layer.
- Use `skillbag-python-ensure` before running the bundled Python helper.
- Treat `input-path` as the path to an existing PDF file.
- Treat `language` as the Tesseract or `ocrmypdf` language expression. Use
  `eng` by default; use values such as `eng+deu`, `fra`, or `spa+eng` when
  the user or document context calls for them.
- If `output-path` is omitted, write the OCR copy next to the input PDF as
  `<input-stem><output-suffix>.pdf`.
- If the computed or explicit output file already exists and `force=false`,
  reuse it and do not run OCR again.
- If `force=false`, inspect the original PDF for a usable text layer before
  running OCR. Use `min-text-chars` and `min-alnum-chars` as the heuristic
  thresholds.
- If the original PDF already has usable text, use the original PDF and do not
  create a separate OCR copy.
- If the original PDF does not have usable text, run OCR and produce the
  output PDF.
- If `force=true`, recreate the OCR output even when it already exists or the
  original appears readable.
- Do not overwrite the original PDF.
- Do not create, modify, or delete unrelated files. Temporary files used for
  text inspection are allowed and must be cleaned up.
- If `pdftotext` or `ocrmypdf` is missing, stop and report the missing tool.
  Do not create placeholder OCR files.

## Execution

From a SkillBag workspace root, run:

```bash
python3 .skills/skillbag-pdf-ocr/scripts/ensure_ocr_pdf.py <input-path>
```

With a language expression:

```bash
python3 .skills/skillbag-pdf-ocr/scripts/ensure_ocr_pdf.py <input-path> --language eng+deu
```

With an explicit output file:

```bash
python3 .skills/skillbag-pdf-ocr/scripts/ensure_ocr_pdf.py <input-path> --output-path <output-path>
```

To recreate the OCR output:

```bash
python3 .skills/skillbag-pdf-ocr/scripts/ensure_ocr_pdf.py <input-path> --force
```

## External Tools

- Python 3 runs the bundled helper script.
- `pdftotext` is used only to estimate whether a useful text layer already
  exists.
- `ocrmypdf` performs OCR and normally relies on Tesseract and Ghostscript.

Ask before installing missing system tools or Python packages. The skill's
responsibility is to run the workflow when the tools are available and to
report clear prerequisites when they are not.
