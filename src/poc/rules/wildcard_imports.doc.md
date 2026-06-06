# `wildcard_imports.py`

Detects `from module import *`.

## Rationale
Wildcard imports pollute the namespace, make it hard to trace where names
come from, and can silently shadow builtins.

## Exceptions
- `__init__.py` re-exports are a common pattern and may be whitelisted in future.
