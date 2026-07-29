from pathlib import Path

from typer.testing import CliRunner

from sqltrace.cli import app
from sqltrace.commands.registry import CommandRegistry

_WORKTREE = Path(__file__).resolve().parents[2]


def test_later_command_registers_without_root_shell_edit() -> None:
    registry = CommandRegistry()

    @registry.command("future")
    def future_command() -> str:
        return "future"

    assert registry.get("future") is future_command


def test_duplicate_command_is_rejected() -> None:
    registry = CommandRegistry()

    @registry.command("same")
    def first() -> None:
        pass

    try:
        registry.command("same")(lambda: None)
    except ValueError as exc:
        assert "duplicate command" in str(exc)
    else:
        raise AssertionError("duplicate command was accepted")


def test_registry_check_command_is_machine_readable() -> None:
    result = CliRunner().invoke(app, ["registry-check", str(_WORKTREE / "contracts/compatibility-matrix.json"), str(_WORKTREE / "contracts/reason-codes.json")])
    assert result.exit_code == 0, result.output
    assert "valid" in result.stdout


def test_future_command_module_is_discovered_without_root_edit(tmp_path: Path) -> None:
    import importlib
    import sys

    import sqltrace.cli as cli
    import sqltrace.commands as commands

    module_dir = tmp_path / "future_commands"
    module_dir.mkdir()
    (module_dir / "future_command.py").write_text(
        "from sqltrace.commands.registry import registry\n"
        "import typer\n"
        "@registry.command('future')\n"
        "def future() -> None:\n"
        "    typer.echo('future-output')\n",
        encoding="utf-8",
    )
    commands.__path__.append(str(module_dir))
    sys.modules.pop("sqltrace.commands.future_command", None)
    importlib.reload(cli)
    result = CliRunner().invoke(cli.app, ["future"])
    assert result.exit_code == 0, result.stdout
    assert result.stdout == "future-output\n"
