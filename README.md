# overtime-evidence-kit

![CI](https://github.com/GitHuawei/overtime-evidence-kit/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

`overtime-evidence-kit` is a **mock-only** toolkit for structuring fictional overtime evidence packages with schemas, validators, renderers, and release checks.

It is safe to inspect because every committed example is fictional. The repository is for structure review, local demo runs, and open-source discussion. It is not a place to upload, process, summarize, or review real case material.

First run:

```powershell
python scripts/check_all.py
```

Run the demo:

```powershell
python scripts/run_demo.py
```

The demo writes generated mock output to `outputs/demo/`, which is ignored by git.

What you can run locally:

- Validate a committed mock evidence package.
- Build a package from fictional mock input sources.
- Evaluate mock events with local rules.
- Render a Markdown mock report and CSV evidence index.
- Run the same quality gate used by CI.

What this project does not do:

- No real chat import.
- No real Git repository scanning.
- No real audio or transcript processing.
- No SaaS hosting, account system, upload workflow, or paid service workflow.
- No legal advice, legal conclusions, or outcome guarantees.

## Project Status

Current status: **v0.1.0 Release Candidate**.

Included capabilities:

- Mock evidence package with fictional events and evidence items.
- JSON Schema validation for the public package structure.
- Validator checks for schema, time order, evidence coverage, mock-only boundaries, and sensitive patterns.
- Mock input adapter and rules engine for the sample package.
- Markdown mock report renderer.
- CSV evidence index renderer.
- `scripts/check_all.py` quality gate used locally and in CI.
- Open-source governance documents, release checklist, issue templates, and PR template.

Still not supported:

- Real chat import.
- Real Git repository scanning.
- Real audio processing or transcript ingestion.
- SaaS hosting or account-based workflows.
- Customer upload workflows or paid pilot materials.
- Legal advice, legal conclusions, or outcome guarantees.
- Real service delivery playbooks or private review procedures.

## Mock-only Boundary

All evidence data in this repository must be fictional mock data.

Do not submit, paste, migrate, summarize, or derive examples from:

- Real WeChat chats, group chats, screenshots, exports, or message IDs.
- Real Git commits, repository names, source code, branch names, or commit hashes.
- Real recordings, transcripts, meeting notes, or file names.
- Real company names, person names, project names, client names, addresses, phone numbers, contract details, salaries, amounts, or identifiers.
- Any combination of details that could identify a real dispute, workplace, customer, project, or person.

Mock examples must be created from the structure level. Do not anonymize a real case and commit it here.

This project does not provide legal advice and does not promise any negotiation, arbitration, litigation, or enforcement result.

## Appropriate Use

Use this repository to:

- Learn how a mock evidence package can be structured.
- Discuss schema, validator, renderer, and public output design.
- Run local checks against fictional samples.
- Contribute open-source improvements that preserve mock-only boundaries.

Do not use this repository to:

- Store or process real case evidence.
- Ask maintainers to review private material in issues, pull requests, or discussions.
- Generate legal conclusions.
- Replace professional legal review.
- Publish real employer, employee, customer, project, address, payment, or contact details.

## Quick Start

Run the full local quality gate:

```powershell
python scripts/check_all.py
```

Run the complete mock demo:

```powershell
python scripts/run_demo.py
```

Generated files:

- `outputs/demo/package.json`
- `outputs/demo/mock-report.md`
- `outputs/demo/mock-evidence-index.csv`

Validate the committed mock package:

```powershell
python scripts/validate_evidence_package.py examples/mock-evidence-package/package.json
```

Render the public mock report:

```powershell
python scripts/render_mock_report.py examples/mock-evidence-package/package.json
```

Render the public evidence index:

```powershell
python scripts/render_evidence_index.py examples/mock-evidence-package/package.json
```

Build and evaluate from mock input sources:

```powershell
python scripts/build_mock_package.py
python scripts/evaluate_mock_package.py examples/mock-evidence-package/package.json
```

## Example Output

Current committed mock output summary:

- Included events: 4
- Evidence items: 11
- Excluded candidates: 3
- Quality gates: `pass: 2`, `needs_review: 2`
- Evidence strength: `strong: 3`, `medium: 1`

Public outputs:

- [Mock report](examples/mock-evidence-package/mock-report.md)
- [Evidence index CSV](examples/mock-evidence-package/mock-evidence-index.csv)

The public report and CSV are meant for GitHub-readable review. They show structured summaries, evidence locators, quality gates, and review notes. They do not expose full chat text, recordings, source code, private workflow details, or legal conclusions.

## Quality Gates

`python scripts/check_all.py` covers:

- UTF-8 and text corruption checks.
- JSON and JSONL parsing.
- Mock package build and rules evaluation.
- Evidence package validation.
- Renderer execution.
- Committed output consistency.
- Unit tests.
- Sensitive pattern scanning.
- Release readiness file and boundary checks.

GitHub Actions runs the same quality gate through `.github/workflows/ci.yml`.

## Repository Layout

```text
.github/    CI, issue templates, and pull request template
docs/       SOP, specs, boundaries, release checklist, roadmap, and output docs
examples/   mock input sources, mock package, report, and evidence index
schema/     JSON Schema files
scripts/    validator, renderers, builder, rules engine, and check_all
tests/      unit tests
```

## Documentation

- [SOP](docs/SOP.md)
- [Use cases](docs/use-cases.md)
- [Mock month walkthrough](docs/mock-month-walkthrough.md)
- [Demo guide](docs/demo.md)
- [Evidence package spec](docs/evidence-package-spec.md)
- [Input adapters](docs/input-adapters.md)
- [Package builder](docs/package-builder.md)
- [Rules engine](docs/rules-engine.md)
- [Public outputs](docs/public-outputs.md)
- [Validation rules](docs/validation-rules.md)
- [Privacy and redaction](docs/privacy-and-redaction.md)
- [Service boundary](docs/service-boundary.md)
- [Open-source boundary](docs/open-source-boundary.md)
- [Release checklist](docs/release-checklist.md)
- [Public launch notes](docs/public-launch.md)
- [Repository settings](docs/repository-settings.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## Contributing

Contributions are welcome when they preserve the mock-only boundary. Before opening a pull request, run:

```powershell
python scripts/check_all.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
```

Do not include real evidence, private materials, or identifiable case details in issues, pull requests, commits, tests, documentation, or discussions.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
