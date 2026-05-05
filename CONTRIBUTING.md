# Contributing to SkillBag Docs

Thanks for contributing.

This repository contains reusable document-processing skills for SkillBag
workspaces. Good contributions keep document workflows explicit, safe, and
portable across projects.

## Before You Start

- Read [README.md](./README.md).
- Read [AGENTS.md](./AGENTS.md).
- Review the current document skills in [`.skills/`](./.skills/).
- Check the core SkillBag standard before relying on behavior that may be
  normative.

## What Good Contributions Look Like

Strong contributions usually do at least one of the following:

- add a reusable document workflow that belongs outside the core standard
- improve safety around document reads, writes, conversions, or OCR
- clarify parameters, output paths, language settings, or overwrite behavior
- reduce local assumptions in favor of reusable defaults
- keep `SKILLS.md` and skill metadata synchronized

## Skill Editing Rules

When editing or adding a document skill:

- keep the canonical skill name stable unless a rename is intentional
- keep the `description` concise because it is part of the discovery surface
- preserve valid YAML frontmatter followed by Markdown instructions
- keep `metadata.version` in semantic version format
- update [`.skills/SKILLS.md`](./.skills/SKILLS.md) so it stays exact and sorted
- state file read and write boundaries clearly
- move large secondary detail into `references/`, `scripts/`, or `assets/`
  only when needed

## What To Avoid

Avoid changes that:

- hide destructive document operations behind vague instructions
- overwrite source documents by default
- assume one organization's folder names, languages, or document workflow
- duplicate rules that belong in the core SkillBag standard
- leave skill descriptions or catalog entries out of sync

## Pull Requests

Pull requests should:

- stay focused on one document skill or one logical behavior change
- update documentation affected by the change
- call out any parameter, metadata, dependency, or behavior change clearly

## Changelog

If the change is meaningful for users of this repository, add a short entry to
[CHANGELOG.md](./CHANGELOG.md).
