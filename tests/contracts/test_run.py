import pytest
from pydantic import ValidationError

from sqltrace.contracts.compatibility import CompatibilityStatus, migrate_legacy_run_spec
from sqltrace.contracts.run import RunRequest, RunSpec


LEGACY_BASE = {
    "contract_id": "CTR-RUN-001",
    "contract_family": "policy/state",
    "contract_version": "0.1.0",
    "producer": "sqltrace",
    "producer_version": "0.1.0",
    "correlation_id": "corr-1",
    "run_id": "run-1",
    "repository_root": "repo",
}


@pytest.mark.parametrize("snapshot_id", [None, "", "  ", "placeholder", "PENDING", "not-set", "not_set", "todo"])
def test_legacy_placeholder_snapshot_is_removed_without_generation(snapshot_id: object) -> None:
    payload = dict(LEGACY_BASE)
    if snapshot_id is not None:
        payload["snapshot_id"] = snapshot_id
    result = migrate_legacy_run_spec(payload)
    assert result.status is CompatibilityStatus.MIGRATABLE
    assert result.reason == "LEGACY_RUN_SPEC_MIGRATABLE"
    assert result.run_spec is not None
    assert not hasattr(result.run_spec, "snapshot_id")


@pytest.mark.parametrize("snapshot_id", ["unknown", "sentinel", "none", "null", "snapshot-1"])
def test_legacy_unverifiable_snapshot_is_quarantined(snapshot_id: str) -> None:
    result = migrate_legacy_run_spec({**LEGACY_BASE, "snapshot_id": snapshot_id})
    assert result.status is CompatibilityStatus.QUARANTINED
    assert result.reason == "LEGACY_SNAPSHOT_ID_UNVERIFIABLE"
    assert result.run_spec is None


def test_legacy_migration_preserves_invalidation_and_revalidation() -> None:
    result = migrate_legacy_run_spec(LEGACY_BASE)
    assert result.invalidates_stages == (
        "snapshot", "inventory", "structural_scan", "unitization", "static_analysis",
        "semantic_analysis", "normalization", "resolution", "sql_discovery",
        "conversion_projection", "artifact_generation",
    )
    assert result.lossless is False
    assert result.requires_revalidation is True


def test_legacy_identity_is_not_repaired() -> None:
    with pytest.raises(ValidationError):
        migrate_legacy_run_spec({**LEGACY_BASE, "run_id": "unknown"})


def base_meta() -> dict[str, str]:
    return {
        "contract_id": "CTR-RQR-001",
        "contract_family": "policy",
        "contract_version": "1.0.0",
        "producer": "sqltrace",
        "producer_version": "0.1.0",
        "correlation_id": "corr-1",
    }


def test_run_request_uses_bootstrap_identity_without_snapshot() -> None:
    request = RunRequest(**base_meta(), repository_root="repo", include_globs=["**/*"])
    assert request.correlation_id == "corr-1"
    assert not hasattr(request, "snapshot_id")


def test_run_spec_requires_run_identity_and_rejects_snapshot_identity() -> None:
    data = {
        **base_meta(),
        "contract_id": "CTR-RUN-001",
        "contract_family": "state",
        "run_id": "run-1",
        "repository_root": "repo",
    }
    spec = RunSpec(**data)
    assert spec.run_id == "run-1"
    with pytest.raises(ValidationError):
        RunSpec(**data, snapshot_id="snapshot-1")


def test_placeholder_snapshot_identity_is_rejected() -> None:
    with pytest.raises(ValidationError):
        RunRequest(**base_meta(), repository_root="repo", snapshot_id="placeholder")
