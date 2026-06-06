"""Rule: detect wildcard imports (`from module import *`).

Docs: wildcard_imports.doc.md
"""

import ast
from typing import Any, Dict, List

RULE_NAME = "wildcard_imports"


def check(tree: ast.AST, source: str) -> List[Dict[str, Any]]:
    """Find from-imports that use the wildcard '*'."""
    violations: List[Dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    violations.append({
                        "line": node.lineno,
                        "message": f"Wildcard import from '{node.module or 'unknown'}'",
                        "module": node.module,
                    })
    return violations
