import pytest
from pydantic import ValidationError

from sqltrace.contracts.registry import ContractDescriptor, ContractRegistry, EmbeddedDescriptor


def public(contract_id: str) -> ContractDescriptor:
    return ContractDescriptor(contract_id=contract_id, name="Nested", family="state", version="1.0.0", owner_path=f"sqltrace.{contract_id}")


def test_embedded_prefix_must_match_owner_contract() -> None:
    with pytest.raises(ValidationError, match="owner contract"):
        ContractRegistry(contracts=[public("CTR-AAA-001"), public("CTR-BBB-001")], embedded=[EmbeddedDescriptor(name="CTR-AAA-001#Nested", owner_contract_id="CTR-BBB-001")])


def test_duplicate_embedded_names_are_rejected() -> None:
    item = EmbeddedDescriptor(name="CTR-AAA-001#Nested", owner_contract_id="CTR-AAA-001")
    with pytest.raises(ValidationError, match="duplicate embedded"):
        ContractRegistry(contracts=[public("CTR-AAA-001")], embedded=[item, item])


def test_malformed_or_unregistered_embedded_prefix_is_rejected() -> None:
    with pytest.raises(ValidationError, match="CONTRACT_ID#TypeName"):
        ContractRegistry(contracts=[public("CTR-AAA-001")], embedded=[EmbeddedDescriptor(name="BAD#Nested", owner_contract_id="CTR-AAA-001")])
    with pytest.raises(ValidationError, match="unregistered embedded"):
        ContractRegistry(contracts=[public("CTR-AAA-001")], embedded=[EmbeddedDescriptor(name="CTR-BBB-001#Nested", owner_contract_id="CTR-BBB-001")])


def test_amendment_embedded_ownership_is_complete() -> None:
    from sqltrace.contracts.registry import AUTHORITATIVE_R1_CATALOG

    names = {item.name for item in AUTHORITATIVE_R1_CATALOG.embedded_contracts}
    assert {
        "CTR-FSB-001#StructuralOutline",
        "CTR-FSB-001#FileScopedFact",
        "CTR-FSB-001#SfcBlockMap",
        "CTR-LRS-001#SemanticSymbolFinding",
        "CTR-LRS-001#AnalysisWarning",
        "CTR-LRS-001#TokenUsage",
        "CTR-PRJ-001#ConversionChange",
        "CTR-PRJ-001#ConversionDiagnostic",
        "CTR-PRJ-001#UnsupportedConstruct",
    } <= names
