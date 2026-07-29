import pytest
from pydantic import ValidationError

from sqltrace.contracts.registry import ContractDescriptor, ContractRegistry, EmbeddedDescriptor


def descriptor(contract_id: str = "CTR-RUN-001", owner_path: str = "sqltrace.contracts.run.RunSpec") -> ContractDescriptor:
    return ContractDescriptor(
        contract_id=contract_id,
        name="RunSpec",
        family="state",
        version="1.0.0",
        owner_path=owner_path,
    )


def test_registry_serialization_is_canonical_and_sorted() -> None:
    registry = ContractRegistry(contracts=[descriptor("CTR-ZZZ-001", "sqltrace.contracts.zzz.Zzz"), descriptor()])
    assert registry.to_json() == registry.to_json()
    assert registry.contracts[0].contract_id == "CTR-ZZZ-001"
    assert registry.canonical()["contracts"][0]["contract_id"] == "CTR-RUN-001"


def test_duplicate_contract_id_and_owner_are_rejected() -> None:
    with pytest.raises(ValidationError, match="duplicate contract_id"):
        ContractRegistry(contracts=[descriptor(), descriptor(owner_path="other.Path")])
    with pytest.raises(ValidationError, match="duplicate owner_path"):
        ContractRegistry(contracts=[descriptor(), descriptor("CTR-OTH-001")])


def test_embedded_contract_requires_owner_and_hash_name() -> None:
    with pytest.raises(ValidationError, match="CONTRACT_ID#TypeName"):
        ContractRegistry(contracts=[descriptor()], embedded=[EmbeddedDescriptor(name="RunSpec", owner_contract_id="CTR-RUN-001")])
    with pytest.raises(ValidationError, match="prefix must match owner"):
        ContractRegistry(contracts=[descriptor()], embedded=[EmbeddedDescriptor(name="CTR-OTH-001#Nested", owner_contract_id="CTR-RUN-001")])
