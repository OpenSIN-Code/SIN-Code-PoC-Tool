"""Rule: detect `== None` or `!= None` comparisons (should be `is None` / `is not None`).

Docs: none_comparison.doc.md
"""

import ast
from typing import Any, Dict, List

RULE_NAME = "none_comparison"


def check(tree: ast.AST, source: str) -> List[Dict[str, Any]]:
    """Find equality comparisons against None instead of identity checks."""
    violations: List[Dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for op in node.ops:
                if isinstance(op, (ast.Eq, ast.NotEq)):
                    # Check if any comparator is a Constant(None) or NameConstant(None)
                    for comparator in node.comparators:
                        if _is_none(comparator):
                            violations.append({
                                "line": node.lineno,
                                "message": "Use 'is None' or 'is not None' instead of == / !=",
                            })
    return violations


def _is_none(node: ast.AST) -> bool:
    """Check if an AST node represents the None literal."""
    if isinstance(node, ast.Constant) and node.value is None:
        return True
    if hasattr(ast, "NameConstant") and isinstance(node, ast.NameConstant) and node.value is None:  # Python < 3.8
        return True
    return False
