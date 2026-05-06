---
name: create-diagrams
description: Create or update diagram artifacts with a markdown companion note and optional Mermaid representation.
metadata:
  author: backupdev
  version: 1.0.0
---

## Parameters

```yaml
required:
  - name: diagram-title
  - name: diagram-path
  - name: diagram-scope
optional:
  - name: diagram-type
    default: mermaid
  - name: source-artifacts
    default: []
  - name: companion-note-path
  - name: include-mermaid
    default: true
  - name: overwrite
    default: false
```

## Instructions

- Use this skill when a task needs a maintained diagram artifact rather than a
  one-off inline sketch.
- Treat `diagram-path` as the primary diagram artifact. Supported values for
  `diagram-type` include `mermaid`, `drawio`, or another explicit format the
  user requests and the workspace can reasonably create.
- If `companion-note-path` is omitted, write a sibling markdown note using the
  same basename as `diagram-path`.
- Before creating a new diagram, check whether `diagram-path` or
  `companion-note-path` already exists.
  - If either exists and `overwrite=false`, update the existing artifact only
    when the user clearly asked for an update.
  - If the request could create a duplicate diagram for the same scope, stop
    and ask whether to update the existing diagram or create a new one.
- The companion markdown note MUST include:
  - diagram title
  - path to the primary diagram artifact
  - diagram scope
  - source artifacts or source context used
  - what the diagram does not prove
  - caveats or interpretation notes when needed
- When `include-mermaid=true`, include a Mermaid representation in the
  companion note unless the primary diagram itself is already Mermaid-only.
- Keep diagrams source-backed. Do not present inferred relationships as
  verified facts; label inferences or assumptions clearly in the companion
  note.
- Keep file links relative to the companion note when linking local source
  artifacts.

## Outputs

- Primary diagram artifact at `diagram-path`
- Markdown companion note
- Mermaid representation when requested

## File Boundaries

- May create or update `diagram-path`.
- May create or update `companion-note-path`.
- Must not modify unrelated documents or source artifacts.
