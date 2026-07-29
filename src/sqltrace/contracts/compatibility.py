"""Explicit contract compatibility declarations and quarantine results."""

from __future__ import annotations

from enum import Enum
import json
import re
from dataclasses import dataclass

from .run import RunSpec

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_CONTRACT_ID = re.compile(r"^CTR-[A-Z]{3}-\d{3}$")
_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class CompatibilityStatus(str, Enum):
    READABLE = "READABLE"
    WRITABLE = "WRITABLE"
    MIGRATABLE = "MIGRATABLE"
    RECOMPUTE_REQUIRED = "RECOMPUTE_REQUIRED"
    QUARANTINED = "QUARANTINED"


class CompatibilityEntry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    contract_id: str
    version: str
    current: bool = False
    readable: bool
    writable: bool
    migrator: str | None = None
    recompute_required: bool = False
    invalidates_stages: list[str]
    lossless: bool
    requires_revalidation: bool = False

    @field_validator("contract_id")
    @classmethod
    def valid_contract_id(cls, value: str) -> str:
        if not _CONTRACT_ID.fullmatch(value):
            raise ValueError("malformed contract_id")
        return value

    @field_validator("version")
    @classmethod
    def semantic_version(cls, value: str) -> str:
        if not _SEMVER.fullmatch(value):
            raise ValueError("invalid semantic version")
        return value

    @field_validator("invalidates_stages")
    @classmethod
    def normalized_invalidation(cls, value: list[str]) -> list[str]:
        if any(not stage.strip() for stage in value):
            raise ValueError("invalidation stages must contain non-empty values")
        return list(dict.fromkeys(value))
    @model_validator(mode="after")
    def validate_semantics(self) -> "CompatibilityEntry":
        if not self.readable and not self.writable and not self.migrator and not self.recompute_required:
            raise ValueError("compatibility path is required")
        if self.current and (not self.writable or self.migrator or self.recompute_required):
            raise ValueError("current version must be writable without migration")
        if self.current and self.invalidates_stages:
            raise ValueError("current version must declare empty invalidation stages")
        if not self.current and not self.invalidates_stages:
            raise ValueError("invalidation stages must be non-empty")
        if not self.lossless and not self.requires_revalidation:
            raise ValueError("lossy compatibility requires revalidation")
        if self.migrator and self.writable:
            raise ValueError("migrator cannot be attached to writable version")
        if self.recompute_required and self.migrator:
            raise ValueError("choose migrator or recomputation, not both")
        return self


class CompatibilityResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    contract_id: str
    version: str
    status: CompatibilityStatus
    reason: str
    invalidates_stages: tuple[str, ...] = ()


class CompatibilityMatrix(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    entries: list[CompatibilityEntry] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_unique_entries(self) -> "CompatibilityMatrix":
        keys = [(item.contract_id, item.version) for item in self.entries]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate compatibility entry")
        current_counts: dict[str, int] = {item.contract_id: 0 for item in self.entries}
        for item in self.entries:
            if item.current:
                current_counts[item.contract_id] += 1
        if any(count != 1 for count in current_counts.values()):
            raise ValueError("one current version per contract is required")
        return self

    def to_json(self) -> str:
        entries = sorted((item.model_dump(mode="json") for item in self.entries), key=lambda item: (item["contract_id"], item["version"]))
        return json.dumps({"entries": entries}, ensure_ascii=False, sort_keys=True, indent=2) + "\n"

    def check(self, contract_id: str, version: str) -> CompatibilityResult:
        entry = next((item for item in self.entries if item.contract_id == contract_id and item.version == version), None)
        if entry is None:
            return CompatibilityResult(contract_id=contract_id, version=version, status=CompatibilityStatus.QUARANTINED, reason="unknown incompatible contract version")
        if entry.migrator:
            status = CompatibilityStatus.MIGRATABLE
        elif entry.recompute_required:
            status = CompatibilityStatus.RECOMPUTE_REQUIRED
        elif entry.writable:
            status = CompatibilityStatus.WRITABLE
        elif entry.readable:
            status = CompatibilityStatus.READABLE
        else:
            status = CompatibilityStatus.QUARANTINED
        reason = "LEGACY_RUN_SPEC_MIGRATABLE" if entry.migrator == "legacy_run_spec_0_1_0_to_1_0_0" else "declared compatibility"
        return CompatibilityResult(contract_id=contract_id, version=version, status=status, reason=reason, invalidates_stages=tuple(entry.invalidates_stages))

    @classmethod
    def from_json(cls, path: str) -> "CompatibilityMatrix":
        try:
            with open(path, encoding="utf-8") as handle:
                return cls.model_validate(json.load(handle))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"invalid compatibility matrix: {path}") from exc



_LEGACY_INVALIDATES = (
    "snapshot", "inventory", "structural_scan", "unitization", "static_analysis",
    "semantic_analysis", "normalization", "resolution", "sql_discovery",
    "conversion_projection", "artifact_generation",
)
_LEGACY_PLACEHOLDERS = {"", "placeholder", "pending", "not-set", "not_set", "todo"}


@dataclass(frozen=True)
class LegacyMigrationResult:
    status: CompatibilityStatus
    reason: str
    run_spec: RunSpec | None
    invalidates_stages: tuple[str, ...] = _LEGACY_INVALIDATES
    lossless: bool = False
    requires_revalidation: bool = True


def migrate_legacy_run_spec(payload: dict[str, object]) -> LegacyMigrationResult:
    snapshot_id = payload.get("snapshot_id")
    if snapshot_id is not None and (
        not isinstance(snapshot_id, str)
        or snapshot_id.strip().casefold() not in _LEGACY_PLACEHOLDERS
    ):
        return LegacyMigrationResult(CompatibilityStatus.QUARANTINED, "LEGACY_SNAPSHOT_ID_UNVERIFIABLE", None)
    migrated = dict(payload)
    migrated.pop("snapshot_id", None)
    migrated["contract_version"] = "1.0.0"
    run_spec = RunSpec.model_validate(migrated)
    return LegacyMigrationResult(CompatibilityStatus.MIGRATABLE, "LEGACY_RUN_SPEC_MIGRATABLE", run_spec)
__all__ = ["CompatibilityEntry", "CompatibilityMatrix", "CompatibilityResult", "CompatibilityStatus", "LegacyMigrationResult", "migrate_legacy_run_spec"]
