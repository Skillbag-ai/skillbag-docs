---
name: document-to-markdown-transcript
description: Create a normalized markdown transcript from PDF, EPUB, Word, ODT, image, text, or similar document sources. #use/skillbag-pdf-ocr
dependencies:
  - name: skillbag-pdf-ocr
    required: false
allowed-tools: pdftotext ocrmypdf tesseract pandoc libreoffice soffice textutil python3 python
metadata:
  author: backupdev
  version: 1.0.0
---

## Parameters

```yaml
required:
  - name: input-path
  - name: output-markdown
optional:
  - name: language
    default: eng
  - name: force-ocr
    default: false
  - name: overwrite
    default: false
  - name: include-metadata
    default: true
```

## Instructions

- Use this skill when a document should be converted into markdown for faster
  later agent processing instead of repeatedly reading the original binary or
  page-rendered file.
- Prefer the bundled script for deterministic local extraction:
  `python3 .skills/document-to-markdown-transcript/scripts/document_to_markdown_transcript.py <input-path> <output-markdown>`
- Treat `input-path` as the original source document. Do not modify it.
- Treat `output-markdown` as the normalized transcript path.
- If `output-markdown` exists and `overwrite=false`, reuse it and report that
  no new transcript was generated.
- Choose the extraction path by source type:
  - PDF with usable text: extract text with layout-aware settings when helpful.
  - PDF without usable text or when `force-ocr=true`: use
    `skillbag-pdf-ocr` first, then extract text from the OCR-backed PDF.
  - Word, ODT, or EPUB documents: use `pandoc`, LibreOffice, `textutil`, or
    another available local converter to preserve headings, lists, tables, and
    links as markdown when possible. EPUB extraction requires `pandoc`.
  - Images: use OCR with `language`, then normalize the result into markdown.
  - Plain text or existing markdown: copy or normalize the content without
    inventing structure.
- Preserve document structure over visual fidelity:
  - headings should stay headings when detectable
  - lists should stay lists
  - tables should stay tables only when structure is sufficiently clear
  - page headers, footers, and repeated boilerplate may be collapsed only when
    they are clearly repetitive noise
- At the top of the transcript, include a short metadata block when
  `include-metadata=true`:
  - source path
  - extraction method
  - OCR language when OCR was used
  - extraction caveats or uncertain sections
- If a table-heavy source loses structure during transcript generation, stop
  using this skill as the only output and recommend or invoke
  `extract-structured-tables`.
- Do not silently invent missing or unreadable content. Mark uncertain text
  clearly.

## Outputs

- Markdown transcript at `output-markdown`
- Brief extraction summary, including OCR use and caveats

## File Boundaries

- May read `input-path`.
- May create `output-markdown`.
- May create an OCR-backed PDF only through `skillbag-pdf-ocr` when needed.
- Must not overwrite the original source document.
