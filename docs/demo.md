# Demo Guide

The demo runs the complete mock-only pipeline with one command.

```powershell
python scripts/run_demo.py
```

It uses only the fictional mock source files already committed in this repository. It does not read user files, scan a real Git repository, import real chats, process recordings, or connect to external services.

## What the Demo Does

The demo pipeline:

1. Builds a mock evidence package from committed mock source files.
2. Evaluates mock events with the local rules engine.
3. Validates the evaluated package.
4. Renders a Markdown mock report.
5. Renders a CSV evidence index.
6. Prints a short summary with output paths.

## Generated Files

By default, files are written to `outputs/demo/`:

- `package.json`
- `mock-report.md`
- `mock-evidence-index.csv`

`outputs/demo/` is ignored by git and should not be committed.

## Custom Output Directory

Use `--output-dir` to write the demo output somewhere else:

```powershell
python scripts/run_demo.py --output-dir tmp/demo-output
```

The custom directory is for generated mock output only.

## Cleaning Output

To clean the default demo output, remove the generated directory:

```powershell
Remove-Item -Recurse -Force outputs/demo
```

The next demo run will recreate it.

## Mock-only Boundary

The demo deliberately does not:

- Read real WeChat chats, exports, screenshots, or message IDs.
- Scan real Git repositories, branches, source code, or commit hashes.
- Read recordings, transcripts, meeting notes, or private files.
- Process real company names, person names, project names, amounts, addresses, phone numbers, contracts, salaries, or identifiers.
- Produce legal advice, legal conclusions, or outcome guarantees.

If you want to experiment, create fictional mock inputs only. Do not copy, anonymize, or transform real case material into this repository.
