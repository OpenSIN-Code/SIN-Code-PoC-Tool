"""Clean code without violations."""

import os
from typing import List


def safe(a: List[int]):
    if a is None:
        return 0
    return 1


def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def handle_error():
    try:
        risky()
    except ValueError:
        pass
