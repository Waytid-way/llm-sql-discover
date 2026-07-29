"""Machine-readable reason-code ownership and evolution registry."""

from __future__ import annotations

import json
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_ALLOWED_NAMESPACES = {"SNAPSHOT", "SOURCE", "ANALYZER", "UNIT", "LLM", "NORMALIZATION", "RESOLVER", "SQL", "PROJECTION", "STATE", "EVENT", "POLICY", "BENCHMARK"}
_CONTRACT = re.compile(r"^CTR-[A-Z]{3}-\d{3}$")
_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
_CODE = re.compile(r"^[A-Z][A-Z0-9_]*\.[A-Z][A-Z0-9_]*$")


def _version(value: str) -> tuple[int, int, int]:
    if not _SEMVER.fullmatch(value):
        raise ValueError("invalid semantic version")
    return tuple(int(part) for part in value.split("."))


class ReasonCode(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    code: str
    namespace: str
    owner_contract: str
    severity: Literal["INFO", "WARNING", "ERROR", "CRITICAL"]
    terminal_behavior: Literal["TERMINAL", "NON_TERMINAL", "QUARANTINED"]
    description: str
    introduced_in: str
    deprecated_in: str | None = None
    replacement: str | None = None

    @field_validator("code")
    @classmethod
    def valid_code(cls, value: str) -> str:
        if not _CODE.fullmatch(value):
            raise ValueError("invalid reason code")
        return value

    @field_validator("namespace")
    @classmethod
    def known_namespace(cls, value: str) -> str:
        if value not in _ALLOWED_NAMESPACES:
            raise ValueError("unknown namespace")
        return value

    @field_validator("owner_contract")
    @classmethod
    def valid_owner(cls, value: str) -> str:
        if not _CONTRACT.fullmatch(value):
            raise ValueError("malformed owner contract")
        return value

    @field_validator("description")
    @classmethod
    def non_empty_description(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("description must be non-empty")
        return value

    @field_validator("introduced_in", "deprecated_in")
    @classmethod
    def valid_version(cls, value: str | None) -> str | None:
        if value is not None:
            _version(value)
        return value

    @field_validator("replacement")
    @classmethod
    def valid_replacement(cls, value: str | None) -> str | None:
        if value is not None and not _CODE.fullmatch(value):
            raise ValueError("invalid replacement reason code")
        return value

    @model_validator(mode="after")
    def validate_evolution(self) -> "ReasonCode":
        prefix, _ = self.code.split(".", 1)
        if prefix != self.namespace:
            raise ValueError("reason code prefix must match namespace")
        if self.replacement is not None and self.deprecated_in is None:
            raise ValueError("replacement requires deprecated_in")
        if self.deprecated_in is not None:
            if _version(self.deprecated_in) < _version(self.introduced_in):
                raise ValueError("deprecated_in cannot precede introduced_in")
            if self.replacement is None:
                raise ValueError("deprecated reason code requires replacement")
        if self.replacement == self.code:
            raise ValueError("replacement cannot equal deprecated code")
        return self


class ReasonCodeRegistry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    codes: list[ReasonCode] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_unique_codes(self) -> "ReasonCodeRegistry":
        values = [item.code for item in self.codes]
        if len(values) != len(set(values)):
            raise ValueError("duplicate reason code")
        self.codes.sort(key=lambda item: item.code)
        return self

    def canonical(self) -> dict[str, object]:
        return {"codes": [item.model_dump(mode="json", exclude_none=True) for item in sorted(self.codes, key=lambda item: item.code)]}

    def to_json(self) -> str:
        return json.dumps(self.canonical(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"

    def assert_compatible_with(self, newer: "ReasonCodeRegistry", version: str) -> None:
        major = _version(version)[0]
        current = {item.code: item for item in self.codes}
        replacement = {item.code: item for item in newer.codes}
        for code, old in current.items():
            if code not in replacement:
                if old.deprecated_in is None or _version(old.deprecated_in)[0] == major:
                    raise ValueError(f"reason code removed within same major: {code}")
                continue
            new = replacement[code]
            if (old.namespace, old.owner_contract, old.severity, old.terminal_behavior) != (new.namespace, new.owner_contract, new.severity, new.terminal_behavior):
                raise ValueError(f"reason code repurposed within same major: {code}")

    @classmethod
    def from_json(cls, path: str) -> "ReasonCodeRegistry":
        try:
            with open(path, encoding="utf-8") as handle:
                return cls.model_validate_json(handle.read())
        except (OSError, ValueError) as exc:
            raise ValueError(f"invalid reason-code registry: {path}") from exc


__all__ = ["ReasonCode", "ReasonCodeRegistry"]
