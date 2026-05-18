# Changelog

All notable changes to this repository should be documented in this file.

The format is intentionally simple while the project remains a draft.

## v0.2.1

- Added EPUB extraction to `document-to-markdown-transcript` using local
  `pandoc`.

## v0.2.0

- Added `document-to-markdown-transcript` for creating normalized markdown
  transcripts from PDF, Word, ODT, image, text, and similar document sources.
- Added `extract-structured-tables` for table-dominant documents that need
  markdown tables and optional spreadsheet or CSV derivatives.
- Added `markdown-link-hygiene` for auditing or rewriting workspace-absolute
  local markdown links into portable relative links.
- Added `create-diagrams` for maintained diagram artifacts with markdown
  companion notes and optional Mermaid representations.
- Added `create-word-document-from-template` for generating DOCX files from
  markdown using a user-supplied or context-defined Word template.
- Added bundled Python helper scripts for `create-word-document-from-template`
  and `markdown-link-hygiene`, with `skillbag-python-ensure` dependencies.
- Rewrote `.skills/SKILLS.md` as a strict sorted SkillBag catalog.

## v0.1.0

- Initial scaffold of `skillbag-docs` as a SkillBag source repository for
  reusable document-processing skills.
- Added `skillbag-pdf-ocr` for checking whether a PDF has a usable text layer
  and creating an OCR-backed PDF only when needed.
- Documented planned future skill areas for PDF, Word, ODT, metadata,
  conversion, and document normalization workflows.
