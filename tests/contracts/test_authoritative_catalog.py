import pytest

from sqltrace.contracts.registry import (
    AUTHORITATIVE_R1_CATALOG,
    ContractDescriptor,
    ContractRegistry,
    validate_authoritative_catalog,
)


def test_authoritative_catalog_contains_normative_public_contracts() -> None:
    registry = ContractRegistry(contracts=list(AUTHORITATIVE_R1_CATALOG.public_contracts), embedded=list(AUTHORITATIVE_R1_CATALOG.embedded_contracts))
    assert validate_authoritative_catalog(registry) is registry


def test_missing_public_contract_fails_deterministically() -> None:
    contracts = list(AUTHORITATIVE_R1_CATALOG.public_contracts)[1:]
    with pytest.raises(ValueError, match="missing authoritative public contract"):
        validate_authoritative_catalog(ContractRegistry(contracts=contracts, embedded=list(AUTHORITATIVE_R1_CATALOG.embedded_contracts)))


def test_missing_embedded_schema_fails_deterministically() -> None:
    embedded = list(AUTHORITATIVE_R1_CATALOG.embedded_contracts)[1:]
    with pytest.raises(ValueError, match="missing authoritative embedded contract"):
        validate_authoritative_catalog(ContractRegistry(contracts=list(AUTHORITATIVE_R1_CATALOG.public_contracts), embedded=embedded))


def test_unknown_public_schema_fails_deterministically() -> None:
    unknown = ContractDescriptor(contract_id="CTR-UNK-001", name="Unknown", family="state", version="1.0.0", owner_path="sqltrace.unknown.Unknown")
    with pytest.raises(ValueError, match="unknown authoritative public contract"):
        validate_authoritative_catalog(ContractRegistry(contracts=[*AUTHORITATIVE_R1_CATALOG.public_contracts, unknown], embedded=list(AUTHORITATIVE_R1_CATALOG.embedded_contracts)))


def test_equivalent_catalogs_have_identical_bytes() -> None:
    first = ContractRegistry(contracts=list(AUTHORITATIVE_R1_CATALOG.public_contracts), embedded=list(AUTHORITATIVE_R1_CATALOG.embedded_contracts))
    second = ContractRegistry(contracts=list(reversed(AUTHORITATIVE_R1_CATALOG.public_contracts)), embedded=list(reversed(AUTHORITATIVE_R1_CATALOG.embedded_contracts)))
    assert first.to_json().encode() == second.to_json().encode()


def test_authoritative_descriptor_metadata_must_match() -> None:
    altered = list(AUTHORITATIVE_R1_CATALOG.public_contracts)
    altered[0] = altered[0].model_copy(update={"family": "altered"})
    registry = ContractRegistry(contracts=altered, embedded=list(AUTHORITATIVE_R1_CATALOG.embedded_contracts))
    with pytest.raises(ValueError, match="descriptor mismatch"):
        validate_authoritative_catalog(registry)
def test_authoritative_embedded_metadata_must_match() -> None:
    altered = list(AUTHORITATIVE_R1_CATALOG.embedded_contracts)
    altered[0] = altered[0].model_copy(update={"owner_contract_id": "CTR-RUN-001"})
    registry = ContractRegistry.model_construct(
        contracts=list(AUTHORITATIVE_R1_CATALOG.public_contracts), embedded=altered
    )
    with pytest.raises(ValueError, match="embedded descriptor mismatch"):
        validate_authoritative_catalog(registry)
