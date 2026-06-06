"""Rule: heuristic check for inconsistent return types across branches.

Docs: consistent_returns.doc.md
"""

import ast
from typing import Any, Dict, List, Optional

RULE_NAME = "consistent_returns"


def check(tree: ast.AST, source: str) -> List[Dict[str, Any]]:
    """Flag functions where branches return different types (e.g., int vs str).

    This is a simple heuristic: collect all return values' type names and
    warn if there are 2+ distinct types (excluding None).
    """
    violations: List[Dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return_types = _collect_return_types(node)
            # Filter out None-only returns
            non_none = [t for t in return_types if t != "NoneType"]
            if len(non_none) > 1 and len(set(non_none)) > 1:
                violations.append({
                    "line": node.lineno,
                    "message": f"Function '{node.name}' may return inconsistent types: {sorted(set(non_none))}",
                    "function": node.name,
                    "types": sorted(set(non_none)),
                })
    return violations


def _collect_return_types(func: ast.AST) -> List[str]:
    """Walk a function body and collect return-value type names."""
    types: List[str] = []
    for node in ast.walk(func):
        if isinstance(node, ast.Return) and node.value is not None:
            types.append(_type_name(node.value))
    return types


def _type_name(node: ast.AST) -> str:
    """Return a rough type name for an AST expression node."""
    if isinstance(node, ast.Constant):
        return type(node.value).__name__
    # Python < 3.8 compatibility (not available in 3.14+)
    if hasattr(ast, "NameConstant") and isinstance(node, ast.NameConstant):
        return type(node.value).__name__
    if isinstance(node, ast.List):
        return "list"
    if isinstance(node, ast.Dict):
        return "dict"
    if isinstance(node, ast.Tuple):
        return "tuple"
    if isinstance(node, ast.Set):
        return "set"
    if hasattr(ast, "Str") and isinstance(node, ast.Str):  # Python < 3.8
        return "str"
    if hasattr(ast, "Num") and isinstance(node, ast.Num):  # Python < 3.8
        return type(node.n).__name__
    if isinstance(node, ast.Name):
        return node.id  # variable name, best effort
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return f"{node.func.id}()"
        if isinstance(node.func, ast.Attribute):
            return f"{node.func.attr}()"
    return "unknown"
