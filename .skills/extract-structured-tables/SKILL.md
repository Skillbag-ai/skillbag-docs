---
name: extract-structured-tables
description: Extract table-dominant documents into markdown tables and optional spreadsheet or CSV derivatives.
dependencies:
  - name: document-to-markdown-transcript
    required: false
  - name: skillbag-pdf-ocr
    required: false
allowed-tools: pdftotext ocrmypdf tesseract pandoc libreoffice soffice python3 python
metadata:
  author: backupdev
  version: 1.0.0
---

## Parameters

```yaml
required:
  - name: source-path
  - name: output-markdown
optional:
  - name: output-spreadsheet
  - name: output-csv-dir
  - name: language
    default: eng
  - name: force-ocr
    default: false
  - name: overwrite
    default: false
```

## Instructions

- Use this skill when a document, PDF page, screenshot, image, or transcript is
  mainly a table, matrix, register, checklist, pricing grid, role matrix, or
  control crosswalk.
- If `output-markdown` exists and `overwrite=false`, stop and ask before
  replacing it.
- Inspect the source before extraction. Strong table-dominance signals include:
  repeated row and column alignment, visible grid layout, consistent field
  labels, checklist columns, matrix cells, or flattened text that loses obvious
  structure.
- If the source is not table-dominant, do not force a table output. Use or
  recommend `document-to-markdown-transcript` instead.
- Use structure-preserving extraction first:
  - for PDFs, try layout-aware text extraction before OCR
  - when OCR is required, use `skillbag-pdf-ocr` or image OCR with the selected
    `language`
  - render or visually inspect pages when text extraction is ambiguous and
    local tools are available
- Normalize into markdown tables:
  - keep one logical table per section when possible
  - preserve header meaning instead of collapsing columns
  - preserve legends, notes, and footnotes directly below the related table
  - mark uncertain or unreadable cells explicitly
  - do not invent missing values
- If `output-spreadsheet` is supplied, create a workbook with one sheet per
  logical table when that improves readability.
- If `output-csv-dir` is supplied, write one CSV file per logical table using
  stable filenames.
- Return a concise extraction note covering why the source was treated as
  tabular, which outputs were created, and what remained ambiguous.

## Outputs

- Structured markdown derivative at `output-markdown`
- Optional workbook at `output-spreadsheet`
- Optional CSV files under `output-csv-dir`
- Extraction note with caveats

## File Boundaries

- May read `source-path`.
- May create or overwrite declared output files only under the requested
  overwrite policy.
- Must not overwrite the original source document.
