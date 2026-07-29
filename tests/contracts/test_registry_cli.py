import subprocess
import sys
from pathlib import Path

from sqltrace.contracts.registry import AUTHORITATIVE_R1_CATALOG, ContractRegistry, validate_authoritative_catalog

_WORKTREE = Path(__file__).resolve().parents[2]


def test_registry_module_check_validates_authoritative_files() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sqltrace.contracts.registry",
            "--check",
            str(_WORKTREE / "contracts" / "compatibility-matrix.json"),
            str(_WORKTREE / "contracts" / "reason-codes.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=_WORKTREE,
        env={**__import__("os").environ, "PYTHONPATH": str(_WORKTREE / "src")},
    )
    assert result.returncode == 0, result.stderr
    assert '"status": "valid"' in result.stdout

def test_authoritative_catalog_is_checked_as_part_of_registry_contract() -> None:
    registry = ContractRegistry(contracts=list(AUTHORITATIVE_R1_CATALOG.public_contracts), embedded=list(AUTHORITATIVE_R1_CATALOG.embedded_contracts))
    assert validate_authoritative_catalog(registry) is registry
