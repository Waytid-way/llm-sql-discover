"""Stable Typer root shell for incrementally registered commands."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from .contracts.compatibility import CompatibilityMatrix
from .contracts.reason_codes import ReasonCodeRegistry
from .commands.registry import registry

app = typer.Typer(add_completion=False, no_args_is_help=True)
registry.discover()
registry.bind(app)

@app.callback()
def main() -> None:
    """Stable root command group."""
    return None


@app.command("registry-check")
def registry_check(
    compatibility_matrix: Path = typer.Argument(...),
    reason_codes: Path = typer.Argument(...),
) -> None:
    """Validate the authoritative compatibility and reason-code registries."""
    CompatibilityMatrix.from_json(str(compatibility_matrix))
    ReasonCodeRegistry.from_json(str(reason_codes))
    typer.echo(json.dumps({"status": "valid"}, sort_keys=True))


if __name__ == "__main__":
    app()
