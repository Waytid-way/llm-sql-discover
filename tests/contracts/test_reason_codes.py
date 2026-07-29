import pytest
from pydantic import ValidationError

from sqltrace.contracts.reason_codes import ReasonCode, ReasonCodeRegistry


def code(code: str = "POLICY.TEST", namespace: str = "POLICY") -> ReasonCode:
    return ReasonCode(
        code=code,
        namespace=namespace,
        owner_contract="CTR-RSN-001",
        severity="INFO",
        terminal_behavior="NON_TERMINAL",
        description="test reason",
        introduced_in="1.0.0",
    )


def test_reason_codes_are_sorted_and_canonical() -> None:
    registry = ReasonCodeRegistry(codes=[code("POLICY.Z"), code()])
    assert [item.code for item in registry.codes] == ["POLICY.TEST", "POLICY.Z"]
    assert registry.to_json() == registry.to_json()


def test_duplicate_codes_and_unknown_namespace_are_rejected() -> None:
    with pytest.raises(ValidationError, match="duplicate reason code"):
        ReasonCodeRegistry(codes=[code(), code()])
    with pytest.raises(ValidationError, match="unknown namespace"):
        ReasonCodeRegistry(codes=[code("NOPE.TEST", "NOPE")])
