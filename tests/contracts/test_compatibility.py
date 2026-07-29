from pathlib import Path

import pytest
from pydantic import ValidationError

from sqltrace.contracts.compatibility import CompatibilityEntry, CompatibilityMatrix, CompatibilityStatus

_CURRENT = CompatibilityEntry(
    contract_id="CTR-RUN-001", version="1.0.0", current=True, readable=True,
    writable=True, invalidates_stages=[], lossless=True, requires_revalidation=False,
)
def test_unknown_incompatible_version_is_quarantined() -> None:
    legacy = CompatibilityEntry(contract_id="CTR-RUN-001", version="0.1.0", current=False, readable=True, writable=False, migrator=None, recompute_required=False, invalidates_stages=["run"], lossless=False, requires_revalidation=True)
    matrix = CompatibilityMatrix(entries=[legacy, _CURRENT])
    result = matrix.check("CTR-RUN-001", "9.0.0")
    assert result.status is CompatibilityStatus.QUARANTINED


def test_malformed_compatibility_entry_is_rejected() -> None:
    with pytest.raises(ValidationError):
        CompatibilityEntry(contract_id="CTR-RUN-001", version="bad", current=True, readable=True, writable=True, invalidates_stages=["run"], lossless=True)


def test_compatibility_serialization_is_deterministic() -> None:
    matrix = CompatibilityMatrix(entries=[])
    assert matrix.to_json() == matrix.to_json()

def test_authoritative_legacy_run_spec_is_migratable() -> None:
    matrix = CompatibilityMatrix.from_json(str(Path(__file__).parents[2] / "contracts" / "compatibility-matrix.json"))
    result = matrix.check("CTR-RUN-001", "0.1.0")
    assert result.status is CompatibilityStatus.MIGRATABLE
    assert result.reason == "LEGACY_RUN_SPEC_MIGRATABLE"
    assert result.invalidates_stages == (
        "snapshot", "inventory", "structural_scan", "unitization", "static_analysis",
        "semantic_analysis", "normalization", "resolution", "sql_discovery",
        "conversion_projection", "artifact_generation",
    )

def test_authoritative_request_has_no_legacy_entry() -> None:
    matrix = CompatibilityMatrix.from_json(str(Path(__file__).parents[2] / "contracts" / "compatibility-matrix.json"))
    assert not any(item.contract_id == "CTR-RQR-001" and not item.current for item in matrix.entries)
