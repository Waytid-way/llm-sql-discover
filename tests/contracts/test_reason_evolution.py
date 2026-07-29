import pytest
from pydantic import ValidationError

from sqltrace.contracts.reason_codes import ReasonCode, ReasonCodeRegistry


def code(**overrides: object) -> ReasonCode:
    data: dict[str, object] = {
        "code": "POLICY.TEST",
        "namespace": "POLICY",
        "owner_contract": "CTR-RSN-001",
        "severity": "INFO",
        "terminal_behavior": "NON_TERMINAL",
        "description": "test reason",
        "introduced_in": "1.0.0",
    }
    data.update(overrides)
    return ReasonCode(**data)


def test_code_prefix_matches_namespace() -> None:
    with pytest.raises(ValidationError, match="prefix"):
        code(code="SQL.TEST")


def test_description_is_non_empty() -> None:
    with pytest.raises(ValidationError, match="description"):
        code(description="")


def test_replacement_requires_deprecation() -> None:
    with pytest.raises(ValidationError, match="deprecated"):
        code(replacement="POLICY.NEW")


def test_deprecated_version_cannot_precede_introduction() -> None:
    with pytest.raises(ValidationError, match="deprecated_in"):
        code(deprecated_in="0.9.0", introduced_in="1.0.0", replacement="POLICY.NEW")


def test_same_major_removal_fails() -> None:
    current = ReasonCodeRegistry(codes=[code()])
    with pytest.raises(ValueError, match="removed"):
        current.assert_compatible_with(ReasonCodeRegistry(codes=[]), "1.0.0")


def test_same_major_meaning_repurpose_fails() -> None:
    current = ReasonCodeRegistry(codes=[code()])
    changed = ReasonCodeRegistry(codes=[code(severity="ERROR")])
    with pytest.raises(ValueError, match="repurposed"):
        current.assert_compatible_with(changed, "1.0.0")
