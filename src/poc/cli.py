"""Typer CLI for PoC — Proof-of-Correctness.

Docs: cli.doc.md
"""

import json
import sys
from pathlib import Path
from typing import Optional

import typer

from poc.verifier import verify_file, verify_directory

app = typer.Typer(help="PoC — Proof-of-Correctness: verify code invariants")


@app.callback()
def main_callback() -> None:
    """PoC — Proof-of-Correctness."""
    pass


@app.command()
def verify(
    target: str = typer.Argument(..., help="File or directory to verify"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output JSON file"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Config file (not yet implemented)"),
) -> None:
    """Verify code invariants in a file or directory.

    Walks the AST and applies rules to detect common bugs and anti-patterns.
    """
    target_path = Path(target)

    if target_path.is_file():
        result = verify_file(str(target_path))
        results = [result]
    elif target_path.is_dir():
        results = verify_directory(str(target_path))
    else:
        typer.echo(f"Error: target not found: {target_path}", err=True)
        raise typer.Exit(1)

    # Aggregate summary
    total_checks = sum(len(r["checks"]) for r in results)
    failed_checks = sum(1 for r in results for c in r["checks"] if not c["pass"])
    passed_checks = total_checks - failed_checks

    report = {
        "results": results,
        "summary": {
            "files": len(results),
            "total_checks": total_checks,
            "passed": passed_checks,
            "failed": failed_checks,
        },
    }

    json_out = json.dumps(report, indent=2, ensure_ascii=False)
    if output:
        Path(output).write_text(json_out, encoding="utf-8")
        typer.echo(f"Report written to {output}")
    else:
        typer.echo(json_out)

    if failed_checks > 0:
        raise typer.Exit(1)


def main() -> None:
    """Entry point for the poc CLI."""
    app()


if __name__ == "__main__":
    main()
