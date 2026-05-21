# Security Policy

## Supported Scope

The supported branch for this Release Candidate is `master`.

Security and privacy boundary issues include:

- A script, document, test, or template that could allow real private information to be committed.
- A validator or quality gate that misses obvious sensitive patterns.
- A public output renderer that exposes raw source material instead of safe summaries.
- CI behavior that diverges from `python scripts/check_all.py`.

## Do Not Publicly Submit Sensitive Information

Do not include real case material in issues, pull requests, discussions, commits, comments, attachments, or screenshots.

Never submit:

- Real WeChat chats, group chats, screenshots, exports, or message IDs.
- Real Git commits, repository names, branch names, source code, or commit hashes.
- Real recordings, transcripts, meeting notes, or file names.
- Real company names, person names, project names, client names, addresses, phone numbers, amounts, contract details, salaries, or identifiers.
- Any details that could identify a real workplace, dispute, customer, project, or person.

Use fictional mock data and `mock-*` identifiers when describing a problem.

## Reporting a Vulnerability

Use GitHub Security Advisories or another private channel for security-sensitive reports. Keep the report mock-only.

Include:

- Affected file or behavior.
- Fictional reproduction steps.
- Expected behavior.
- Actual behavior.
- Why the issue could create a privacy or release-readiness risk.

Do not attach real evidence or private material.

## Handling Principles

- Privacy boundary fixes take priority.
- Fixes should include tests or quality-gate coverage when practical.
- Public outputs must remain summaries and indexes, not raw evidence dumps.
- This project does not provide legal advice or promise legal outcomes.
