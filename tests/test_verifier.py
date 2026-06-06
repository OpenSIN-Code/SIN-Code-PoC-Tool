"""Tests for PoC verifier and rules.

Docs: test_verifier.doc.md
"""

from pathlib import Path

from poc.verifier import verify_file, verify_directory
from poc.rules import bare_except, mutable_defaults, unclosed_files, none_comparison, wildcard_imports, consistent_returns

FIXTURES = Path(__file__).parent / "fixtures"


def test_bare_except_rule():
    """Detect bare except: catches everything."""
    source = "try:\n    pass\nexcept:\n    pass\n"
    tree = __import__("ast").parse(source)
    v = bare_except.check(tree, source)
    assert len(v) == 1
    assert v[0]["line"] == 3


def test_mutable_defaults_rule():
    """Detect mutable default arguments."""
    source = "def f(a=[]):\n    pass\n"
    tree = __import__("ast").parse(source)
    v = mutable_defaults.check(tree, source)
    assert len(v) == 1
    assert v[0]["function"] == "f"


def test_unclosed_files_rule():
    """Detect open() without with or close()."""
    source = "f = open('x.txt')\n"
    tree = __import__("ast").parse(source)
    v = unclosed_files.check(tree, source)
    assert len(v) == 1
    assert v[0]["variable"] == "f"


def test_none_comparison_rule():
    """Detect == None and != None."""
    source = "if x == None:\n    pass\n"
    tree = __import__("ast").parse(source)
    v = none_comparison.check(tree, source)
    assert len(v) == 1


def test_wildcard_imports_rule():
    """Detect from module import *."""
    source = "from os import *\n"
    tree = __import__("ast").parse(source)
    v = wildcard_imports.check(tree, source)
    assert len(v) == 1
    assert v[0]["module"] == "os"


def test_consistent_returns_rule():
    """Detect inconsistent return types across branches."""
    source = "def f():\n    if True:\n        return 1\n    return 's'\n"
    tree = __import__("ast").parse(source)
    v = consistent_returns.check(tree, source)
    assert len(v) == 1
    assert "int" in v[0]["types"]
    assert "str" in v[0]["types"]


def test_integration_bad_file():
    """End-to-end: verify bad_code.py has failures."""
    result = verify_file(str(FIXTURES / "bad_code.py"))
    assert result["file"].endswith("bad_code.py")
    assert any(not c["pass"] for c in result["checks"])
    failed_rules = [c["rule"] for c in result["checks"] if not c["pass"]]
    assert "bare_except" in failed_rules
    assert "mutable_defaults" in failed_rules
    assert "unclosed_files" in failed_rules
    assert "none_comparison" in failed_rules
    assert "wildcard_imports" in failed_rules
    assert "consistent_returns" in failed_rules


def test_integration_good_file():
    """End-to-end: verify good_code.py passes all checks."""
    result = verify_file(str(FIXTURES / "good_code.py"))
    assert all(c["pass"] for c in result["checks"])


def test_verify_directory():
    """Verify directory scanning finds both fixtures."""
    results = verify_directory(str(FIXTURES))
    files = [r["file"] for r in results]
    assert any("bad_code.py" in f for f in files)
    assert any("good_code.py" in f for f in files)
