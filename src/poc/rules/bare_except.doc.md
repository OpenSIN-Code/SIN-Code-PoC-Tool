# `bare_except.py`

Detects bare `except:` blocks that catch `SystemExit` and `KeyboardInterrupt`.

## Rationale
Bare excepts are dangerous in production because they silently swallow
unrecoverable exceptions. Always catch explicit exception types.

## False Positives
- `except Exception:` is allowed (not bare)
