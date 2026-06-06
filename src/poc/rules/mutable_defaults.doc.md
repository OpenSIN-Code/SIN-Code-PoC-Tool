# `mutable_defaults.py`

Detects mutable literals (`[]`, `{}`, `set()`) as function default arguments.

## Rationale
Python evaluates default arguments once at definition time. Mutable defaults
are shared across calls, leading to surprising state accumulation.

## Fix
Use `None` as default and instantiate inside the function body.

```python
def f(a=None):
    if a is None:
        a = []
```
