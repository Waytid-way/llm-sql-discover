from pathlib import Path

import pytest
from pydantic import ValidationError

from sqltrace.contracts.compatibility import CompatibilityEntry, CompatibilityMatrix
from sqltrace.contracts.meta import ContractMeta
from sqltrace.contracts.registry import ContractDescriptor, ContractRegistry


def test_contract_meta_rejects_malformed_version() -> None:
    with pytest.raises(ValidationError, match="semantic version"):
        ContractMeta(
            contract_id="CTR-RSN-001",
            contract_family="policy",
            contract_version="draft",
            producer="sqltrace",
            producer_version="0.1.0",
        )


def test_contract_descriptor_requires_contract_id_shape() -> None:
    with pytest.raises(ValidationError):
        ContractDescriptor(
            contract_id="wrong",
            name="RunSpec",
            family="state",
            version="1.0.0",
            owner_path="sqltrace.contracts.run.RunSpec",
        )


def test_compatibility_matrix_rejects_duplicate_entries() -> None:
    entry = CompatibilityEntry(
        contract_id="CTR-RUN-001",
        version="1.0.0",
        current=True,
        readable=True,
        writable=True,
        invalidates_stages=[],
        lossless=True,
        requires_revalidation=False,
    )
    with pytest.raises(ValidationError, match="duplicate"):
        CompatibilityMatrix(entries=[entry, entry])


def test_missing_registry_file_is_deterministic_error(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="invalid compatibility matrix"):
        CompatibilityMatrix.from_json(str(tmp_path / "missing.json"))
