# `unclosed_files.py`

Detects `open()` calls assigned to a variable but not used in a `with` statement
and never followed by `.close()`.

## Rationale
Leaked file handles exhaust OS resources and can prevent file deletion on Windows.

## Limitations
- Does not track flow across function boundaries
- Does not detect reassignment of the variable
