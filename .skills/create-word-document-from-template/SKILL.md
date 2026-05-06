---
name: create-word-document-from-template
description: Create a DOCX document from markdown using a user-supplied or context-defined Word template.
dependencies:
  - name: document-to-markdown-transcript
    required: false
allowed-tools: pandoc libreoffice soffice textutil python3 python
metadata:
  author: backupdev
  version: 1.0.0
---

## Parameters

```yaml
required:
  - name: markdown-source
  - name: output-docx
optional:
  - name: template-path
  - name: document-subtitle
  - name: template-context-key
    default: DOCX_TEMPLATE_PATH
  - name: overwrite
    default: false
```

## Instructions

- Use this skill when markdown should become a `.docx` while preserving a
  reusable Word template's style model.
- Treat `markdown-source` as the editable source of truth. Do not edit the
  generated `.docx` as the primary content source.
- Resolve `template-path` in this order:
  1. explicit `template-path`
  2. the context value named by `template-context-key`
  3. a clear user-provided template path in the current conversation
- If the resolved template path is a stable non-secret user preference, follow
  the core SkillBag input-resolution rule and persist it to `USER_CONTEXT.md`
  unless the user says not to.
- If no template is resolved, ask for a template path instead of silently using
  an unstyled default when the user requested a template-backed document.
- If `output-docx` exists and `overwrite=false`, stop and ask before replacing
  it.
- Convert markdown to DOCX using the best available local converter that
  preserves headings, paragraphs, bullet lists, numbered lists, code blocks,
  and pipe tables. Prefer `pandoc --reference-doc <template-path>` when
  available.
- If `document-subtitle` is supplied and the converter does not support a
  native subtitle field, add it to the markdown-derived document in a minimal,
  template-compatible way rather than hand-tuning styles.
- Validate the result after generation:
  - confirm `output-docx` exists and is non-empty
  - extract text with `textutil`, LibreOffice, or another available local tool
    when possible
  - spot-check that headings, lists, and tables survived sensibly
- Report any converter limitations or manual follow-up required.

## Outputs

- DOCX file at `output-docx`
- Markdown source retained as canonical editable content
- Brief validation summary

## File Boundaries

- May read `markdown-source` and `template-path`.
- May create or overwrite `output-docx` only under the requested overwrite
  policy.
- Must not overwrite the source markdown or template.
