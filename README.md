# SkillBag Docs

SkillBag Docs is a companion SkillBag repository for reusable document
processing skills. It focuses on workflows around PDFs and other office
document formats such as Word and ODT.

This repository is itself a valid SkillBag source:

- repository instructions live in [AGENTS.md](./AGENTS.md)
- installed skills live under [`.skills/`](./.skills/)
- the skill catalog lives at [`.skills/SKILLS.md`](./.skills/SKILLS.md)

The skills here are meant to be installed into other workspaces as
dependencies. They should stay reusable, format-focused, and independent of
one organization's filing conventions.

## Available Skills

### [skillbag-pdf-ocr](./.skills/skillbag-pdf-ocr/SKILL.md)

Checks whether a PDF already has a usable text layer and creates an OCR-backed
PDF only when needed.

Key parameters:

- `input-path` is required
- `language` defaults to `eng` and accepts Tesseract language expressions such
  as `eng+deu`
- `output-path` can override the generated OCR file location
- `output-suffix` defaults to `_OCR`
- `force` defaults to `false`

Behavior:

- reuses an existing OCR output when present unless `force=true`
- checks the original PDF for a usable text layer with `pdftotext`
- runs `ocrmypdf` only when OCR is needed or explicitly forced
- writes only the selected OCR output file and temporary files required for
  text inspection
- reports missing external tools clearly instead of creating placeholder output

Use this when a task needs machine-readable text from a scanned or image-only
PDF, while avoiding unnecessary OCR on already-readable documents.

## Planned Skill Areas

These areas are intentionally documented as roadmap, not as installed skills.
Only skills listed in [`.skills/SKILLS.md`](./.skills/SKILLS.md) are currently
available.

- PDF text extraction and structured extraction
- PDF splitting, merging, compression, and repair
- PDF/A and archival validation workflows
- Word document inspection and conversion helpers
- ODT and LibreOffice-based document conversion workflows
- document metadata inspection and cleanup
- batch document normalization for agent-readable workspaces

## How To Use

Typical usage is to add this repository as a SkillBag dependency from another
workspace, then install the needed skills into that workspace's `.skills/`
directory.

Example dependency declaration:

```yaml
dependencies:
  - name: skillbag-pdf-ocr
    version: main
    source: git@github.com:Skillbag-ai/skillbag-docs.git
```

`skillbag-pdf-ocr` also declares a dependency on
`skillbag-python-ensure` from
[`skillbag-utils`](https://github.com/Skillbag-ai/skillbag-utils), because it
uses a bundled Python helper script.

## Repository Layout

- [AGENTS.md](./AGENTS.md): repository-level installation metadata
- [README.md](./README.md): project overview
- [CONTRIBUTING.md](./CONTRIBUTING.md): contribution guidance
- [GOVERNANCE.md](./GOVERNANCE.md): document-skill repository governance
- [SUSTAINABILITY.md](./SUSTAINABILITY.md): funding and maintenance model
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md): collaboration standards
- [SECURITY.md](./SECURITY.md): security reporting guidance
- [CHANGELOG.md](./CHANGELOG.md): notable repository changes
- [LICENSE.md](./LICENSE.md): MIT license
- [`.skills/SKILLS.md`](./.skills/SKILLS.md): low-cost skill discovery catalog

## Design Notes

Document skills should be conservative about file writes. A skill must clearly
state which files it may create, modify, or delete, especially when operating
on user-supplied documents.

Prefer parameterized workflows over local naming assumptions. For example,
OCR languages, output paths, suffixes, and overwrite behavior should be
explicit parameters rather than hidden project policy.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Security

See [SECURITY.md](./SECURITY.md).

## License

Released under the MIT license. See [LICENSE.md](./LICENSE.md).
