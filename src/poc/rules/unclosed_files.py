"""Rule: detect `open()` calls not inside a `with` statement and without `.close()`.

Docs: unclosed_files.doc.md
"""

import ast
from typing import Any, Dict, List, Set

RULE_NAME = "unclosed_files"


def check(tree: ast.AST, source: str) -> List[Dict[str, Any]]:
    """Find open() calls that are not guarded by a with statement or closed explicitly.

    Heuristic: if open() is assigned to a name and that name is never used in
    a `.close()` call and not inside a with-statement context, flag it.
    """
    violations: List[Dict[str, Any]] = []

    # Find all with-context variables that come from open()
    with_vars: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.With):
            for item in node.items:
                if isinstance(item.context_expr, ast.Call) and _is_open_call(item.context_expr):
                    if isinstance(item.optional_vars, ast.Name):
                        with_vars.add(item.optional_vars.id)
                    elif isinstance(item.optional_vars, ast.Tuple):
                        for elt in item.optional_vars.elts:
                            if isinstance(elt, ast.Name):
                                with_vars.add(elt.id)

    # Find all open() calls assigned to names
    open_assignments: Dict[str, int] = {}  # name -> line
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(node.value, ast.Call) and _is_open_call(node.value):
                    open_assignments[target.id] = node.lineno

    # Find all .close() calls
    closed_vars: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "close":
            if isinstance(node.func.value, ast.Name):
                closed_vars.add(node.func.value.id)

    for var, line in open_assignments.items():
        if var not in with_vars and var not in closed_vars:
            violations.append({
                "line": line,
                "message": f"Unclosed file handle: '{var}' opened without with-statement or close()",
                "variable": var,
            })

    return violations


def _is_open_call(call: ast.Call) -> bool:
    """Check if a call node is an open() call (built-in or io.open)."""
    if isinstance(call.func, ast.Name) and call.func.id == "open":
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "open":
        return True
    return False
