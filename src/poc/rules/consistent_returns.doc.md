# `consistent_returns.py`

Heuristic: detects functions where different branches return different types.

## Rationale
Inconsistent return types are a common source of `TypeError` at runtime.
Static type checkers (mypy) catch this, but PoC provides a lightweight
AST-only alternative for projects without type annotations.

## Limitations
- Uses only literal type names; variable names are reported as-is
- `None` is ignored (returning a value or None is common)
