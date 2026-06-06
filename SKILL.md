# sin-poc Skill

## Trigger
- User says: "verify code", "proof of correctness", "check invariants", "code quality check", "poc verify"

## Usage

```bash
poc verify <file_or_dir>
```

## Checks (MVP)
1. `bare_except` — no bare `except:` blocks
2. `mutable_defaults` — no mutable default arguments in functions
3. `unclosed_files` — no `open()` without `with` or `.close()`
4. `none_comparison` — no `== None`, use `is None`
5. `wildcard_imports` — no `from module import *`
6. `consistent_returns` — heuristic: return type consistency across branches

## Output
JSON report with `pass`/`fail` per check, per file.

## Integration
- CI pipeline: exit code 1 on any failure
- Pre-commit hook: `poc verify src/`
- Combine with `sin-orchestrate` for gating releases
