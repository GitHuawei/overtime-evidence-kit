# Release Checklist

This checklist prepares `overtime-evidence-kit` for a `v0.1.0 Release Candidate` state. It does not create a GitHub Release or publish a package.

## Local Checks

Run:

```powershell
python scripts/check_all.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
git status --short
```

Expected result:

- All checks pass.
- `docs/plans/` is not staged.
- No local temporary files are staged.

## Content Audit

Confirm:

- README states Release Candidate status.
- README explains supported and unsupported capabilities.
- README links to public mock outputs.
- Documentation does not promise legal outcomes.
- Examples are fictional mock data.
- Tests do not include real data.
- Scripts do not rely on private local paths.
- CI calls `python scripts/check_all.py`.

## Sensitive Information Audit

Confirm the repository does not contain:

- Real WeChat chats or group chats.
- Real Git commits, repository names, branch names, source code, or commit hashes.
- Real recordings or transcripts.
- Real person names.
- Real company names.
- Real project names.
- Real customer names.
- Real addresses.
- Real phone numbers.
- Real amounts, salaries, contracts, or identifiers.
- Any detail combination that could identify a real case.

## GitHub Repository Settings

Suggested manual settings before a formal release:

- Repository description mentions mock-only evidence package tooling.
- Repository topics are generic and do not imply legal advice.
- Branch protection is configured if collaborators are added.
- Security advisories are enabled.
- Issue templates and PR template are visible.

## v0.1.0 Tag Preparation

These commands are documentation only. Do not run them unless the maintainer explicitly decides to create a tag:

```powershell
git tag -a v0.1.0 -m "v0.1.0 release candidate"
git push origin v0.1.0
```

Do not create a GitHub Release unless explicitly requested by the maintainer.

## Final Boundary Check

Before publishing any release notes, confirm:

- No real evidence appears in the repository, issues, pull requests, discussions, screenshots, or attachments.
- All examples use mock-only data.
- The project does not claim to provide legal advice.
- Public outputs remain summaries and indexes, not raw evidence dumps.
