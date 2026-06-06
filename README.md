# PoC — Proof-of-Correctness

PoC is an automated code verifier that checks invariants by walking the Python AST. It catches common bugs and anti-patterns such as bare `except:` blocks, mutable default arguments, unclosed file handles, `== None` comparisons, wildcard imports, and inconsistent return types. It runs as a standalone CLI or integrates into CI pipelines (exit code 1 on any failure).

## SOTA Status

- Tests: **9 passing** (`pytest tests/ -q`, ~0.2s)
- CI: ![ci](https://img.shields.io/badge/ci-pending-lightgrey) (placeholder — wire up GitHub Actions)
- Maturity tier: **1 / 3** (MVP — v0.1.0)
- Last commit: 2026-06-06

## Quick Start

```bash
pip install -e .
poc verify path/to/file_or_dir
```

## CLI

```bash
poc verify <path>          # walks file or directory, prints violations
```

Exit code: `0` = clean, `1` = any violation found (suitable for CI gates).

## Integration

This tool is exposed in the unified `sin code` hub:

```bash
sin code poc verify .          # alias of: poc verify .
```

See `AGENTS.md` for boundaries, the rule catalogue, and verification steps.

## License

MIT

