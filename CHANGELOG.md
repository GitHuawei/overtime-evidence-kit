# Changelog

## Unreleased

- No unreleased changes yet.

## v0.1.0 - planned

### Added

- Mock evidence package for a fictional sample month.
- Public mock evidence package boundaries for release review.
- JSON Schema files for package validation.
- Validator checks for schema, event timing, evidence coverage, and mock-only boundaries.
- Mock input adapter and package builder.
- Rules engine for evidence strength, quality gate, risk flags, and review action fields.
- Markdown mock report renderer.
- CSV evidence index renderer.
- `scripts/check_all.py` local quality gate.
- GitHub Actions CI.
- Open-source governance files.
- Release checklist, issue templates, and pull request template.

### Changed

- Project status moved from Open Source Preview to Release Candidate.
- README now emphasizes current capability, unsupported capability, public output examples, and final quality gates.
- Public outputs are designed for GitHub-readable review and avoid raw source material.
- Documentation now has stronger mock-only and privacy boundary warnings.

### Security

- Added release readiness checks for required governance files and public boundary language.
- Sensitive scan continues to block phone-number-like values, ID-card-like values, real-commit-like hashes, forbidden paths, and forbidden private-material markers.
- Contributors are instructed not to submit real chats, real Git data, real recordings, real identities, real organizations, real addresses, real phone numbers, real amounts, or any identifiable case details.
