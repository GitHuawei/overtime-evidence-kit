# Roadmap

## Completed

### Phase 0: MVP Skeleton

- README, SOP, service boundary, and privacy documentation.
- Core schema files for events, evidence items, and packages.
- Mock input sources and mock evidence package.
- Basic validator and mock report renderer.
- Unit tests.

### Phase 1: Validation Enhancements

- GitHub Actions CI.
- JSON Schema validation.
- Time-order validation.
- `durationMinutes` consistency checks.
- Event evidence coverage validation.
- `quickLocator` substring validation.
- Mock-only sensitive pattern scanning.

### Open Source Readiness

- `LICENSE`.
- `CONTRIBUTING.md`.
- `SECURITY.md`.
- Open-source boundary documentation.
- README privacy warnings, quick start, and project scope.
- `.idea/` ignore rule.

### Open Source Preview

- Full mock month walkthrough.
- One-command quality gate.
- CI aligned with `scripts/check_all.py`.
- Improved validator output and rules.
- Improved mock report and evidence index outputs.
- Documentation for public outputs.
- Tests for key validation and rendering behavior.

### Phase A: Input Adapter MVP

- Mock source adapter fields.
- `scripts/build_mock_package.py`.
- `docs/input-adapters.md`.
- `docs/package-builder.md`.
- Build -> validate -> render workflow.

### Phase B: Rules Engine MVP

- `scripts/rules_engine.py`.
- `scripts/evaluate_mock_package.py`.
- `docs/rules-engine.md`.
- Automatic calculation of `evidenceStrength`, `qualityGate`, `riskFlags`, and `reviewAction`.

### Phase C: Public Output Polish

- GitHub-readable mock report structure.
- Stable public evidence index fields.
- Renderer consistency checks.
- Documentation for reading public outputs.

## Current

### Phase D: Open Source Release Candidate

Status: complete for `v0.1.0 Release Candidate`.

- Release Candidate README status.
- `CHANGELOG.md`.
- Release checklist.
- GitHub issue templates.
- Pull request template.
- Stronger contribution, security, and open-source boundary language.
- Release readiness audit in `scripts/check_all.py`.

### Phase E: Public Launch Prep

Status: complete for controlled public launch preparation.

- README first-screen launch wording.
- `CHANGELOG.md` known limitations.
- Public release checklist updates.
- Public launch notes.
- Repository setting suggestions.
- Launch readiness checks in `scripts/check_all.py`.

## Later Directions

- Stricter mock input adapter validation.
- Configurable rules-engine thresholds.
- Local-only redaction workflow design.
- Better CLI user experience.
- More fictional mock scenarios.
- Clearer validator grouping and remediation messages.

## Permanently Out of Scope

- Real case material.
- Real customer source evidence.
- Real WeChat, real Git, or real audio ingestion.
- Automatic legal conclusions.
- Replacing lawyers, arbitrators, courts, regulators, or professional judgment.
