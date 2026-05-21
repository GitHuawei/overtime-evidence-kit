# Public Launch Notes

This document prepares `overtime-evidence-kit` for a controlled public launch. It is public-safe documentation only and does not create a GitHub Release or tag.

## Launch Readiness Summary

Current status: `v0.1.0 Release Candidate`.

Ready to show publicly:

- Mock-only evidence package structure.
- JSON Schema validation.
- Local validator.
- Mock input builder.
- Rules engine for fictional events.
- Markdown report renderer.
- CSV evidence index renderer.
- CI-backed quality gate.
- Governance, security, contribution, issue, and PR templates.

Not included:

- Real WeChat import.
- Real Git scanning.
- Real audio or transcript handling.
- SaaS hosting or account workflows.
- Customer upload workflows.
- Paid service delivery material.
- Legal advice, legal conclusions, or outcome guarantees.

## Pre-public Checklist

Before announcing the repository:

- Run `python scripts/check_all.py`.
- Run `python -m unittest discover -s tests -p "test_*.py"`.
- Run `git diff --check`.
- Confirm `docs/plans/` is not staged or committed.
- Confirm README states mock-only boundaries near the top.
- Confirm `CHANGELOG.md` includes known limitations.
- Confirm issue and PR templates warn against real evidence.
- Confirm no GitHub Release or tag is created unless explicitly approved.

## Repository Description Suggestion

```text
Mock-only toolkit for structuring overtime evidence packages with schemas, validators, renderers, and release checks.
```

## Short Public Introduction

```text
overtime-evidence-kit is a mock-only open-source toolkit for exploring how overtime-related evidence packages can be structured, validated, and rendered locally. It ships fictional sample data, schemas, validators, renderers, and release checks. It does not process real evidence and does not provide legal advice.
```

## What Not to Say Publicly

Do not claim that this project:

- Handles real disputes.
- Imports real chats, Git repositories, recordings, or transcripts.
- Produces legal conclusions.
- Predicts negotiation, arbitration, litigation, or enforcement outcomes.
- Provides a paid service workflow or private delivery procedure.
- Accepts private evidence in issues, pull requests, discussions, or attachments.

## Post-launch Monitoring Checklist

After making the repository public or announcing it:

- Watch new issues for real evidence or private information.
- Close or redact reports that include identifiable material.
- Point contributors to the issue templates and mock-only boundary.
- Confirm CI stays green on `master`.
- Monitor whether README wording causes confusion about real evidence support.
- Keep GitHub Release and tag creation as a separate maintainer decision.
