"""Deterministic contract ownership registry and atomic JSON writer."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Callable

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .meta import ContractMeta

_CONTRACT_ID = re.compile(r"^CTR-[A-Z]{3}-\d{3}$")
_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ContractDescriptor(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    contract_id: str
    name: str
    family: str
    version: str
    owner_path: str
    embedded: bool = False

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

    @field_validator("name", "family", "owner_path")
    @classmethod
    def non_empty(cls, value: str) -> str:
        if not value.strip() or ".." in value or "\\" in value:
            raise ValueError("descriptor values must be non-empty and normalized")
        return value


class EmbeddedDescriptor(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str
    owner_contract_id: str

    @field_validator("name")
    @classmethod
    def qualified_name(cls, value: str) -> str:
        if "#" not in value or value.startswith("#") or value.endswith("#"):
            raise ValueError("embedded name must use CONTRACT_ID#TypeName")
        prefix, type_name = value.split("#", 1)
        if not _CONTRACT_ID.fullmatch(prefix) or not type_name or "#" in type_name:
            raise ValueError("embedded name must use CONTRACT_ID#TypeName")
        return value

    @field_validator("owner_contract_id")
    @classmethod
    def valid_owner_id(cls, value: str) -> str:
        if not _CONTRACT_ID.fullmatch(value):
            raise ValueError("malformed owner contract")
        return value


class ContractRegistry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    metadata: ContractMeta | None = None
    contracts: list[ContractDescriptor] = Field(default_factory=list)
    embedded: list[EmbeddedDescriptor] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_ownership(self) -> "ContractRegistry":
        ids = [item.contract_id for item in self.contracts]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate contract_id")
        owners = [item.owner_path for item in self.contracts]
        if len(owners) != len(set(owners)):
            raise ValueError("duplicate owner_path")
        embedded_names = [item.name for item in self.embedded]
        if len(embedded_names) != len(set(embedded_names)):
            raise ValueError("duplicate embedded name")
        public_ids = set(ids)
        for item in self.embedded:
            prefix, _ = item.name.split("#", 1)
            if prefix != item.owner_contract_id:
                raise ValueError("embedded prefix must match owner contract")
            if prefix not in public_ids:
                raise ValueError(f"unregistered embedded contract: {prefix}")
            if item.owner_contract_id not in public_ids:
                raise ValueError(f"unregistered owner contract: {item.owner_contract_id}")
        return self

    def canonical(self) -> dict[str, object]:
        data = self.model_dump(mode="json", exclude_none=True)
        data["contracts"] = sorted(data["contracts"], key=lambda item: item["contract_id"])
        data["embedded"] = sorted(data["embedded"], key=lambda item: item["name"])
        return data

    def to_json(self) -> str:
        return json.dumps(self.canonical(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"

    @classmethod
    def from_json(cls, path: Path) -> "ContractRegistry":
        try:
            return cls.model_validate_json(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"invalid contract registry: {path}") from exc


# Public IDs are the union of the normative core registry and A2 additions.
_R1_PUBLIC_SPECS = (
    ("CTR-RQR-001", "RunRequest", "policy"),
    ("CTR-RUN-001", "RunSpec", "policy/state"),
    ("CTR-SNP-001", "SnapshotManifest", "snapshot"),
    ("CTR-FIL-001", "FileInstance", "identity"),
    ("CTR-EVD-001", "EvidenceAnchor", "source-anchor"),
    ("CTR-UNT-001", "AnalysisUnit", "analysis-unit"),
    ("CTR-STF-001", "StaticFactBundle", "static-facts"),
    ("CTR-CAP-001", "AnalyzerCapability", "policy"),
    ("CTR-FSB-001", "FileStructureBundle", "static-facts"),
    ("CTR-DEC-001", "AnalysisDecision", "policy"),
    ("CTR-LRQ-001", "FileAnalysisRequest", "llm-analysis"),
    ("CTR-LRS-001", "FileAnalysisResult", "llm-analysis"),
    ("CTR-FND-001", "FindingBase", "findings"),
    ("CTR-FRQ-001", "FrontendRequestFinding", "findings"),
    ("CTR-BEP-001", "BackendEndpointFinding", "findings"),
    ("CTR-DBO-001", "DatabaseOperationFinding", "findings"),
    ("CTR-UNR-001", "UnresolvedReference", "findings"),
    ("CTR-EDG-001", "ResolverEdge", "resolver"),
    ("CTR-CVR-001", "ChainVerificationResult", "resolver"),
    ("CTR-CHN-001", "ExecutionChain", "chain"),
    ("CTR-RRC-001", "ResolvedRequestContract", "chain"),
    ("CTR-SQL-001", "SqlFinding", "sql-discovery"),
    ("CTR-SCM-001", "SchemaContext", "sql-discovery"),
    ("CTR-TRP-001", "TargetRuntimeProfile", "conversion-projection"),
    ("CTR-PRJ-001", "SqlConversionProjection", "conversion-projection"),
    ("CTR-EVT-001", "PipelineEvent", "pipeline-events"),
    ("CTR-ART-001", "ArtifactManifest", "artifacts"),
    ("CTR-BMK-001", "BenchmarkCase", "benchmark"),
    ("CTR-SQC-001", "SqlCandidate", "sql-discovery"),
    ("CTR-SNR-001", "SqlNormalizationResult", "sql-discovery"),
    ("CTR-NDB-001", "NoDatabaseOperationFinding", "findings"),
    ("CTR-OUT-001", "OutboxRecord", "pipeline-events"),
    ("CTR-ESM-001", "EventSegmentManifest", "pipeline-events"),
    ("CTR-BMM-001", "BenchmarkManifest", "benchmark"),
    ("CTR-RSN-001", "ReasonCodeRegistry", "policy"),
)

_R1_EMBEDDED_SPECS = (
    ("CTR-STF-001#SymbolFact", "CTR-STF-001"),
    ("CTR-STF-001#CallFact", "CTR-STF-001"),
    ("CTR-STF-001#RouteFact", "CTR-STF-001"),
    ("CTR-STF-001#HttpCallFact", "CTR-STF-001"),
    ("CTR-STF-001#DatabaseCallFact", "CTR-STF-001"),
    ("CTR-STF-001#DtoPropertyFact", "CTR-STF-001"),
    ("CTR-STF-001#DiRegistrationFact", "CTR-STF-001"),
    ("CTR-FSB-001#StructuralOutline", "CTR-FSB-001"),
    ("CTR-FSB-001#FileScopedFact", "CTR-FSB-001"),
    ("CTR-FSB-001#SfcBlockMap", "CTR-FSB-001"),
    ("CTR-LRS-001#SemanticSymbolFinding", "CTR-LRS-001"),
    ("CTR-LRS-001#AnalysisWarning", "CTR-LRS-001"),
    ("CTR-LRS-001#TokenUsage", "CTR-LRS-001"),
    ("CTR-CHN-001#MissingLink", "CTR-CHN-001"),
    ("CTR-RRC-001#ResolvedFieldBinding", "CTR-RRC-001"),
    ("CTR-RRC-001#UnresolvedField", "CTR-RRC-001"),
    ("CTR-SQL-001#SqlFragment", "CTR-SQL-001"),
    ("CTR-SQL-001#SqlParameterBinding", "CTR-SQL-001"),
    ("CTR-PRJ-001#ConversionChange", "CTR-PRJ-001"),
    ("CTR-PRJ-001#ConversionDiagnostic", "CTR-PRJ-001"),
    ("CTR-PRJ-001#UnsupportedConstruct", "CTR-PRJ-001"),
)


@dataclass(frozen=True)
class AuthoritativeCatalog:
    public_contracts: tuple[ContractDescriptor, ...]
    embedded_contracts: tuple[EmbeddedDescriptor, ...]


def _public_descriptors() -> tuple[ContractDescriptor, ...]:
    return tuple(ContractDescriptor(contract_id=cid, name=name, family=family, version="1.0.0", owner_path=f"sqltrace.contracts.{name}") for cid, name, family in _R1_PUBLIC_SPECS)


def _embedded_descriptors() -> tuple[EmbeddedDescriptor, ...]:
    return tuple(EmbeddedDescriptor(name=name, owner_contract_id=owner) for name, owner in _R1_EMBEDDED_SPECS)


AUTHORITATIVE_R1_CATALOG = AuthoritativeCatalog(_public_descriptors(), _embedded_descriptors())


def validate_authoritative_catalog(registry: ContractRegistry) -> ContractRegistry:
    expected_public = {item.contract_id: item for item in AUTHORITATIVE_R1_CATALOG.public_contracts}
    actual_public = {item.contract_id: item for item in registry.contracts}
    for contract_id in expected_public.keys() - actual_public.keys():
        raise ValueError(f"missing authoritative public contract: {contract_id}")
    for contract_id in actual_public.keys() - expected_public.keys():
        raise ValueError(f"unknown authoritative public contract: {contract_id}")
    for contract_id, expected in expected_public.items():
        if actual_public[contract_id] != expected:
            raise ValueError(f"authoritative descriptor mismatch: {contract_id}")
    expected_embedded = {item.name: item for item in AUTHORITATIVE_R1_CATALOG.embedded_contracts}
    actual_embedded = {item.name: item for item in registry.embedded}
    for name in expected_embedded.keys() - actual_embedded.keys():
        raise ValueError(f"missing authoritative embedded contract: {name}")
    for name in actual_embedded.keys() - expected_embedded.keys():
        raise ValueError(f"unknown authoritative embedded contract: {name}")
    for name, expected in expected_embedded.items():
        if actual_embedded[name] != expected:
            raise ValueError(f"authoritative embedded descriptor mismatch: {name}")
    return registry


def write_atomic(path: Path, producer: Callable[[], str | bytes] | str | bytes) -> None:
    """Validate and publish bytes atomically, preserving prior output on failure."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        payload = producer() if callable(producer) else producer
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        if not isinstance(payload, bytes):
            raise TypeError("atomic payload must be bytes or str")
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.", delete=False) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, target)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def check_files(compatibility_matrix: Path, reason_codes: Path) -> None:
    """Validate authoritative R1 ownership plus compatibility and reason registries."""
    from .compatibility import CompatibilityMatrix
    from .reason_codes import ReasonCodeRegistry

    CompatibilityMatrix.from_json(str(compatibility_matrix))
    ReasonCodeRegistry.from_json(str(reason_codes))
    validate_authoritative_catalog(ContractRegistry(contracts=list(AUTHORITATIVE_R1_CATALOG.public_contracts), embedded=list(AUTHORITATIVE_R1_CATALOG.embedded_contracts)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument("compatibility_matrix", type=Path)
    parser.add_argument("reason_codes", type=Path)
    args = parser.parse_args()
    try:
        check_files(args.compatibility_matrix, args.reason_codes)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        raise SystemExit(1) from exc
    print(json.dumps({"status": "valid"}, sort_keys=True))


__all__ = ["AUTHORITATIVE_R1_CATALOG", "AuthoritativeCatalog", "ContractDescriptor", "ContractRegistry", "EmbeddedDescriptor", "validate_authoritative_catalog", "write_atomic"]
