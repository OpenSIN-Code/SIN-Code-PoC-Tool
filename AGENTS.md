# SIN-Code-PoC-Tool — Agent-Engineering Hints

## What it does (1 sentence)
Proof-of-Correctness — automated AST-based verifier that catches bare `except:`, mutable default arguments, unclosed file handles, `== None` comparisons, wildcard imports, and inconsistent return types; exits 1 on any failure for CI gating.

## Stack
- Language: Python
- Version: 0.1.0
- Test count: 9 tests
- CLI: `poc` with 1 subcommand (`verify`)

## When to use
- CI gate to fail builds on common anti-patterns that ruff/flake8 miss or don't fail-fast on.
- Pre-commit hook to catch invariant violations before they reach review.
- One-shot audit of an unfamiliar Python codebase to surface low-hanging quality issues.

## Boundaries
- Do NOT remove or rename rules in `src/poc/rules/` without bumping the major version — rule IDs are part of the public contract.
- Do NOT extend the rule engine with anything that needs runtime execution — PoC is a pure-static AST tool by design.
- Always add a new rule as a self-contained module in `src/poc/rules/` with its own `.doc.md`.
- Always keep `verifier.py`'s exit-code contract: `0` = clean, `1` = any violation found.

## Key files
- `src/poc/verifier.py` — AST walker that loads rules and emits violations.
- `src/poc/rules/` — one module per invariant (drop-in extension point).
- `src/poc/cli.py` — Typer CLI (single `verify` command, file-or-directory input).
- `tests/test_verifier.py` — 9 behavioral tests (good-file pass, bad-file fail, directory walk).
- `tests/fixtures/` — paired `good_*.py` / `bad_*.py` files exercised by the tests.

## Verification
- `pytest tests/ -v` — all 9 tests pass.
- `poc --help` — prints help with the `verify` subcommand.
- `poc verify tests/fixtures/` — smoke test on the bundled fixtures (expect non-zero exit).
