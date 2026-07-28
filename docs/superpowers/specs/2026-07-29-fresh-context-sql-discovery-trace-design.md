# Fresh-Context SQL Discovery & Trace
## Architecture and Contract Specification

**Document status:** Proposed V1 specification for user review  
**Specification date:** 2026-07-29  
**Scope:** Repository discovery, Frontend-to-Database trace, and SQL conversion projections  
**Primary stack:** Vue 2 JavaScript/TypeScript; C# .NET Framework/OWIN/Web API; SQL Server source; MySQL and PostgreSQL targets  
**Excluded from V1:** API execution, database execution, source rewriting, automatic migration patches, production-equivalence claims

---

## 1. Purpose

This specification defines a deterministic source-analysis system that scans a repository using isolated fresh-context analysis units, discovers database access and SQL, connects Frontend request origins to Backend call chains, resolves request-body and parameter lineage, and generates target-specific SQL conversion projections for MySQL and PostgreSQL.

The system is designed to reduce Lost in the Middle by preventing an ever-growing repository conversation from becoming the working memory of the analysis. Static analyzers produce source-grounded facts and exact evidence anchors. LLMs perform bounded semantic interpretation over one analysis unit at a time. Cross-file reasoning is performed over validated structured facts and typed graph edges.

The specification is normative. Implementations claiming V1 conformance MUST satisfy the required contracts, state transitions, evidence rules, compatibility rules, and acceptance gates defined here.

### 1.1 Primary outcomes

A completed run MUST be able to produce:

1. A reproducible repository inventory tied to an immutable snapshot.
2. A coverage decision for every included source file.
3. Static facts and exact source anchors for supported Vue 2 and C# source.
4. SQL and database-operation findings with original source expressions.
5. Frontend HTTP request findings, including trigger, route, query, headers, and request-body expressions where present.
6. Backend endpoint, handler, service, repository, dependency-injection, DTO, and database-operation findings.
7. Typed cross-file chains from Frontend origin to SQL or an explicit no-database terminal.
8. Request-body lineage from Frontend field to serialized field, Backend DTO/property, method parameter, and SQL parameter where resolvable.
9. Canonical SQL discovery records independent of any target database.
10. MySQL and PostgreSQL conversion projections created independently from the discovery records.
11. Partial, ambiguous, unsupported, and conflicting results with machine-readable reason codes.
12. Audit events, operational state, canonical JSON artifacts, and reproducible human-readable reports.

---

## 2. Scope and non-goals

### 2.1 V1 scope

V1 MUST support:

- Vue 2 Single File Components using JavaScript or TypeScript.
- Vue 2 Options API methods, lifecycle hooks, computed properties, watchers, template event bindings, imported request helpers, and direct Axios/fetch-style calls where statically detectable.
- C# projects using .NET Framework or compatible Roslyn-loadable source, including OWIN and ASP.NET Web API routing patterns.
- Hybrid C# analysis: project-aware semantic analysis when available and syntax fallback when it is not.
- SQL Server source SQL discovery.
- Target projections for both MySQL and PostgreSQL.
- Optional schema-aware validation using DDL, schema dumps, or equivalent metadata when supplied.
- Best-effort dependency-injection resolution from explicit registrations and configuration facts.
- Whole-file and symbol-scoped analysis units.
- Deterministic-first cross-file resolution with focused LLM verification only for semantic gaps.
- Local/private LLM, external-redacted LLM, and static-only run policies.

### 2.2 V1 non-goals

V1 MUST NOT claim or perform:

- API execution.
- Production database query execution.
- Automatic source-code rewriting.
- Automatic migration commits or pull requests.
- Automatic proof of business-semantic equivalence between SQL Server and target SQL.
- Generic support for Vue 3, React, Java, Node.js backends, or arbitrary frameworks.
- Whole-program symbolic execution.
- Runtime-accurate ORM SQL generation when the ORM requires a live provider/runtime to generate SQL.
- Complete dependency-injection resolution for dynamic registrations that cannot be proven from repository facts.
- Resolution of a chain solely from method-name similarity, route suffix similarity, or LLM confidence.

---

## 3. Normative language and terminology

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

Key terminology:

- **Project Source Input:** Repository content intentionally provided for analysis.
- **Snapshot:** Immutable bytes and metadata used by one run.
- **Static Fact:** Parser- or semantic-model-derived information tied to exact source.
- **Evidence Anchor:** Analyzer-created exact source location and source identity.
- **Analysis Unit:** The single bounded source unit sent to one LLM request.
- **Finding:** A validated semantic or structural record tied to one or more evidence anchors.
- **Authoritative Edge:** A cross-entity relationship proven by deterministic evidence.
- **Candidate Edge:** A plausible relationship that has not met authoritative proof requirements.
- **Projection:** Target-specific derived output generated from canonical discovery data.
- **Operational Authority:** Current transactional state used for scheduling and resume.
- **Audit Authority:** Append-only event history used to explain and reconcile state transitions.

---

## 4. Architecture decisions

### ADR-001: Deterministic orchestration owns workflow

The Workflow Coordinator MUST own:

- phase ordering;
- task scheduling;
- state transitions;
- retry classification;
- concurrency limits;
- leases and heartbeats;
- cost reservations;
- cancellation;
- checkpoint and resume;
- cache reuse;
- invalidation;
- run completion and exit status.

LLMs MUST NOT create new workflow tasks, skip validation phases, modify state directly, or declare a run complete.

### ADR-002: Static analyzers own source truth

Static analyzers MUST be the authority for:

- source byte offsets;
- line and column positions;
- source expressions;
- declaration spans;
- symbol declarations;
- syntax relationships;
- semantic symbol resolution when available;
- route, call, assignment, string, and database-operation candidates;
- Evidence Anchors.

LLMs MUST reference existing `anchor_id` values and MUST NOT invent or modify line numbers, columns, byte ranges, file identities, or source hashes.

### ADR-003: Hybrid semantic analysis

The C# analyzer MUST attempt project-aware semantic analysis before syntax fallback.

The analyzer capability enum is:

```text
SEMANTIC_COMPLETE
SEMANTIC_PARTIAL
SYNTAX_ONLY
UNSUPPORTED
```

Every static fact MUST declare the capability level under which it was produced. An implementation MUST NOT mark an overload-sensitive, interface-sensitive, or cross-project relationship authoritative when only syntax facts are available.

The Vue analyzer MUST use Vue SFC parsing plus JavaScript/TypeScript AST analysis and MUST map every extracted span back to the original `.vue` snapshot.

### ADR-004: Immutable hybrid snapshots

For Git repositories, the system SHOULD materialize or address an immutable Git tree based on a selected commit. For non-Git folders, the system MUST create a content-addressed snapshot containing the exact bytes analyzed.

After snapshot creation, all stages MUST read from the snapshot rather than the mutable working tree.

### ADR-005: Analysis Unit is the execution primitive

One LLM request MUST contain source from exactly one Analysis Unit and exactly one file instance. No rolling conversation history from prior units is allowed.

A normal file SHOULD use one whole-file Analysis Unit. A file exceeding context or policy limits MUST be decomposed into symbol-scoped units without cutting through a symbol boundary.

### ADR-006: Deterministic-first cross-file resolution

Resolver edges have three evidence classes:

```text
AUTHORITATIVE
CANDIDATE
REJECTED
```

Focused LLM verification MAY rank candidates, explain semantic gaps, or identify missing evidence. It MUST NOT promote a candidate edge to authoritative status without deterministic evidence accepted by the resolver.

### ADR-007: Discovery and conversion are separate

SQL discovery MUST be target-independent. MySQL and PostgreSQL conversion MUST be independent projections generated from canonical `SqlFinding` records.

A change to target rules, parser version, target runtime profile, or schema metadata MUST NOT invalidate repository inventory, static facts, or target-independent SQL discovery.

### ADR-008: Two-layer state authority

SQLite is the operational authority for current transactional state, leases, checkpoints, stage results, and indexes.

Append-only JSONL is the audit authority for state-transition history, fingerprints, provider calls, policy decisions, migrations, and artifact generation.

The implementation MUST provide reconciliation from audit events to operational snapshots and MUST detect divergence.

### ADR-009: Policy-driven LLM data handling

Each run MUST select one of:

```text
LOCAL_PRIVATE
EXTERNAL_REDACTED
STATIC_ONLY
```

Project source is trusted project input. Policy controls exist for privacy, provider governance, exact-source preservation, and output reliability—not because source is presumed hostile.

### ADR-010: V1 excludes execution and rewrite

V1 MUST end at discovery, trace, conversion projection, validation, and reporting. API execution, database execution, code rewrite, and automatic migration changes belong to later specifications.

---

## 5. System context and data boundaries

```text
[Project Source Input]
        |
        v
[Immutable Snapshot]
        |
        v
[Static Analyzer Adapters]
        |
        v
[Static Facts + Evidence Anchors]
        |
        v
[LLM Data Policy Boundary]
        |
        v
[Bounded Semantic Analysis]
        |
        v
[Contract + Anchor Validation]
        |
        v
[Normalized Findings Store]
        |
        v
[Deterministic Resolver]
        |
        +----------------------+
        |                      |
        v                      v
[Execution Chains]     [SQL Discovery Records]
                               |
                    +----------+----------+
                    |                     |
                    v                     v
             [MySQL Projection]   [PostgreSQL Projection]
                    |                     |
                    +----------+----------+
                               |
                               v
                     [Reports and Exports]
```

### 5.1 Project source handling

Project source MUST be treated as the primary evidence base. The system SHOULD avoid security-oriented threat terminology in normal reporting.

The implementation MUST still enforce:

- snapshot root containment;
- symlink containment;
- exact source hash validation;
- encoding and newline preservation;
- provider allowlists;
- privacy policy for external providers;
- file-size, token, and cost limits.

### 5.2 LLM output handling

LLM output is **non-authoritative semantic output**. It becomes a normalized finding only after:

1. contract-schema validation;
2. identity validation;
3. anchor validation;
4. source-hash validation;
5. allowed-reference validation;
6. invariant validation;
7. conflict checks against authoritative static facts.

Instruction-like text inside comments or string literals MUST be treated as source data rather than pipeline instructions. Prompts MUST state this instruction-isolation rule explicitly.

---

## 6. Identity and provenance model

The system MUST use distinct identities for distinct concepts.

### 6.1 Identity hierarchy

```text
snapshot_id
  └── file_instance_id
        ├── content_id
        ├── symbol_id
        ├── anchor_id
        └── analysis_unit_id
              └── finding_id
                    ├── chain_id
                    └── projection_id
```

### 6.2 Identity definitions

#### `snapshot_id`

Identifies the immutable repository state used by a run.

- Git mode: derived from repository identity, Git tree/commit identity, submodule identities, and snapshot policy version.
- Content-addressed mode: derived from sorted file-instance manifest entries and snapshot policy version.

#### `content_id`

Identifies exact file bytes independently of path.

```text
content_id = sha256(original_bytes)
```

#### `file_instance_id`

Identifies one path instance inside one snapshot. Two files with identical bytes but different paths MUST have different file-instance IDs.

```text
file_instance_id = hash(snapshot_id, normalized_relative_path, content_id)
```

#### `symbol_id`

Identifies a declaration within a file instance.

Where semantic identity is available, the canonical input SHOULD include language, project/module, namespace, containing type, member name, generic arity, parameter types, and declaration anchor.

Where only syntax identity is available, the ID MUST include capability level and MUST NOT imply semantic uniqueness beyond the file.

#### `anchor_id`

Identifies one exact source range in the original snapshot.

```text
anchor_id = hash(file_instance_id, start_byte, end_byte, anchor_kind, analyzer_family_version)
```

#### `analysis_unit_id`

Identifies the bounded unit submitted to static classification or LLM analysis.

```text
analysis_unit_id = hash(file_instance_id, unit_kind, unit_anchor_ids, unit_policy_version)
```

#### `finding_id`

Identifies one normalized finding.

```text
finding_id = hash(
  snapshot_id,
  finding_kind,
  primary_anchor_ids,
  containing_symbol_id,
  normalized_semantic_key,
  finding_contract_version
)
```

#### `chain_id`

Identifies a resolved or partial trace seeded by a Frontend request or Backend endpoint.

#### `projection_id`

Identifies a target-specific conversion result.

```text
projection_id = hash(
  sql_finding_id,
  target_profile_id,
  converter_rule_set_version,
  target_parser_version,
  schema_context_id
)
```

### 6.3 Provenance requirements

Every persisted contract MUST include enough provenance to answer:

- Which snapshot produced this entity?
- Which file instance and source bytes support it?
- Which analyzer, prompt, model, resolver, converter, and schema versions participated?
- Which earlier entities were consumed?
- Which policy mode was used?
- Which stage fingerprint controls cache reuse?

---

## 7. Snapshot and source-fidelity specification

### 7.1 Snapshot modes

```text
GIT_IMMUTABLE
CONTENT_ADDRESSED
```

The selected mode MUST be recorded in `SnapshotManifest`.

### 7.2 Git snapshot requirements

A Git snapshot MUST record:

- repository identity;
- commit ID;
- tree ID when available;
- submodule commit IDs when included;
- sparse/include policy;
- untracked-file policy;
- Git LFS handling policy;
- materialization path or object-reader mode.

A run MUST NOT silently mix committed bytes with mutable working-tree bytes.

### 7.3 Content-addressed snapshot requirements

The snapshot store MUST preserve:

- original bytes;
- normalized relative path;
- content hash;
- detected encoding;
- byte-order mark when present;
- newline style or mixed-newline metadata;
- file size;
- line count computed from original decoded source;
- source-read diagnostics.

### 7.4 Source coordinate system

Evidence MUST use original snapshot coordinates.

Required coordinates:

- `start_byte`, inclusive;
- `end_byte`, exclusive;
- `start_line`, 1-based;
- `end_line`, 1-based;
- `start_column`, 1-based Unicode scalar or explicitly declared coordinate unit;
- `end_column`, exclusive;
- `coordinate_encoding`.

V1 MUST standardize `start_byte/end_byte` against original bytes and line/column against decoded source using a declared encoding. Byte offsets are the final authority when line-column reconstruction is disputed.

### 7.5 Vue SFC source mapping

The Vue adapter MUST NOT report positions from concatenated or synthetic script text as source positions.

For every SFC block, it MUST maintain:

- original block start/end byte offsets;
- block-local to file-global mapping;
- template AST mapping;
- script/script-setup distinction if encountered;
- external-script reference diagnostics;
- generated/synthetic-node indicators.

### 7.6 Redaction and source fidelity

External-redacted mode MUST use length-preserving masking or a reversible offset map that preserves anchor validity.

Redaction MUST NOT alter:

- byte length without an offset map;
- newline count;
- anchor boundaries;
- analysis-unit identity;
- source-hash provenance.

The original snapshot remains the source authority. Redacted payloads MUST have separate payload fingerprints.

---

## 8. Contract families and versioning

### 8.1 Contract families

V1 defines these independently versioned families:

```text
snapshot
identity
source-anchor
static-facts
analysis-unit
llm-analysis
findings
resolver
chain
sql-discovery
conversion-projection
state
pipeline-events
artifacts
policy
benchmark
```

Each envelope MUST include:

```python
class ContractHeader:
    contract_family: str
    contract_version: str
    producer: str
    producer_version: str
    run_id: str
    snapshot_id: str
    correlation_id: str
    created_at: str
```

### 8.2 Version semantics

- Major version: incompatible meaning or structure.
- Minor version: backward-compatible additions.
- Patch version: clarification or validation correction without wire-shape change.

### 8.3 Compatibility matrix

The implementation MUST maintain a machine-readable compatibility matrix defining:

- readable producer versions;
- writable versions;
- available migrators;
- stage invalidation effects;
- whether migration is lossless;
- whether migrated entities require revalidation.

### 8.4 Unknown values

Unknown enum values MUST NOT be silently coerced. They MUST be:

- retained as raw values where forward-compatible;
- quarantined where semantics are required;
- accompanied by a compatibility diagnostic.

### 8.5 Explicit migrators

Every incompatible contract change MUST provide an explicit migrator or explicitly declare that recomputation is required.

### 8.6 Contract registry IDs

The following identifiers are stable references used by the implementation plan, tests, migrations, and review records.

| Contract ID | Contract | Family |
|---|---|---|
| `CTR-RUN-001` | `RunSpec` | policy/state |
| `CTR-SNP-001` | `SnapshotManifest` | snapshot |
| `CTR-FIL-001` | `FileInstance` | identity |
| `CTR-EVD-001` | `EvidenceAnchor` | source-anchor |
| `CTR-UNT-001` | `AnalysisUnit` | analysis-unit |
| `CTR-STF-001` | `StaticFactBundle` | static-facts |
| `CTR-DEC-001` | `AnalysisDecision` | policy |
| `CTR-LRQ-001` | `FileAnalysisRequest` | llm-analysis |
| `CTR-LRS-001` | `FileAnalysisResult` | llm-analysis |
| `CTR-FND-001` | `FindingBase` | findings |
| `CTR-FRQ-001` | `FrontendRequestFinding` | findings |
| `CTR-BEP-001` | `BackendEndpointFinding` | findings |
| `CTR-DBO-001` | `DatabaseOperationFinding` | findings |
| `CTR-UNR-001` | `UnresolvedReference` | findings |
| `CTR-EDG-001` | `ResolverEdge` | resolver |
| `CTR-CVR-001` | `ChainVerificationResult` | resolver |
| `CTR-CHN-001` | `ExecutionChain` | chain |
| `CTR-RRC-001` | `ResolvedRequestContract` | chain |
| `CTR-SQL-001` | `SqlFinding` | sql-discovery |
| `CTR-SCM-001` | `SchemaContext` | sql-discovery |
| `CTR-TRP-001` | `TargetRuntimeProfile` | conversion-projection |
| `CTR-PRJ-001` | `SqlConversionProjection` | conversion-projection |
| `CTR-EVT-001` | `PipelineEvent` | pipeline-events |
| `CTR-ART-001` | `ArtifactManifest` | artifacts |
| `CTR-BMK-001` | `BenchmarkCase` | benchmark |

A contract ID MUST retain its semantics within a major contract version. A replacement with incompatible semantics MUST receive a new contract ID or a new major version recorded in the compatibility matrix.

---

## 9. Core contracts

The following schemas are conceptual normative models. Exact implementation syntax may differ, but field semantics and invariants MUST be preserved.

### 9.1 `RunSpec` (`CTR-RUN-001`)

```python
class RunSpec(ContractHeader):
    repository_root: str
    snapshot_preference: Literal["GIT_THEN_CONTENT", "GIT_ONLY", "CONTENT_ONLY"]
    git_revision: str | None
    include_globs: list[str]
    exclude_globs: list[str]
    frontend_roots: list[str]
    backend_roots: list[str]
    schema_inputs: list[str]
    target_profile_ids: list[str]
    llm_policy_mode: Literal["LOCAL_PRIVATE", "EXTERNAL_REDACTED", "STATIC_ONLY"]
    model_profile_id: str | None
    task_contract_hash: str
    max_file_bytes: int
    max_analysis_unit_tokens: int
    analyzer_concurrency: int
    llm_concurrency: int
    max_attempts_per_unit: int
    max_total_cost_usd: str | None
    strict_snapshot: bool
    verify_semantic_gaps: bool
```

The normalized `RunSpec`, contract compatibility matrix, and toolchain profile MUST contribute to the run contract fingerprint.

For a Git repository with uncommitted content, the implementation MUST NOT silently analyze a mixture of `HEAD` and working-tree bytes. It MUST either analyze the selected immutable Git revision or materialize the requested working-tree content through `CONTENT_ADDRESSED` mode.

### 9.2 `SnapshotManifest` (`CTR-SNP-001`)

```python
class SnapshotManifest(ContractHeader):
    snapshot_mode: Literal["GIT_IMMUTABLE", "CONTENT_ADDRESSED"]
    repository_label: str
    repository_fingerprint: str
    git_commit_id: str | None
    git_tree_id: str | None
    file_instance_ids: list[str]
    snapshot_policy_version: str
    manifest_hash: str
```

### 9.3 `FileInstance` (`CTR-FIL-001`)

```python
class FileInstance(ContractHeader):
    file_instance_id: str
    content_id: str
    relative_path: str
    byte_size: int
    line_count: int
    encoding: str
    newline_mode: str
    language: str
    role_candidates: list[str]
    source_availability: Literal["AVAILABLE", "UNREADABLE", "POLICY_EXCLUDED"]
```

Invariants:

- `relative_path` MUST use normalized POSIX separators.
- `relative_path` MUST remain within the snapshot root.
- `content_id` MUST match the preserved original bytes.

### 9.4 `EvidenceAnchor` (`CTR-EVD-001`)

```python
class EvidenceAnchor(ContractHeader):
    anchor_id: str
    file_instance_id: str
    content_id: str
    anchor_kind: str
    symbol_id: str | None
    start_byte: int
    end_byte: int
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    coordinate_encoding: str
    source_excerpt_hash: str
    analyzer_capability: str
```

Invariants:

- `0 <= start_byte < end_byte <= file_size`.
- Line and column ranges MUST reconstruct to the same source range.
- `source_excerpt_hash` MUST match the bytes in the anchor range.
- Anchors are immutable within a snapshot.

### 9.5 `AnalysisUnit` (`CTR-UNT-001`)

```python
class AnalysisUnit(ContractHeader):
    analysis_unit_id: str
    file_instance_id: str
    unit_kind: Literal[
        "WHOLE_FILE", "TYPE", "METHOD", "FUNCTION", "VUE_COMPONENT",
        "VUE_TEMPLATE", "VUE_SCRIPT", "MODULE_SCOPE"
    ]
    root_anchor_id: str
    included_anchor_ids: list[str]
    containing_symbol_ids: list[str]
    source_slice_start_byte: int
    source_slice_end_byte: int
    unit_policy_version: str
    unit_status: Literal["READY", "STATIC_ONLY", "UNSUPPORTED"]
```

An Analysis Unit MUST reference one file instance only.

### 9.6 `StaticFactBundle` (`CTR-STF-001`)

```python
class StaticFactBundle(ContractHeader):
    analysis_unit_id: str
    file_instance_id: str
    analyzer_adapter: str
    analyzer_capability: str
    symbols: list[SymbolFact]
    imports: list[ImportFact]
    exports: list[ExportFact]
    routes: list[RouteFact]
    calls: list[CallFact]
    assignments: list[AssignmentFact]
    ui_triggers: list[UiTriggerFact]
    http_calls: list[HttpCallFact]
    string_expressions: list[StringExpressionFact]
    database_calls: list[DatabaseCallFact]
    dto_properties: list[DtoPropertyFact]
    di_registrations: list[DiRegistrationFact]
    diagnostics: list[AnalyzerDiagnostic]
```

Every fact MUST reference at least one `anchor_id`.

### 9.7 `AnalysisDecision` (`CTR-DEC-001`)

```python
class AnalysisDecision(ContractHeader):
    file_instance_id: str
    analysis_unit_id: str | None
    decision: Literal[
        "FULL_LLM", "STATIC_ONLY", "SKIPPED_IRRELEVANT", "UNSUPPORTED"
    ]
    reason_codes: list[str]
    classifier_version: str
    supporting_fact_ids: list[str]
```

Every included file MUST have at least one coverage decision.

### 9.8 `FileAnalysisRequest` (`CTR-LRQ-001`)

```python
class FileAnalysisRequest(ContractHeader):
    analysis_unit_id: str
    task_contract_hash: str
    prompt_version: str
    model_profile_id: str
    provider_policy_mode: str
    allowed_finding_kinds: list[str]
    allowed_anchor_ids: list[str]
    static_fact_bundle_hash: str
    source_payload_fingerprint: str
    source_text: str
```

The request MUST include exactly one Analysis Unit and MUST NOT include conversation history from another unit.

### 9.9 `FileAnalysisResult` (`CTR-LRS-001`)

```python
class FileAnalysisResult(ContractHeader):
    analysis_unit_id: str
    analysis_status: Literal[
        "COMPLETE", "PARTIAL", "STATIC_ONLY", "UNSUPPORTED", "FAILED"
    ]
    semantic_symbols: list[SemanticSymbolFinding]
    frontend_requests: list[FrontendRequestFinding]
    backend_endpoints: list[BackendEndpointFinding]
    database_operations: list[DatabaseOperationFinding]
    sql_candidates: list[SqlCandidateFinding]
    unresolved_references: list[UnresolvedReference]
    warnings: list[AnalysisWarning]
    token_usage: TokenUsage | None
```

Every finding in the result MUST reference only allowed anchors and entities from the request, except explicit unresolved references.

---

## 10. Analyzer adapter architecture

### 10.1 Adapter protocol

Every analyzer adapter MUST expose:

- adapter identity and version;
- supported languages/frameworks;
- capability declaration;
- project-context diagnostics;
- analysis-unit extraction;
- static-fact extraction;
- Evidence Anchor generation;
- stable JSON request/response protocol;
- deterministic output for identical inputs and adapter version.

### 10.2 C# analyzer modes

#### Semantic mode

The C# adapter SHOULD load solution/project context using a project-aware Roslyn workspace when possible.

Semantic facts SHOULD include:

- fully qualified symbol identity;
- overload selection;
- interface/base-member relationships;
- type information;
- constant values;
- attribute constructor and named arguments;
- invocation target symbols;
- project and assembly identity;
- partial declarations;
- extension-method resolution.

#### Partial semantic mode

When project loading is incomplete, the adapter MUST declare missing references and MUST downgrade affected facts individually or at bundle level.

#### Syntax-only mode

Syntax-only facts MAY include declarations, invocation syntax, attribute syntax, string expressions, and candidate database operations. They MUST NOT imply semantic call resolution.

### 10.3 Vue 2 analyzer

The Vue adapter MUST support:

- SFC block discovery;
- Options API `methods`, `computed`, `watch`, `data`, and lifecycle hooks;
- template event handlers;
- direct and imported Axios/fetch/custom client calls where detectable;
- request URL, query, headers, and body expressions;
- local assignments and object-construction facts;
- imports/exports;
- object spreads and conditional fields;
- source mapping to the original SFC.

### 10.4 Dependency-injection facts

The C# adapter SHOULD extract explicit registrations from supported container styles and custom registration helpers where statically recognizable.

A DI relationship MUST include:

- service/interface symbol;
- implementation symbol candidate;
- lifetime when available;
- registration scope/module;
- registration anchor;
- resolution status;
- ambiguity reason when multiple implementations are present.

### 10.5 Capability reason codes

At minimum:

```text
PROJECT_LOAD_FAILED
MISSING_REFERENCE
UNSUPPORTED_LANGUAGE_FEATURE
EXTERNAL_SCRIPT_UNAVAILABLE
GENERATED_SOURCE_MAPPING_UNAVAILABLE
FILE_ENCODING_UNSUPPORTED
FILE_TOO_LARGE_FOR_SAFE_UNITIZATION
SEMANTIC_MODEL_PARTIAL
SYNTAX_FALLBACK_USED
```

---

## 11. Deterministic classification and LLM scheduling

Every included file MUST pass deterministic classification before LLM scheduling.

### 11.1 Classification outcomes

#### `FULL_LLM`

Use when static facts indicate relevant database, request, route, DTO, service, repository, or SQL behavior, or when deterministic classification remains uncertain.

#### `STATIC_ONLY`

Use when:

- run policy is static-only;
- external-provider policy excludes the file;
- redaction would remove required semantic content;
- user explicitly excludes the file from LLM processing;
- static facts are sufficient and policy prefers no model call.

#### `SKIPPED_IRRELEVANT`

Use only when deterministic rules prove the file is outside the analysis task. The reason MUST be machine-readable and included in coverage reports.

#### `UNSUPPORTED`

Use when the system cannot safely decode, unitize, parse, or map the file.

### 11.2 Scheduling requirements

The scheduler MUST:

- reserve estimated cost before dispatch;
- respect per-provider and global concurrency limits;
- stop new scheduling when remaining budget cannot cover the reservation;
- avoid duplicate requests through idempotency keys;
- release or reconcile reservations after usage is known;
- persist request fingerprints before dispatch;
- treat timeout-after-dispatch as an indeterminate provider state when provider status cannot be checked.

---

## 12. Findings model

### 12.1 Common finding fields

```python
class FindingBase(ContractHeader):
    finding_id: str
    finding_kind: str
    primary_anchor_ids: list[str]
    related_anchor_ids: list[str]
    containing_symbol_id: str | None
    evidence_class: Literal["STATIC", "SEMANTIC_LLM", "DERIVED"]
    analyzer_capability: str
    confidence: float | None
    status: Literal[
        "VALIDATED", "PARTIAL", "AMBIGUOUS", "CONFLICT",
        "UNRESOLVED", "QUARANTINED"
    ]
    reason_codes: list[str]
```

Confidence MUST NOT substitute for status or evidence class.

### 12.2 `FrontendRequestFinding`

Required semantics:

- Frontend symbol or template trigger origin;
- client type;
- HTTP method when known;
- raw URL expression;
- normalized route when deterministically derivable;
- unresolved route components;
- query expression;
- body expression;
- headers expression;
- body-field seeds;
- trigger anchors;
- request-call anchors.

### 12.3 `BackendEndpointFinding`

Required semantics:

- controller/handler symbol;
- HTTP verbs;
- route template and normalized route;
- route prefix composition evidence;
- parameter bindings;
- request DTO symbol;
- authorization metadata when statically available;
- immediate call facts.

### 12.4 `DatabaseOperationFinding`

Required semantics:

- containing symbol;
- access library/provider;
- operation kind;
- command or query expression anchors;
- parameter-binding anchors;
- transaction context when visible;
- source-dialect classification;
- ORM/raw/stored-procedure category.

### 12.5 `UnresolvedReference`

An unresolved reference MUST include:

- source entity;
- reference kind;
- raw expression/name;
- candidate IDs when available;
- missing evidence type;
- reason code;
- recommended next deterministic resolver action.

---

## 13. Cross-file resolver specification

### 13.1 Typed graph nodes

Required node families:

```text
UI_TRIGGER
FRONTEND_SYMBOL
HTTP_REQUEST
BACKEND_ENDPOINT
BACKEND_SYMBOL
DTO_TYPE
DTO_PROPERTY
DI_REGISTRATION
DATABASE_OPERATION
SQL_FINDING
SCHEMA_OBJECT
```

### 13.2 Edge types

Required edge types:

```text
UI_TRIGGERS_SYMBOL
SYMBOL_MAKES_HTTP_REQUEST
ROUTE_MATCHES_ENDPOINT
SYMBOL_CALLS_SYMBOL
INTERFACE_BINDS_IMPLEMENTATION
REQUEST_BINDS_DTO
BODY_FIELD_MAPS_DTO_PROPERTY
ARGUMENT_BINDS_PARAMETER
PARAMETER_FLOWS_TO_SQL
DATABASE_OPERATION_USES_SQL
SQL_REFERENCES_SCHEMA_OBJECT
```

### 13.3 `ResolverEdge`

```python
class ResolverEdge(ContractHeader):
    edge_id: str
    from_node_id: str
    to_node_id: str | None
    edge_type: str
    authority: Literal["AUTHORITATIVE", "CANDIDATE", "REJECTED"]
    status: Literal["RESOLVED", "AMBIGUOUS", "CONFLICT", "MISSING"]
    evidence_anchor_ids: list[str]
    resolver_id: str
    resolver_version: str
    reason_codes: list[str]
    candidate_node_ids: list[str]
    confidence: float | None
```

### 13.4 Authoritative route resolution

An authoritative route edge requires:

- compatible HTTP verb;
- exact normalized route-template equivalence after deterministic prefix and constant expansion;
- no unresolved route prefix that could change identity;
- one distinguishable endpoint candidate.

Suffix-only route matches MUST remain candidates.

### 13.5 Authoritative symbol resolution

An authoritative symbol call edge requires a semantic symbol reference or another deterministic binding of equivalent strength.

Name equality alone MUST NOT be authoritative.

### 13.6 DI resolution

Explicit registration MAY produce an authoritative interface-binding edge when service and implementation symbols are semantically identified and the registration context is applicable.

Multiple applicable registrations MUST produce ambiguity unless deterministic scope rules distinguish them.

### 13.7 Focused LLM verification

Focused LLM verification MUST consume a compact `ChainVerificationRequest` containing only:

- the chain seed;
- candidate edges;
- referenced static facts;
- Evidence Anchors or exact excerpts;
- allowed candidate IDs;
- explicit questions.

It MUST return `ChainVerificationResult` containing:

```python
class ChainVerificationResult(ContractHeader):
    chain_id: str
    reviewed_candidate_edge_ids: list[str]
    ranked_candidate_edge_ids: list[str]
    referenced_anchor_ids: list[str]
    reason_codes: list[str]
    semantic_explanation: str
    recommended_action: Literal[
        "ACCEPT_CANDIDATE_FOR_REVIEW",
        "REJECT_CANDIDATE",
        "REQUEST_MORE_STATIC_EVIDENCE",
        "KEEP_AMBIGUOUS"
    ]
    confidence: float
```

This result is advisory. A deterministic validator decides whether any new evidence permits edge promotion.

### 13.8 `ExecutionChain` (`CTR-CHN-001`)

```python
class ExecutionChain(ContractHeader):
    chain_id: str
    seed_node_id: str
    frontend_request_id: str | None
    endpoint_id: str | None
    ordered_node_ids: list[str]
    edge_ids: list[str]
    sql_finding_ids: list[str]
    request_contract_id: str | None
    status: Literal[
        "COMPLETE", "PARTIAL", "AMBIGUOUS", "CONFLICT", "REJECTED"
    ]
    weakest_required_edge_status: str
    missing_links: list[MissingLink]
    verification_result_ids: list[str]
    resolver_snapshot_hash: str
```

A chain is `COMPLETE` only when every required edge is authoritative and resolved, and the chain terminates at at least one `SqlFinding` or an explicit deterministic `NO_DATABASE_OPERATION` terminal classification.

Chain confidence MAY be reported for prioritization, but it MUST NOT override `weakest_required_edge_status`.

---

## 14. Request-body and parameter-lineage specification

### 14.1 Resolution levels

The resolver MUST preserve three distinct levels:

1. Raw source expression.
2. Reconstructed Frontend object shape.
3. Backend and SQL lineage mapping.

### 14.2 Body-field statuses

```text
RESOLVED
CONDITIONAL
COMPUTED
UNRESOLVED
MISMATCH
EXCLUDED
```

### 14.3 Required lineage path

Where evidence exists, the system SHOULD resolve:

```text
Frontend source field
  -> serialized wire field
  -> Backend DTO property or endpoint parameter
  -> service/repository method parameter
  -> database parameter binding
  -> SQL placeholder or expression
```

### 14.4 Presence semantics

Object spreads, branch-dependent assignments, optional chaining, and computed keys MUST preserve conditionality. A field that is present only on some paths MUST NOT be reported as always present.

### 14.5 Naming rules

Mapping MAY use:

- explicit serialized-name attributes;
- configured serializer naming policy;
- exact wire-name equality;
- deterministic camelCase/PascalCase conversion when the serializer policy is known.

Name similarity without a known serialization rule remains a candidate mapping.

### 14.6 Type and nullability

When type information is available, lineage SHOULD record:

- Frontend inferred type category;
- Backend declared type;
- nullability;
- collection/object shape;
- conversion or parsing methods;
- mismatch diagnostics.

### 14.7 `ResolvedRequestContract` (`CTR-RRC-001`)

```python
class ResolvedRequestContract(ContractHeader):
    request_contract_id: str
    frontend_request_id: str
    endpoint_id: str | None
    request_dto_symbol_id: str | None
    field_bindings: list[ResolvedFieldBinding]
    unresolved_fields: list[UnresolvedField]
    status: Literal["COMPLETE", "PARTIAL", "MISMATCH", "UNRESOLVED"]
```

Each `ResolvedFieldBinding` MUST preserve the original Frontend expression anchor, wire name, Backend property/parameter identity, presence semantics, and all downstream SQL parameter IDs that are deterministically supported.

---

## 15. SQL discovery specification

### 15.1 Discovery categories

```text
LITERAL
CONCATENATED
INTERPOLATED
BUILDER
HELPER_COMPOSED
STORED_PROCEDURE
ORM_OPERATION
ORM_RAW_SQL
PARTIAL
UNKNOWN
```

### 15.2 `SqlFinding`

```python
class SqlFinding(FindingBase):
    source_dialect: Literal["SQLSERVER", "UNKNOWN"]
    sql_kind: str
    database_operation_id: str
    original_expression_anchor_ids: list[str]
    original_expression_text: str
    reconstructed_template: str | None
    reconstruction_status: Literal[
        "COMPLETE", "PARTIAL", "NOT_APPLICABLE", "FAILED"
    ]
    fragments: list[SqlFragment]
    parameter_bindings: list[SqlParameterBinding]
    dynamic_identifier_bindings: list[DynamicIdentifierBinding]
    referenced_schema_objects: list[SchemaObjectReference]
    risk_codes: list[str]
    manual_review_required: bool
```

### 15.3 Reconstruction rules

Reconstruction MUST preserve unknown fragments explicitly. It MUST NOT silently replace unknown expressions with guessed literals.

A reconstructed template SHOULD use typed placeholders such as:

```text
{{value:param_name}}
{{identifier:table_name}}
{{fragment:where_clause}}
{{unknown:anchor_id}}
```

Dynamic identifiers MUST be distinguished from value parameters.

### 15.4 ORM operations

When exact SQL cannot be known statically, the system MUST record the ORM operation, expression anchors, provider hints, and why exact SQL is unavailable. It MUST NOT fabricate generated SQL.

### 15.5 Source SQL risks

At minimum, discovery MUST flag:

- dynamic table/column identifiers;
- concatenated values with injection surface;
- stored procedure dependencies;
- temp tables and table variables;
- table hints and `NOLOCK`;
- `MERGE`, `OUTPUT`, `APPLY`, `PIVOT`, `UNPIVOT`;
- identity retrieval;
- recursive CTEs;
- date/time and timezone assumptions;
- collation and case-sensitivity assumptions;
- pagination behavior;
- transaction/isolation dependencies.

---

## 16. Optional schema context

### 16.1 Schema modes

```text
NO_SCHEMA
PARTIAL_SCHEMA
COMPLETE_DECLARED_SCHEMA
```

### 16.2 Supported schema inputs

V1 MAY ingest:

- SQL Server DDL files;
- schema-only exports;
- manually supplied catalog JSON;
- migration scripts;
- stored-procedure and function definitions.

### 16.3 Schema context contracts

Schema entities SHOULD include:

- database/schema name;
- object kind;
- table/view/routine identity;
- columns and data types;
- nullability;
- keys and indexes;
- identity/computed attributes;
- parameter and return types;
- source anchors or external-source provenance.

### 16.4 Validation levels

Conversion and discovery reports MUST distinguish:

```text
UNVALIDATED
SYNTAX_VALIDATED
SCHEMA_PARTIALLY_VALIDATED
SCHEMA_VALIDATED
```

Absence of schema MUST NOT prevent syntax-level conversion projection.

---

## 17. Conversion projection architecture

### 17.1 Target profiles

A target profile MUST include:

```python
class TargetRuntimeProfile:
    target_dialect: Literal["MYSQL", "POSTGRESQL"]
    server_version: str
    driver_or_provider: str | None
    sql_mode_or_equivalent: list[str]
    identifier_case_policy: str
    default_collation: str | None
    timezone_policy: str | None
    parameter_style: str
    profile_version: str
```

### 17.2 Projection contract

```python
class SqlConversionProjection(ContractHeader):
    projection_id: str
    sql_finding_id: str
    target_profile_id: str
    target_dialect: str
    candidate_sql: str | None
    changes: list[ConversionChange]
    risk_codes: list[str]
    unsupported_constructs: list[UnsupportedConstruct]
    validation_level: str
    parser_diagnostics: list[str]
    schema_diagnostics: list[str]
    manual_review_required: bool
    status: Literal[
        "CANDIDATE", "PARTIAL", "UNSUPPORTED", "INVALID"
    ]
```

### 17.3 Conversion stages

1. Read canonical `SqlFinding`.
2. Confirm reconstruction sufficiency.
3. Parse source SQL where possible.
4. Apply deterministic target rules.
5. Invoke bounded LLM conversion assistance only for declared semantic ambiguity.
6. Parse or lint target candidate.
7. Apply optional schema-aware checks.
8. Generate changes, risks, unsupported constructs, and review requirement.

### 17.4 Target-independent discovery guarantee

No target-specific rewrite MUST mutate the canonical `SqlFinding`.

### 17.5 MySQL and PostgreSQL concerns

The rule system MUST cover target-specific differences including, where applicable:

- `TOP`, `OFFSET/FETCH`, and `LIMIT` semantics;
- identifier quoting;
- `GETDATE`, `ISNULL`, `CONVERT`, `DATEADD`, `DATEDIFF`;
- string concatenation and NULL behavior;
- boolean representation;
- identity/sequence retrieval;
- `OUTPUT` and `RETURNING`;
- `MERGE` alternatives;
- temporary object behavior;
- collations and case sensitivity;
- stored procedures/functions;
- transaction and isolation differences;
- parameter syntax and driver support.

A projection MUST state the target runtime assumptions used.

---

## 18. State architecture

### 18.1 Run states

```text
CREATED
VALIDATING
SNAPSHOTTING
INVENTORYING
UNITIZING
EXTRACTING_STATIC_FACTS
CLASSIFYING
ANALYZING_UNITS
NORMALIZING
BUILDING_INDEXES
RESOLVING_CHAINS
VERIFYING_GAPS
DISCOVERING_SQL
PROJECTING_TARGETS
GENERATING_REPORTS
COMPLETED
PARTIAL_SUCCESS
PAUSED
CANCELLING
CANCELLED
FAILED
RECONCILING
```

### 18.2 File states

```text
DISCOVERED
SNAPSHOTTED
UNITIZATION_PENDING
UNITIZED
STATIC_PENDING
STATIC_RUNNING
STATIC_COMPLETE
CLASSIFIED
ANALYSIS_PENDING
ANALYSIS_RUNNING
ANALYSIS_COMPLETE
VALIDATED
STATIC_ONLY_COMPLETE
QUARANTINED
UNSUPPORTED
FAILED_TERMINAL
STALE
```

### 18.3 Analysis-unit states

```text
READY
STATIC_PENDING
STATIC_COMPLETE
LLM_PENDING
LLM_RUNNING
LLM_RETRY_WAIT
LLM_COMPLETE
VALIDATED
STATIC_ONLY
QUARANTINED
UNSUPPORTED
FAILED_TERMINAL
STALE
```

A file is analysis-complete only when all required units are in terminal states and aggregation has completed.

### 18.4 Chain states

```text
NEW
RESOLVING
COMPLETE
PARTIAL
AMBIGUOUS
CONFLICT
VERIFICATION_PENDING
VERIFICATION_REVIEWED
REJECTED
STALE
```

### 18.5 Projection states

```text
PENDING
GENERATING
CANDIDATE
PARTIAL
UNSUPPORTED
INVALID
STALE
```

### 18.6 Transactional state change

Every operational transition MUST:

1. validate the current state and transition rule;
2. write an audit event through the same transaction or durable outbox;
3. update the operational snapshot;
4. commit atomically from the caller’s perspective.

### 18.7 Idempotency

Idempotency keys MUST include the logical entity, stage, input fingerprint, and contract family version. Repeated completion with identical payload hashes MUST be a no-op. Different payload hashes for the same deterministic input MUST produce a nondeterminism diagnostic.

### 18.8 Required transition invariants

- A run MUST reach `SNAPSHOTTING` before inventory or analysis.
- Static analysis MUST complete or terminate before an Analysis Unit enters `LLM_PENDING`.
- An LLM result MUST enter `LLM_COMPLETE` before validation.
- Only validated findings may be indexed by the authoritative resolver.
- A stale entity MUST NOT be consumed by a downstream stage.
- A projection MUST reference a validated `SqlFinding` and a compatible target profile.
- `COMPLETED` requires all required phases complete and all required entities terminal.
- `PARTIAL_SUCCESS` requires usable artifacts plus at least one declared non-success terminal entity.
- Resume MUST return to the first incomplete phase whose input fingerprint remains compatible.

The implementation plan MUST define and test the complete allowed-transition tables. Any transition not explicitly allowed by those tables is invalid.

---

## 19. Events, reconciliation, and rebuild

### 19.1 Required event fields

```python
class PipelineEvent:
    sequence: int
    event_id: str
    event_type: str
    run_id: str
    snapshot_id: str
    entity_type: str
    entity_id: str
    stage: str | None
    idempotency_key: str
    input_fingerprint: str | None
    payload_hash: str
    payload: dict
    occurred_at: str
```

### 19.2 Audit events

At minimum:

- snapshot created;
- file discovered;
- analysis unit created;
- static analysis completed;
- classification decision made;
- provider request reserved/dispatched/completed/failed;
- result validated/quarantined;
- index built;
- resolver edge created/updated;
- chain state changed;
- SQL finding created;
- conversion projection generated;
- artifact generated;
- contract migration applied;
- invalidation applied;
- run paused/resumed/completed.

### 19.3 Reconciliation

The reconciliation process MUST detect:

- missing operational rows for committed events;
- operational state without a corresponding audit event;
- payload-hash mismatches;
- non-monotonic event sequences;
- invalid state transitions;
- missing referenced snapshot entities.

### 19.4 Rebuild scope

The system SHOULD be able to rebuild derived operational views from:

- immutable snapshot;
- contract versions and migrators;
- append-only events;
- retained stage payloads.

Provider calls need not be repeated when validated stage payloads remain available and compatible.

---

## 20. Cache and invalidation model

### 20.1 Stage fingerprints

Every stage MUST compute a fingerprint from all inputs that can alter output semantics.

### 20.2 Minimum invalidation rules

| Change | Minimum invalidation |
|---|---|
| Snapshot/file bytes | Unitization and all downstream entities for affected file instances |
| Unitization policy | Analysis units and downstream stages |
| Analyzer version | Static facts and downstream stages for affected adapter/language |
| Prompt/task contract/model profile | LLM analysis and downstream semantic findings |
| Classification rules | Decisions, scheduled analysis, and affected downstream findings |
| Resolver rules | Edges, chains, verification, and reports |
| DI resolution rules | DI edges and affected chains |
| SQL discovery rules | SQL findings and projections |
| MySQL rule set | MySQL projections and target reports only |
| PostgreSQL rule set | PostgreSQL projections and target reports only |
| Schema context | Schema validations and affected projections/reports |
| Report template | Generated report artifacts only |
| Contract migration | Entities declared by compatibility matrix |

### 20.3 Parent-child runs

Incremental analysis SHOULD create a child run referencing a parent run. Reused entities MUST retain origin provenance and new validation status.

---

## 21. Failure, retry, and quarantine

### 21.1 Error classes

```text
TRANSIENT_TRANSPORT
PROVIDER_RATE_LIMIT
TIMEOUT_BEFORE_DISPATCH
TIMEOUT_AFTER_DISPATCH
INVALID_STRUCTURED_OUTPUT
CONTRACT_INCOMPATIBLE
EVIDENCE_MISMATCH
SOURCE_CHANGED
ANALYZER_PROTOCOL_ERROR
ANALYZER_CAPABILITY_LIMIT
BUDGET_EXCEEDED
POLICY_RESTRICTED
NONDETERMINISTIC_RESULT
FATAL_CONFIGURATION
```

### 21.2 Retry policy

- Transport and rate-limit errors MAY retry with bounded exponential backoff and jitter.
- Invalid structured output MAY receive at most a bounded repair request containing compact validation errors.
- Evidence mismatch MUST NOT enter an unbounded automatic retry loop; it MUST be quarantined.
- Unsupported capability MUST become an explicit terminal outcome.
- Budget exhaustion MUST pause or partially complete the run without scheduling new requests.

### 21.3 Partial success

A run MAY finish as `PARTIAL_SUCCESS` when usable outputs exist but some entities are unsupported, quarantined, failed, or unresolved. Reports MUST expose coverage and failure counts.

---

## 22. LLM data policy

### 22.1 `LOCAL_PRIVATE`

- Source MAY be sent without redaction according to local policy.
- Provider, model, prompt, and payload fingerprints MUST still be recorded.

### 22.2 `EXTERNAL_REDACTED`

The system MUST apply:

- file/root allowlist;
- secret and connection-information detection;
- length-preserving redaction or offset map;
- payload-size limits;
- provider/model allowlist;
- auditable policy version;
- user-exclusion rules.

### 22.3 `STATIC_ONLY`

- No source is sent to an LLM.
- Static facts and deterministic resolvers remain active.
- Missing semantic capability MUST be reported explicitly.

### 22.4 Policy reason codes

```text
POLICY_SECRET_DETECTED
POLICY_FILE_NOT_ALLOWED
POLICY_PROVIDER_RESTRICTED
POLICY_USER_EXCLUDED
POLICY_REDACTION_INSUFFICIENT
POLICY_STATIC_ONLY_RUN
```

### 22.5 Data retention

Retention policy MUST independently control:

- original snapshot retention;
- redacted payload retention;
- LLM request/response retention;
- stage-result retention;
- audit-event retention;
- generated artifacts.

---

## 23. Observability, cost, and performance

### 23.1 Correlation fields

Logs, events, and metrics MUST support:

- `run_id`;
- `snapshot_id`;
- `file_instance_id`;
- `analysis_unit_id`;
- `request_id`;
- `finding_id`;
- `chain_id`;
- `projection_id`.

### 23.2 Required metrics

#### Inventory and coverage

- files discovered;
- files by language/role;
- files classified by decision;
- unsupported files;
- unitization counts;
- coverage percentage.

#### Analyzer

- parse time;
- semantic-load success rate;
- syntax-fallback rate;
- diagnostics;
- adapter restarts;
- exact-anchor validation failures.

#### LLM

- request count;
- latency;
- retries;
- structured-output failure rate;
- evidence-validation failure rate;
- input/output tokens;
- reserved and actual cost;
- cache hit rate.

#### Resolver

- authoritative edges;
- candidate edges;
- ambiguous/conflict counts;
- chain lengths;
- missing-link categories;
- body-lineage resolution rate.

#### SQL and conversion

- SQL findings by kind;
- complete/partial reconstruction;
- dynamic-identifier count;
- target projections by status;
- syntax/schema validation rates;
- manual-review rates.

### 23.3 Cost reservation

Before dispatch, the scheduler MUST reserve a conservative estimated maximum request cost. Concurrent active reservations MUST count against the run budget.

Actual usage MUST reconcile against reservations after completion. Budget policies MUST define whether excess caused by provider-reported usage results in pause, partial success, or failure.

### 23.4 Performance controls

The system MUST use:

- bounded queues;
- independent analyzer and LLM concurrency;
- stage caches;
- symbol-scoped unitization;
- compact focused verification payloads;
- streaming or paged report generation for large runs where required.

---

## 24. Artifact model

### 24.1 Canonical exports

SQLite is operational authority and JSONL is audit authority. Exported JSON is the canonical interoperable representation of normalized entities, not the mutable operational state authority.

Required exports:

```text
snapshot-manifest.json
file-inventory.jsonl
analysis-decisions.jsonl
static-facts.jsonl
findings.jsonl
resolver-edges.jsonl
execution-chains.jsonl
sql-findings.jsonl
mysql-projections.jsonl
postgresql-projections.jsonl
pipeline-events.jsonl
artifact-manifest.json
run-summary.json
```

### 24.2 Human-readable views

V1 SHOULD produce:

- HTML report;
- XLSX report;
- CLI inspection views.

All human-readable views MUST be reproducible from validated store/export data and MUST NOT require new LLM calls.

### 24.3 `ArtifactManifest`

The manifest MUST include:

- artifact path/type;
- content hash;
- source entity families;
- generator version;
- template version;
- run/snapshot IDs;
- generation timestamp;
- completeness status.

---

## 25. CLI behavior contract

A conforming CLI SHOULD expose equivalent capabilities to:

```text
sqltrace snapshot <repo>
sqltrace inventory --run <run-id>
sqltrace analyze --run <run-id>
sqltrace resolve --run <run-id>
sqltrace project --run <run-id> --target mysql
sqltrace project --run <run-id> --target postgresql
sqltrace report --run <run-id> --format json,html,xlsx
sqltrace resume --run <run-id>
sqltrace reconcile --run <run-id>
sqltrace inspect finding <finding-id>
sqltrace inspect chain <chain-id>
sqltrace inspect projection <projection-id>
```

Machine-readable stdout modes MUST not be mixed with human progress output. Progress and diagnostics SHOULD go to stderr.

Exit statuses MUST distinguish:

- complete success;
- partial success;
- paused by budget/policy;
- validation failure;
- fatal configuration failure.

---

## 26. Benchmark and acceptance specification

V1 is production-gated. Completion of feature tasks alone is insufficient.

### 26.1 Benchmark layers

#### Layer A: Synthetic fixtures

Purpose:

- isolate language and SQL edge cases;
- verify exact spans;
- verify negative behavior;
- test contract invariants.

#### Layer B: Curated Vue/C# pairs

Purpose:

- measure Frontend-to-Backend route linking;
- request-body and DTO mapping;
- service/repository call chains;
- SQL parameter lineage.

#### Layer C: Representative repository snapshot

Purpose:

- measure coverage;
- performance;
- cost;
- resume behavior;
- operational stability;
- realistic ambiguity.

### 26.2 Ground truth requirements

Benchmark truth MUST include:

- expected findings;
- exact anchor ranges;
- expected authoritative and candidate edges;
- expected chain states;
- expected body fields and lineage;
- expected SQL classifications;
- expected conversion-risk flags;
- intentionally unresolved cases.

### 26.3 V1 release gates

Unless a stricter project-specific gate is configured, V1 release MUST meet all of the following on the approved benchmark corpus:

#### Source fidelity

- Exact anchor byte-range accuracy: **100%** for accepted findings.
- Anchor source-hash validation: **100%**.
- Vue SFC global-offset mapping accuracy: **100%** on benchmark fixtures.

#### Discovery

- SQL discovery recall: **>= 95%**.
- SQL discovery precision: **>= 97%**.
- Frontend HTTP request recall: **>= 95%**.
- Backend endpoint recall: **>= 98%**.

#### Resolution

- Authoritative route-edge precision: **>= 99%**.
- Authoritative semantic call-edge precision: **>= 99%**.
- Complete-chain precision: **>= 98%**.
- Request-body field mapping precision: **>= 97%**.
- SQL parameter-lineage precision: **>= 97%**.

#### Conversion

- Deterministic rule regression pass rate: **100%**.
- Target parser acceptance for projections marked syntax-valid: **100%**.
- Mandatory risk-flag recall on annotated fixtures: **100%**.

#### Resume and determinism

- Completed compatible stages repeated after interruption: **0**.
- Duplicate normalized findings from retry: **0**.
- Same snapshot/config/version produces identical deterministic entity IDs: **100%**.

#### Contract compatibility

- All supported compatibility-matrix migrations pass round-trip or declared-loss tests: **100%**.
- Unknown incompatible contract versions are rejected or quarantined: **100%**.

#### Privacy and policy

- External-redacted benchmark secrets present in provider payloads: **0**.
- Redaction-induced anchor mismatches: **0**.

#### Performance and cost

Project-specific absolute ceilings MUST be configured for the representative repository. At minimum, release testing MUST verify:

- bounded memory under configured concurrency;
- no unbounded queue growth;
- budget reservation prevents new scheduling beyond the configured maximum exposure;
- cache-enabled rerun reduces repeated LLM requests to only invalidated units.

### 26.4 Metrics interpretation

A high recall score MUST NOT justify lowering authoritative-edge precision. Uncertain links belong in candidate or ambiguous states.

---

## 27. Required adversarial and negative fixtures

The benchmark MUST include:

- same method name in multiple namespaces;
- overloaded C# methods;
- interface with multiple implementations;
- duplicate routes with different verbs;
- duplicate routes with indistinguishable handlers;
- route prefix constants;
- Axios instance with base URL;
- custom request wrapper;
- Vue mixin or imported method;
- conditional object spread;
- computed request field;
- DTO serialized-name override;
- SQL text inside comments that must not be counted;
- SQL-shaped test data that must not be counted under configured policy;
- interpolated dynamic identifier;
- partial SQL builder;
- stored procedure call;
- LINQ/ORM operation without exact SQL;
- file changed after working-tree snapshot request;
- external provider timeout after dispatch;
- malformed structured output;
- evidence anchor outside allowed unit;
- Windows path and case behavior;
- mixed newline and Unicode identifier cases;
- duplicate-content files at different paths;
- analysis-unit overlap and deduplication cases.

---

## 28. Definition of done for the specification

An implementation conforms to this V1 specification only when:

1. Every included file has an auditable coverage decision.
2. Every accepted finding references analyzer-created exact Evidence Anchors.
3. No LLM-created line/column is accepted as source authority.
4. C# analysis declares semantic capability and degrades explicitly.
5. Vue SFC spans map to the original snapshot.
6. Large files use deterministic symbol-scoped Analysis Units when required.
7. Cross-file authoritative edges are backed by deterministic evidence.
8. Focused LLM verification remains advisory.
9. SQL discovery is target-independent.
10. MySQL and PostgreSQL projections can be regenerated independently.
11. Optional schema context changes validation without requiring source reanalysis.
12. SQLite operational state and JSONL audit events reconcile.
13. Stage-specific invalidation works as specified.
14. Reports regenerate without provider calls.
15. All production acceptance gates pass.

---

## 29. Deferred V2 capabilities

The following require separate design approval and contracts:

- controlled API execution;
- fixture and environment management;
- database equivalence testing;
- source rewrite and patch generation;
- migration pull requests;
- Vue 3, React, Java, and Node adapters;
- runtime tracing;
- dynamic instrumentation;
- distributed multi-node execution;
- organization-level access control and shared service deployment.

---

## Appendix A: Authoritative decision summary

| Decision | V1 choice |
|---|---|
| Product scope | Discovery, Trace, Conversion only |
| Target databases | MySQL and PostgreSQL projections |
| Accuracy | Exact source spans required |
| Analyzer mode | Semantic-first with syntax fallback |
| Snapshot | Git immutable with content-addressed fallback |
| State authority | SQLite operational + JSONL audit |
| Large files | Whole file, then symbol-scoped Analysis Units |
| Conversion | Discovery once, projections later |
| Source-span authority | Static analyzer Evidence Anchors |
| Framework scope | Vue 2 JS/TS + C# .NET Framework/OWIN/Web API |
| Schema | Optional schema-aware |
| DI | Best-effort explicit resolution |
| LLM scheduling | Deterministic two-tier classification |
| Chain verification | Deterministic-first; focused LLM advisory |
| Contract versioning | Per-family compatibility matrix + migrators |
| Identity | Multi-level deterministic identities |
| LLM policy | Local, external-redacted, or static-only |
| Acceptance | Production-gated |
| Benchmark | Synthetic + curated pairs + repository snapshot |
| Source framing | Trusted project input; reliability/privacy focus |

## Appendix B: Contract reason-code principles

Reason codes MUST be:

- stable within a major contract version;
- machine-readable;
- specific enough to guide remediation;
- separate from human-readable explanations;
- preserved through exports and reports.

## Appendix C: Spec-to-plan handoff

The implementation plan derived from this specification MUST:

- reference contract family and ADR identifiers;
- separate production-capable vertical slices;
- include failing, negative, and adversarial tests;
- define benchmark gates at each milestone;
- avoid illustrative implementations that contradict this specification;
- identify exact invalidation impact for every task;
- keep API execution and source rewriting outside V1.
