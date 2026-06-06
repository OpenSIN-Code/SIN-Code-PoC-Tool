"""Intentionally bad code with all PoC violations."""

from os import *  # wildcard import


def risky(a=[]):  # mutable default
    try:
        f = open("tmp.txt")  # unclosed file
        if a == None:  # == None
            return 42
        return "bad"  # inconsistent return types
    except:
        pass


def another_bad(b={}):
    if b is not None:
        return []
    return {}
