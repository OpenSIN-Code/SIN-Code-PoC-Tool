# `none_comparison.doc.md`

Detects `== None` and `!= None` comparisons.

## Rationale
`is None` is the idiomatic, faster, and semantically correct way to check for
None because None is a singleton.
