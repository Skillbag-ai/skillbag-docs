# Security Policy

SkillBag Docs is a repository of document-processing skills, not a hosted
service. Security issues can still exist when a document skill would cause an
agent to:

- overwrite source documents unexpectedly
- write output files outside the intended boundary
- leak document contents through unnecessary logging
- run unsafe conversion commands on untrusted files
- hide destructive behavior behind vague instructions

## Reporting

If you find a security issue in a document skill or repository instruction,
please report it privately to the maintainers before opening a public issue.

A useful report should include:

- the affected file or skill
- the security impact
- a concrete abuse or failure scenario
- any suggested mitigation

## Scope

Examples of in-scope issues:

- a skill that could overwrite unrelated files without clear instruction
- a document conversion workflow that writes outside its declared output path
- guidance that encourages unsafe handling of untrusted documents
- misleading OCR or extraction behavior that hides failed output

Examples of out-of-scope issues:

- generic concerns without a concrete repository impact
- third-party tool vulnerabilities unrelated to this repository's files
- accuracy limitations of OCR engines when the skill reports them honestly

## Disclosure

Please allow maintainers time to evaluate and address the report before public
disclosure.
