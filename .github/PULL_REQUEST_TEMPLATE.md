## Summary

Describe the change.

## Mock-only and Privacy Checklist

- [ ] This pull request contains only fictional mock data.
- [ ] It contains no real WeChat chats, group chats, screenshots, exports, or message IDs.
- [ ] It contains no real Git commits, repository names, branch names, source code, or commit hashes.
- [ ] It contains no real recordings, transcripts, meeting notes, or file names.
- [ ] It contains no real names, company names, project names, customer names, addresses, phone numbers, amounts, contracts, salaries, or identifiers.
- [ ] It contains no real service delivery workflow, private review procedure, or customer material.
- [ ] It does not promise legal advice, legal conclusions, or legal outcomes.
- [ ] It does not add pricing, paid pilot material, private service SOP, or real customer intake content to the public repository.

## Validation

- [ ] I ran `python scripts/check_all.py`.
- [ ] I ran `python -m unittest discover -s tests -p "test_*.py"`.
- [ ] I ran `git diff --check`.
- [ ] New validator, renderer, schema, or rules-engine behavior has test coverage.
- [ ] Documentation was updated where relevant.
