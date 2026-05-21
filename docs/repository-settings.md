# Repository Settings

This document suggests GitHub repository settings for a controlled public launch. It is documentation only and does not require API access.

## Description

Suggested repository description:

```text
Mock-only toolkit for structuring overtime evidence packages with schemas, validators, renderers, and release checks.
```

## Topics

Suggested topics:

```text
overtime
evidence-toolkit
mock-evidence
mock-data
json-schema
validation
documentation
python
open-source
```

Avoid topics that imply legal advice, production evidence handling, or official dispute resolution.

## Homepage

Recommended setting: leave blank unless a stable public documentation page exists.

## Issues

Recommended setting: enable issues only with the existing issue templates visible.

Maintainers should close or edit issues that include real evidence, private data, or identifiable case details.

## Discussions

Recommended setting: keep discussions disabled until moderation expectations are clear.

If discussions are enabled later, pin a mock-only warning and do not allow private evidence review requests.

## Pull Requests

Recommended setting: keep pull requests open to public contributors, with the PR template enabled.

Require contributors to confirm:

- Only fictional mock data is included.
- No real chats, Git data, recordings, identities, organizations, addresses, phone numbers, amounts, or case details are included.
- No legal conclusions or outcome promises are added.

## Branch Protection

Suggested for `master` when more contributors are added:

- Require CI to pass.
- Require review before merge.
- Block force pushes.
- Prefer linear history if maintainers want simple release review.

## Security

Recommended settings:

- Enable GitHub Security Advisories.
- Keep `SECURITY.md` visible.
- Ask reporters to use fictional mock reproduction steps.
- Do not request real evidence in public or private reports.

## Releases and Tags

Do not create a GitHub Release or tag until the maintainer explicitly decides to do so.

When a release is approved, use `CHANGELOG.md` as the release-note base and keep known limitations visible.
