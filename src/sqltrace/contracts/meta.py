"""Lifecycle envelopes and shared contract metadata."""

from __future__ import annotations

from datetime import datetime, timezone
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
_SENTINELS = {"", "unknown", "placeholder", "sentinel", "pending", "not-set", "not_set", "todo", "null", "none"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_identity(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty identity")
    if value.strip().casefold() in _SENTINELS:
        raise ValueError(f"{field} cannot use a placeholder or sentinel identity")
    return value


class ContractMeta(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    contract_id: str
    contract_family: str
    contract_version: str
    producer: str
    producer_version: str
    created_at: str = Field(default_factory=utc_now)

    @field_validator("contract_id", "contract_family", "producer")
    @classmethod
    def non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("metadata values must be non-empty")
        return value

    @field_validator("contract_version", "producer_version")
    @classmethod
    def semantic_version(cls, value: str) -> str:
        if not _SEMVER.fullmatch(value):
            raise ValueError("version must use MAJOR.MINOR.PATCH semantic versioning")
        return value


class BootstrapEnvelope(ContractMeta):
    correlation_id: str

    @field_validator("correlation_id")
    @classmethod
    def valid_correlation_id(cls, value: str) -> str:
        return validate_identity(value, "correlation_id")


class RunEnvelope(BootstrapEnvelope):
    run_id: str

    @field_validator("run_id")
    @classmethod
    def valid_run_id(cls, value: str) -> str:
        return validate_identity(value, "run_id")


class SnapshotEnvelope(RunEnvelope):
    snapshot_id: str

    @field_validator("snapshot_id")
    @classmethod
    def valid_snapshot_id(cls, value: str) -> str:
        return validate_identity(value, "snapshot_id")


__all__ = ["BootstrapEnvelope", "ContractMeta", "RunEnvelope", "SnapshotEnvelope", "utc_now"]
