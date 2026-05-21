# Release Checklist

This checklist prepares `overtime-evidence-kit` for controlled public launch of a `v0.1.0 Release Candidate` repository state. It does not create a GitHub Release, create a tag, or publish a package.

## Public Visibility Decision

Confirm before making the repository public or announcing it:

- Repository visibility decision is intentional.
- README first screen says the project is mock-only.
- README explains what can run locally.
- README explains unsupported capabilities.
- `CHANGELOG.md` has reviewed `v0.1.0 - planned` release notes.
- `docs/public-launch.md` and `docs/repository-settings.md` are current.
- No GitHub Release or tag is created unless explicitly approved.

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
- No GitHub Release or tag has been created by the checklist.

## Content Audit

Confirm:

- README states Release Candidate status.
- README explains supported and unsupported capabilities.
- README links to public mock outputs.
- README links to public launch and repository setting notes.
- CHANGELOG includes known limitations.
- Documentation does not promise legal outcomes.
- Examples are fictional mock data.
- Tests do not include real data.
- Scripts do not rely on private local paths.
- CI calls `python scripts/check_all.py`.
- Issue and PR templates are present.

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
- Homepage is blank unless a stable public documentation site exists.
- Discussions are disabled until moderation expectations are clear, or enabled with a pinned mock-only warning.
- Branch protection is configured if collaborators are added.
- Security advisories are enabled.
- Issue templates and PR template are visible.
- Actions badge points to the current CI workflow.

## v0.1.0 Tag Preparation

These commands are documentation only. Do not run them unless the maintainer explicitly decides to create a tag:

```powershell
git tag -a v0.1.0 -m "v0.1.0 release candidate"
git push origin v0.1.0
```

Do not create a GitHub Release unless explicitly requested by the maintainer.

## Release Note Decision

Before creating a tag or GitHub Release later, confirm:

- `CHANGELOG.md` is the source of truth for release notes.
- Known limitations remain visible.
- Release notes do not mention real cases, customer work, private delivery processes, pricing, or legal outcomes.
- The release title does not imply production support for real evidence.

## Final Boundary Check

Before publishing any release notes, confirm:

- No real evidence appears in the repository, issues, pull requests, discussions, screenshots, or attachments.
- All examples use mock-only data.
- The project does not claim to provide legal advice.
- Public outputs remain summaries and indexes, not raw evidence dumps.
