"""Rule: detect mutable default arguments in function definitions.

Docs: mutable_defaults.doc.md
"""

import ast
from typing import Any, Dict, List

RULE_NAME = "mutable_defaults"

MUTABLE_TYPES = (ast.List, ast.Dict, ast.Set)


def check(tree: ast.AST, source: str) -> List[Dict[str, Any]]:
    """Find function arguments whose default value is a mutable literal."""
    violations: List[Dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults:
                if isinstance(default, MUTABLE_TYPES):
                    violations.append({
                        "line": node.lineno,
                        "message": f"Mutable default argument in function '{node.name}'",
                        "function": node.name,
                    })
            # Also check kw_defaults (keyword-only defaults)
            for default in node.args.kw_defaults:
                if default is not None and isinstance(default, MUTABLE_TYPES):
                    violations.append({
                        "line": node.lineno,
                        "message": f"Mutable default keyword argument in function '{node.name}'",
                        "function": node.name,
                    })
    return violations
