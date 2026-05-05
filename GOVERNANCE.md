# SkillBag Docs Governance

SkillBag Docs is a companion repository for reusable document-processing
skills. It is not the normative standard. The normative specification lives in
the core SkillBag repository.

## Scope

This repository may define useful workflows for PDFs, OCR, office documents,
document conversion, document inspection, and document normalization.

It must not silently redefine core SkillBag semantics. If a document skill
needs behavior that changes the standard, propose that change in the core
`skillbag` repository first.

## Relationship to the Standard

Document skills should:

- follow the current `SKILLBAG.md` rules
- keep `.skills/SKILLS.md` synchronized
- document parameters and failure behavior clearly
- state file write boundaries explicitly
- preserve compatibility with the base skill format where practical

## Maintainer Decisions

Maintainers may merge document-skill changes when they are focused,
documented, and compatible with the core standard.

Changes should be rejected or moved to the core standard when they:

- alter precedence rules
- redefine installation semantics
- change valid source requirements
- introduce conflicting runtime tag behavior
- make broad policy decisions that affect all SkillBag workspaces

## Releases

Release notes should identify:

- new document skills
- breaking parameter or behavior changes
- compatibility updates required by the core standard
- security-relevant changes

## Sponsorship

Sponsorship can fund document-skill maintenance, tests, fixtures, and
documentation. It does not grant private control over these skills or the core
standard.

See [SUSTAINABILITY.md](./SUSTAINABILITY.md) for funding principles.
