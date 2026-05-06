---
name: markdown-link-hygiene
description: Audit or rewrite local markdown links so workspace-absolute file targets become portable relative links. #use/skillbag-python-ensure
dependencies:
  - name: skillbag-python-ensure
    source: git@github.com:Skillbag-ai/skillbag-utils.git
    version: main
    required: true
allowed-tools: python3 python
metadata:
  author: backupdev
  version: 1.0.0
---

## Parameters

```yaml
optional:
  - name: root-path
    default: .
  - name: scope-path
  - name: mode
    default: audit
    values:
      - audit
      - rewrite
  - name: include-patterns
    default:
      - "*.md"
      - "*.mdx"
```

## Instructions

- Use this skill when markdown links should remain portable across machines,
  clones, and workspace roots.
- Scan markdown files under `scope-path` if supplied, otherwise under
  `root-path`.
- Detect markdown link targets that point to local absolute paths inside
  `root-path`.
- In `audit` mode:
  - report each non-portable link with source file and target
  - do not modify files
- In `rewrite` mode:
  - rewrite only markdown link targets, not arbitrary prose
  - preserve the visible link text
  - resolve the target path inside `root-path`
  - compute the relative path from the source markdown file to the target
  - preserve anchors and fragments such as `#section`
  - preserve URL encoding where needed
  - leave links outside `root-path` unchanged
- After rewrite, re-scan the same scope and report whether any workspace-
  absolute local markdown links remain.
- Run the bundled helper script after `skillbag-python-ensure`:

  ```bash
  python3 .skills/markdown-link-hygiene/scripts/markdown_link_hygiene.py --root-path <root-path> [--scope-path <scope-path>] --mode audit
  python3 .skills/markdown-link-hygiene/scripts/markdown_link_hygiene.py --root-path <root-path> [--scope-path <scope-path>] --mode rewrite
  ```

- If a repeated document-generation workflow creates non-portable links,
  mention the likely source workflow so it can be fixed separately.

## Outputs

- Audit report, or rewritten markdown files plus verification report

## File Boundaries

- In `audit` mode, must not write files.
- In `rewrite` mode, may modify markdown files only under the selected scope.
- Must not rewrite external URLs or local paths outside `root-path`.
