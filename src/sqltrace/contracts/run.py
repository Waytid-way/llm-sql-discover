"""Run request and pre-snapshot run specification contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .meta import BootstrapEnvelope, RunEnvelope


class RunRequest(BootstrapEnvelope):
    contract_id: Literal["CTR-RQR-001"] = "CTR-RQR-001"
    repository_root: str
    snapshot_preference: Literal["GIT_THEN_CONTENT", "GIT_ONLY", "CONTENT_ONLY"] = "GIT_THEN_CONTENT"
    include_globs: list[str] = Field(default_factory=list)
    exclude_globs: list[str] = Field(default_factory=list)
    frontend_roots: list[str] = Field(default_factory=list)
    backend_roots: list[str] = Field(default_factory=list)
    schema_inputs: list[str] = Field(default_factory=list)
    target_profile_ids: list[str] = Field(default_factory=list)
    llm_policy_mode: Literal["LOCAL_PRIVATE", "EXTERNAL_REDACTED", "STATIC_ONLY"] = "STATIC_ONLY"
    model_profile_id: str | None = None
    task_contract_hash: str = ""
    max_file_bytes: int = 10_000_000
    max_analysis_unit_tokens: int = 32_000
    analyzer_concurrency: int = 1
    llm_concurrency: int = 1
    max_attempts_per_unit: int = 1
    max_total_cost_usd: str | None = None
    strict_snapshot: bool = True
    verify_semantic_gaps: bool = False


class RunSpec(RunEnvelope):
    contract_id: Literal["CTR-RUN-001"] = "CTR-RUN-001"
    repository_root: str
    snapshot_preference: Literal["GIT_THEN_CONTENT", "GIT_ONLY", "CONTENT_ONLY"] = "GIT_THEN_CONTENT"
    git_revision: str | None = None
    include_globs: list[str] = Field(default_factory=list)
    exclude_globs: list[str] = Field(default_factory=list)
    frontend_roots: list[str] = Field(default_factory=list)
    backend_roots: list[str] = Field(default_factory=list)
    schema_inputs: list[str] = Field(default_factory=list)
    target_profile_ids: list[str] = Field(default_factory=list)
    llm_policy_mode: Literal["LOCAL_PRIVATE", "EXTERNAL_REDACTED", "STATIC_ONLY"] = "STATIC_ONLY"
    model_profile_id: str | None = None
    task_contract_hash: str = ""
    max_file_bytes: int = 10_000_000
    max_analysis_unit_tokens: int = 32_000
    analyzer_concurrency: int = 1
    llm_concurrency: int = 1
    max_attempts_per_unit: int = 1
    max_total_cost_usd: str | None = None
    strict_snapshot: bool = True
    verify_semantic_gaps: bool = False


__all__ = ["RunRequest", "RunSpec"]
