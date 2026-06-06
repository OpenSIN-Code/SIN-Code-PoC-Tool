"""Rule: detect bare `except:` blocks that catch everything.

Docs: bare_except.doc.md
"""

import ast
from typing import Any, Dict, List

RULE_NAME = "bare_except"


def check(tree: ast.AST, source: str) -> List[Dict[str, Any]]:
    """Find bare except handlers (no exception type specified)."""
    violations: List[Dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            violations.append({
                "line": node.lineno,
                "message": "Bare except: catches everything including KeyboardInterrupt and SystemExit",
            })
    return violations
