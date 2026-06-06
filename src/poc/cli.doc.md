# `cli.py`

Typer CLI for PoC. Entry point: `poc verify ...`.

## Commands
- `verify` — verify invariants in a file or directory

## Flags
- `--output` / `-o` — write JSON report to file
- `--config` / `-c` — future: config file for rule toggling

## Exit codes
- `0` — all checks passed
- `1` — any check failed or target not found
