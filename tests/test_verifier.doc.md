# `test_verifier.py`

Unit + integration tests for PoC verifier and individual rules.

## Scenarios Covered
1. `test_bare_except_rule` — bare except block
2. `test_mutable_defaults_rule` — list as default arg
3. `test_unclosed_files_rule` — open() without with/close
4. `test_none_comparison_rule` — `== None`
5. `test_wildcard_imports_rule` — `from os import *`
6. `test_consistent_returns_rule` — int vs str returns
7. `test_integration_bad_file` — end-to-end on bad_code.py
8. `test_integration_good_file` — end-to-end on good_code.py
9. `test_verify_directory` — directory scanning

## Fixtures
- `tests/fixtures/bad_code.py` — all 6 violations
- `tests/fixtures/good_code.py` — clean code, all pass
