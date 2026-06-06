"""Core verification engine for PoC.

Walks Python ASTs and applies rule modules to detect invariants violations.

Docs: verifier.doc.md
"""

import ast
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from poc.rules import (
    bare_except,
    mutable_defaults,
    unclosed_files,
    none_comparison,
    wildcard_imports,
    consistent_returns,
)


@dataclass
class CheckResult:
    """Result of a single rule check on a single file."""
    rule: str
    pass_: bool
    violations: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.rule,
            "pass": self.pass_,
            "violations": self.violations,
        }


# Ordered list of all rule modules
RULES = [
    bare_except,
    mutable_defaults,
    unclosed_files,
    none_comparison,
    wildcard_imports,
    consistent_returns,
]


def verify_file(filepath: str) -> Dict[str, Any]:
    """Verify a single Python file against all rules.

    Args:
        filepath: Path to the Python file.

    Returns:
        JSON-serialisable dict with per-rule results.
    """
    source = Path(filepath).read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {
            "file": filepath,
            "error": f"SyntaxError: {e}",
            "checks": [],
        }

    checks: List[CheckResult] = []
    for rule in RULES:
        violations = rule.check(tree, source)
        checks.append(
            CheckResult(
                rule=rule.RULE_NAME,
                pass_=len(violations) == 0,
                violations=violations,
            )
        )

    return {
        "file": filepath,
        "checks": [c.to_dict() for c in checks],
    }


def verify_directory(dirpath: str) -> List[Dict[str, Any]]:
    """Verify all Python files in a directory recursively.

    Args:
        dirpath: Path to the directory.

    Returns:
        List of per-file JSON-serialisable dicts.
    """
    results: List[Dict[str, Any]] = []
    root = Path(dirpath)
    for path in root.rglob("*.py"):
        # Skip hidden dirs and common non-source dirs
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        if "venv" in path.parts or "__pycache__" in path.parts:
            continue
        results.append(verify_file(str(path)))
    return results
