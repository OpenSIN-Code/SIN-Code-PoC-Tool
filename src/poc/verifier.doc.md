# `verifier.py`

Core verification engine. Walks AST and delegates to rule modules.

## Architecture
1. `verify_file` — parses one file, runs all rules, returns per-check results
2. `verify_directory` — recursively finds `*.py`, skips `venv`/`__pycache__`/hidden dirs
3. `CheckResult` — dataclass for a single rule result on a single file

## Rule Interface
Each rule module must expose:
- `RULE_NAME: str`
- `check(tree: ast.AST, source: str) -> List[Dict]`

Rules are imported in `verifier.py` and iterated in `RULES` list.
