import pytest
from pydantic import ValidationError

from sqltrace.contracts.compatibility import CompatibilityEntry, CompatibilityMatrix, CompatibilityStatus


def entry(**overrides: object) -> CompatibilityEntry:
    data: dict[str, object] = {
        "contract_id": "CTR-RUN-001",
        "version": "1.0.0",
        "current": True,
        "readable": True,
        "writable": True,
        "migrator": None,
        "recompute_required": False,
        "invalidates_stages": [],
        "lossless": True,
        "requires_revalidation": False,
    }
    data.update(overrides)
    return CompatibilityEntry(**data)


def test_current_writable_version_is_valid() -> None:
    assert CompatibilityMatrix(entries=[entry()]).check("CTR-RUN-001", "1.0.0").status is CompatibilityStatus.WRITABLE


def test_readable_only_version_is_valid() -> None:
    value = entry(current=False, version="0.9.0", writable=False, invalidates_stages=["run"])
    assert CompatibilityMatrix(entries=[value, entry()]).check("CTR-RUN-001", "0.9.0").status is CompatibilityStatus.READABLE


def test_migratable_legacy_precedes_readable() -> None:
    value = entry(current=False, version="0.9.0", migrator="migrate_run_v0", writable=False, invalidates_stages=["run"])
    assert CompatibilityMatrix(entries=[value, entry()]).check("CTR-RUN-001", "0.9.0").status is CompatibilityStatus.MIGRATABLE


def test_recomputation_required_legacy_is_explicit() -> None:
    value = entry(current=False, version="0.9.0", readable=False, writable=False, recompute_required=True, invalidates_stages=["run"])
    assert CompatibilityMatrix(entries=[value, entry()]).check("CTR-RUN-001", "0.9.0").status is CompatibilityStatus.RECOMPUTE_REQUIRED


@pytest.mark.parametrize(
    "overrides, message",
    [
        ({"readable": False, "writable": False, "migrator": None, "recompute_required": False}, "compatibility path"),
        ({"lossless": False, "requires_revalidation": False}, "lossy"),
        ({"current": True, "migrator": "bad-migrator"}, "current version"),
        ({"current": False, "invalidates_stages": []}, "invalidation"),
        ({"contract_id": "BAD-ID"}, "contract_id"),
    ],
)
def test_contradictory_compatibility_declarations_fail(overrides: dict[str, object], message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        entry(**overrides)


def test_omitted_invalidation_stages_are_rejected() -> None:
    data = {
        "contract_id": "CTR-RUN-001",
        "version": "1.0.0",
        "current": True,
        "readable": True,
        "writable": True,
        "lossless": True,
    }
    with pytest.raises(ValidationError, match="invalidates_stages"):
        CompatibilityEntry(**data)


def test_current_entry_allows_explicit_empty_invalidation_stages() -> None:
    assert entry(invalidates_stages=[]) is not None


def test_matrix_rejects_multiple_current_versions() -> None:
    first = entry(version="1.0.0")
    second = entry(version="2.0.0")
    with pytest.raises(ValidationError, match="one current version"):
        CompatibilityMatrix(entries=[first, second])


def test_matrix_rejects_missing_current_version() -> None:
    legacy = entry(current=False, version="0.1.0", writable=False, migrator="migrate", invalidates_stages=["run"], lossless=False, requires_revalidation=True)
    with pytest.raises(ValidationError, match="one current version"):
        CompatibilityMatrix(entries=[legacy])

def test_unknown_version_is_quarantined() -> None:
    result = CompatibilityMatrix(entries=[entry()]).check("CTR-RUN-001", "9.0.0")
    assert result.status is CompatibilityStatus.QUARANTINED
