# Contributing

Thank you for considering a contribution to `overtime-evidence-kit`.

This repository is a mock-only open-source project. Contributions must be safe to publish publicly and must not include real case material.

## Ground Rules

- Submit only fictional mock data.
- Do not submit real WeChat chats, group chats, screenshots, exports, or message IDs.
- Do not submit real Git commits, repository names, source code, branch names, or commit hashes.
- Do not submit real recordings, transcripts, meeting notes, company names, person names, project names, client names, addresses, phone numbers, amounts, contract details, salaries, or identifiers.
- Do not submit examples derived from real cases, even if partially anonymized.
- Do not make legal conclusions, outcome promises, or service delivery commitments.
- Add tests for validator, renderer, schema, or rules-engine behavior changes.

## Development Flow

1. Create a focused branch from `master`.
2. Keep each pull request limited to one topic.
3. Update related documentation and tests.
4. Run local validation.
5. Confirm that every added sample is fictional and mock-only.

## Local Validation

Run:

```powershell
python scripts/check_all.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
```

## Mock-only Examples

Allowed:

- `mock-*` identifiers.
- Generic roles such as `technical worker`, `reviewer`, or `coordinator`.
- Fictional system names that are clearly generic examples.
- Structure-realistic but content-fictional timelines.

Forbidden:

- Real chat text or message exports.
- Real commit hashes, repository names, branch names, source code, or logs.
- Real audio summaries or transcripts.
- Real identities, organizations, customers, projects, addresses, phone numbers, or amounts.
- Dates, timelines, or combined details that could identify a real case.

## Pull Request Checklist

Before opening a pull request, confirm:

- Local tests pass.
- `python scripts/check_all.py` passes.
- The change includes only mock data.
- Documentation does not promise legal outcomes.
- New validator or renderer behavior has test coverage.
- No IDE files, local caches, generated temporary files, or private materials are committed.

## Where to Report Boundary Concerns

If you notice a privacy or mock-only boundary risk, open a privacy boundary issue using the template and describe the problem with fictional reproduction steps only.
