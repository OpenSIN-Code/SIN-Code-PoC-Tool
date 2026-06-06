# PoC — Proof-of-Correctness

PoC is an automated code verifier that checks invariants by walking the Python AST. It catches common bugs and anti-patterns such as bare `except:` blocks, mutable default arguments, unclosed file handles, `== None` comparisons, wildcard imports, and inconsistent return types. It runs as a standalone CLI or integrates into CI pipelines (exit code 1 on any failure).
