# Fresh-Context SQL Discovery & Trace
## Normative Amendment v1.1

**Status:** Approved normative amendment  
**Date:** 2026-07-29  
**Applies to:** `2026-07-29-fresh-context-sql-discovery-trace-design.md`  
**Scope:** Resolves planning blockers #1–#9 and supersedes conflicting text in the base specification.

This amendment is normative. Where this document and the base specification disagree, this amendment takes precedence. Requirements not changed here remain in force.

---

## A1. Lifecycle envelopes and identity creation order

The single `ContractHeader` model is replaced by four lifecycle envelopes:

```python
class ContractMeta:
    contract_id: str
    contract_family: str
    contract_version: str
    producer: str
    producer_version: str
    created_at: str

class BootstrapEnvelope(ContractMeta):
    correlation_id: str

class RunEnvelope(BootstrapEnvelope):
    run_id: str

class SnapshotEnvelope(RunEnvelope):
    snapshot_id: str
```

The creation order is fixed:

```text
RunRequest received
  -> run_id allocated
  -> RunSpec persisted
  -> RUN_CREATED committed
  -> snapshot materialized
  -> snapshot_id calculated
  -> SnapshotManifest persisted
  -> SNAPSHOT_CREATED committed
  -> source-derived identities created
```

Rules:

- User input uses `RunRequest` (`CTR-RQR-001`) with `BootstrapEnvelope`.
- Persisted pre-snapshot configuration uses `RunSpec` (`CTR-RUN-001`) with `RunEnvelope`.
- Source-derived contracts use `SnapshotEnvelope`.
- Global registries and compatibility documents use `ContractMeta` only.
- `snapshot_id` is never populated with a placeholder or sentinel.
- `SNAPSHOT_FAILED` is valid with `run_id` and without `snapshot_id`.
- A legacy `RunSpec` drops any early placeholder `snapshot_id`; unverifiable sentinel identities are quarantined rather than auto-migrated.

Deterministic identity hierarchy:

```text
correlation_id
  -> run_id
    -> snapshot_id
      -> file_instance_id
        -> symbol_id / anchor_id / analysis_unit_id
          -> finding_id
            -> chain_id / projection_id
```

---

## A2. Contract ownership, registry, and reason codes

Every shape belongs to exactly one category:

1. independently versioned top-level public contract;
2. embedded public schema owned and versioned by one top-level contract; or
3. implementation-private model that cannot cross a persisted/exported boundary.

A persisted nested shape is addressed as `CONTRACT_ID#TypeName`. A type shared across contract families must be promoted to a top-level contract.

New stable top-level IDs:

| Contract ID | Contract |
|---|---|
| `CTR-RQR-001` | `RunRequest` |
| `CTR-CAP-001` | `AnalyzerCapability` |
| `CTR-FSB-001` | `FileStructureBundle` |
| `CTR-SQC-001` | `SqlCandidate` |
| `CTR-SNR-001` | `SqlNormalizationResult` |
| `CTR-NDB-001` | `NoDatabaseOperationFinding` |
| `CTR-OUT-001` | `OutboxRecord` |
| `CTR-ESM-001` | `EventSegmentManifest` |
| `CTR-BMM-001` | `BenchmarkManifest` |
| `CTR-RSN-001` | `ReasonCodeRegistry` |

Required embedded ownership includes:

- static facts (`SymbolFact`, `CallFact`, `RouteFact`, `HttpCallFact`, `DatabaseCallFact`, DTO and DI facts) under `CTR-STF-001`;
- structural outlines, file-scoped facts, and SFC block maps under `CTR-FSB-001`;
- semantic symbols, warnings, and token usage under `CTR-LRS-001`;
- missing links under `CTR-CHN-001`;
- resolved/unresolved field bindings under `CTR-RRC-001`;
- SQL fragments and bindings under `CTR-SQL-001`;
- conversion changes and diagnostics under `CTR-PRJ-001`.

`CTR-RSN-001` records code, namespace, owner contract, severity, terminal behavior, description, introduction version, and deprecation/replacement. Namespaces are `SNAPSHOT`, `SOURCE`, `ANALYZER`, `UNIT`, `LLM`, `NORMALIZATION`, `RESOLVER`, `SQL`, `PROJECTION`, `STATE`, `EVENT`, `POLICY`, and `BENCHMARK`. Codes cannot be silently removed or repurposed within a major version.

---

## A3. Structural scan and deterministic Analysis Units

The source pipeline order is corrected to:

```text
immutable snapshot
  -> inventory
  -> structural scan and exact anchors
  -> FileStructureBundle
  -> deterministic unitization
  -> unit static facts
  -> classification / bounded LLM analysis
```

`FileStructureBundle` (`CTR-FSB-001`) owns symbol/block boundaries, root anchors, file-scoped imports/module facts, SFC block maps, parser diagnostics, capability ID, and `structure_hash`. Unitization consumes `structure_hash`; it does not depend on later semantic/LLM output.

`AnalysisUnit` (`CTR-UNT-001`) includes unit index, owner symbol, primary anchors, context anchors, source byte slice, required flag, token estimate, token-estimator version, unitization-policy version, and unitization fingerprint.

Normative rules:

- Whole-file units are used when the token limit permits.
- Oversized files are partitioned by top-level analyzable symbols ordered by original `start_byte`, then kind priority and `symbol_id`.
- Primary ranges never overlap and never cut through a symbol.
- Imports, containing-type headers, fields, and helper declarations may overlap only as context anchors.
- A semantic finding requires at least one primary anchor owned by its emitting unit; context-only anchors cannot originate a finding.
- File-scoped structural facts are stored once in `FileStructureBundle`.
- `finding_id` is the deduplication key. Identical payload hashes merge provenance. Different hashes for the same ID produce `NORMALIZATION.DUPLICATE_PAYLOAD_CONFLICT`; neither is silently selected.
- A file is complete only after all required units are terminal and aggregation is `COMPLETE` or `PARTIAL_COMPLETE`.
- Unitization-policy, token-estimator, symbol-tree, or structural-parser changes invalidate units and downstream outputs.

---

## A4. Analyzer capability proofs

`AnalyzerCapability` (`CTR-CAP-001`) is structured and scoped to workspace, project, file, analysis unit, or fact. It records level, project-load state, compilation profile hash, resolved/unresolved references, affecting diagnostics, conditional symbols, permitted fact classes, and reason codes.

Objective levels:

- `SEMANTIC_COMPLETE`: parsing succeeded and every symbol/type needed to prove the fact resolves under the recorded compilation profile with no affecting error.
- `SEMANTIC_PARTIAL`: a semantic model exists, but missing references, generated sources, project references, or diagnostics prevent proof for some facts.
- `SYNTAX_ONLY`: exact source parsing and anchors are available, but no usable semantic model proves the fact.
- `UNSUPPORTED`: exact parsing, decoding, mapping, or required language-feature support cannot be produced.

The most specific capability record wins. Unrelated compiler warnings do not downgrade every fact.

Minimum proof rules:

- Exact syntax anchors require at least `SYNTAX_ONLY`.
- C# overload-specific calls, interface relationships, explicit DI symbol bindings, and cross-project constants require fact-level `SEMANTIC_COMPLETE`.
- A local Vue template handler can be authoritative with exact local AST binding; imported/module bindings require module-resolution proof.
- Weaker capability can create a candidate edge but cannot create an authoritative edge requiring stronger proof.

Semantic cache fingerprints include project files, references, target framework, build configuration, conditional symbols, analyzer options, and adapter version.

---

## A5. Vue SFC original-byte mapping

Original snapshot bytes are the authority. Parser-local offsets are never persisted directly.

For each SFC block, record block kind, opening-tag range, content byte range, closing-tag position, parser coordinate unit, and external `src`.

Translation algorithm:

1. Decode original bytes without newline normalization.
2. Build mappings among original bytes, Unicode scalars, and UTF-16 code units.
3. Locate block boundaries against original text and verify original bytes.
4. Convert parser-local ranges to global decoded indexes using the declared coordinate unit.
5. Convert global decoded indexes back to original byte offsets.
6. Reconstruct line/column from original bytes.
7. Round-trip the parser-selected text against the original-byte substring.
8. Persist an anchor only when every check succeeds.

Rules:

- BOM, LF, CRLF, CR, mixed newlines, astral Unicode, and combining characters require byte-exact fixtures.
- TypeScript UTF-16 offsets must pass through the UTF-16-to-byte map.
- `<script src>` content is a separate `FileInstance`; the `.vue` attribute anchor and external source anchor are both retained.
- `<script setup>` is outside Vue 2 V1 semantic support and produces `ANALYZER.UNSUPPORTED_BLOCK_KIND` unless a versioned capability adds support.
- Recovered/malformed nodes can claim exact anchors only when contiguous range and round-trip checks pass.
- Generated/transformed text is not source authority without a verified map to original snapshot bytes.

---

## A6. SQL candidate normalization and promotion

`FileAnalysisResult` may emit `SqlCandidate` (`CTR-SQC-001`), but conversion consumes only canonical `SqlFinding` (`CTR-SQL-001`).

`SqlNormalizationResult` (`CTR-SNR-001`) has outcomes:

```text
PROMOTED
PARTIAL_PROMOTED
REJECTED_FALSE_POSITIVE
QUARANTINED_CONFLICT
REJECTED_UNANCHORED
```

Promotion requires:

1. analyzer-created anchors for every source fragment and original expression;
2. a validated `DatabaseOperationFinding`, except an explicitly supported standalone SQL resource;
3. no conflict with authoritative static facts;
4. reconstruction from anchored literals/fragments, deterministic transformations, and explicit unknown placeholders only;
5. removal or unknown-placeholder representation of LLM text not recoverable from source anchors;
6. deterministic merge of equivalent candidates and quarantine of conflicting payloads.

Unknown fragments use typed placeholders such as `{{unknown:anchor_id}}`; dynamic identifiers remain distinct from value parameters. Rejected candidates stay auditable but cannot create projections. SQL discovery occurs before index construction and chain resolution so complete chains may terminate at canonical SQL findings.

---

## A7. Resolver proof matrix and no-database terminal

`ResolverEdge` separates proof strength (`AUTHORITATIVE`, `CANDIDATE`, `REJECTED`) from resolution status (`RESOLVED`, `AMBIGUOUS`, `CONFLICT`, `MISSING`). Confidence ranks candidates only.

Authoritative requirements:

| Edge | Required proof |
|---|---|
| UI trigger → symbol | Exact local template/directive AST binding; imported cases require module resolution. |
| Symbol → HTTP request | Recognized HTTP call AST owned by the exact caller symbol. |
| Route → endpoint | Compatible verb; base URL, prefix, constants, and parameter tokens fully normalized; exactly one endpoint. |
| Symbol → symbol | Exact semantic target signature/overload. Name equality is candidate-only. |
| Interface → implementation | Explicit applicable DI registration with resolved symbols and unambiguous scope. |
| Request → DTO | Deterministic framework/model-binder selection. |
| Body field → DTO property | Explicit serialized name or known serializer policy yielding exact wire name. |
| Argument → parameter | Exact semantic invocation binding. |
| Parameter → SQL | Deterministic def-use path with no unresolved transformation. |
| DB operation → SQL | Exact anchored expression promoted through SQL normalization. |
| SQL → schema object | Syntax-valid parsed identifier uniquely resolved in supplied schema context. |

Multiple applicable candidates are `AMBIGUOUS`; contradictory authoritative facts are `CONFLICT`; absent proof is `MISSING`; disproven candidates are retained as `REJECTED`.

`NoDatabaseOperationFinding` (`CTR-NDB-001`) is valid only when every required reachable call is authoritatively resolved, every reachable symbol has sufficient database-detection capability, and no DB operation or unresolved call remains. “No SQL found” is never enough. Complete chain state is a pure function of required edge states plus validated SQL or no-database terminal.

Focused LLM verification remains advisory and cannot promote an edge without newly validated deterministic evidence satisfying this matrix.

---

## A8. Transactional outbox and rebuild

V1 selects one durability protocol:

1. Begin SQLite transaction.
2. Validate state transition and allocate the next strictly increasing per-run sequence.
3. Write operational state.
4. Write canonical `PipelineEvent` and `OutboxRecord` in the same SQLite transaction.
5. Commit SQLite.
6. Publisher appends canonical UTF-8 JSON to the active JSONL segment, flushes and `fsync`s, then records delivery acknowledgment.
7. Pending delivery is repaired by reconciliation.

No implementation may claim a filesystem append and SQLite commit are one atomic transaction.

Event IDs are deterministic from run ID, sequence, idempotency key, and payload hash. JSONL rotates at 64 MiB or 100,000 events. Closed segments record sequence range, event count, byte size, SHA-256, previous-segment hash, and close time.

Crash behavior:

- Before SQLite commit: no event exists; retry normally.
- After commit, before append: publish pending outbox row after restart.
- Partial final JSON line: truncate to last valid newline and republish.
- Complete append before acknowledgment: duplicate delivery is deduplicated by event ID.
- Different payload hashes for one idempotency key produce `EVENT.NONDETERMINISTIC_DUPLICATE` and stop automatic delivery.

Reconciliation repairs SQLite → JSONL exports and supports verified JSONL + retained payloads → new operational database rebuild. Live leases, active provider reservations, and retry timers rebuild as safe pending/reconciliation states rather than literal historical state.

---

## A9. Frozen benchmark, denominators, and ceilings

Every release candidate commits `BenchmarkManifest` (`CTR-BMM-001`) and `BenchmarkCase` (`CTR-BMK-001`) under one immutable Git tree. Development cases and holdout cases are disjoint. Layer B and holdout annotations require two independent reviewers and recorded adjudication.

Metric rules:

- Discovery counts normalized entities after deduplication.
- Additional duplicate predictions are false positives.
- Anchor correctness requires exact file instance, start byte, and end byte; overlap is incorrect.
- Required-scope unsupported results are false negatives in all-in metrics.
- Policy exclusions are reported in a separate coverage denominator and cannot improve primary scores.
- Report all-in and supported-subset metrics; supported-subset cannot replace failed all-in gates.
- Ambiguous truth is correct only with exact candidate set and `AMBIGUOUS` status.
- Multiple chains per Frontend request are distinct by seed, terminal set, and ordered required authoritative edge types.
- SQL metrics use promoted canonical `SqlFinding`, not raw candidates.
- Wilson 95% confidence intervals are reported. Discovery/route metrics require at least 100 positive truth entities; lineage/chain metrics require at least 50.

Existing percentage gates remain in force. Additional critical-state classification for ambiguity, conflict, and no-database terminals is 100% on annotated critical fixtures.

Baseline release profile:

- Linux x86-64, 8 vCPU, 32 GiB RAM, local NVMe-class storage, Python 3.12+, .NET 8, Node 22.
- Layer C: 5,000–15,000 files and 300,000–1,000,000 source lines.
- Snapshot + inventory: at most 5 minutes.
- Static extraction: at most 45 minutes with warm toolchains.
- Deterministic normalization, indexing, resolution, both projections, and JSON reports: at most 15 minutes excluding provider latency.
- Total orchestrator + sidecar peak RSS: at most 12 GiB.
- SQLite + retained structured stage payloads: at most 8 GiB excluding snapshot bytes and human reports.
- External-provider reserved exposure: at most USD 25.00.
- External input tokens: at most 5,000,000; output tokens: at most 1,000,000.
- Compatible completed requests repeated on cached rerun: zero.
- Pending queue depth: at most four times configured concurrency per worker class.

A release fails on any mandatory gate, critical false authoritative edge, inexact accepted anchor, or exceeded ceiling. Corpus changes require a new version and cannot hide regression.

---

## A10. Required pipeline order and acceptance additions

The normative run order is:

```text
CREATED
-> VALIDATING
-> SNAPSHOTTING
-> INVENTORYING
-> SCANNING_STRUCTURE
-> UNITIZING
-> EXTRACTING_STATIC_FACTS
-> CLASSIFYING
-> ANALYZING_UNITS
-> NORMALIZING
-> DISCOVERING_SQL
-> BUILDING_INDEXES
-> RESOLVING_CHAINS
-> VERIFYING_GAPS
-> PROJECTING_TARGETS
-> GENERATING_REPORTS
-> COMPLETED | PARTIAL_SUCCESS
```

Required fixtures now include Analysis Unit overlap/shared context/retry/conflict, all analyzer capability levels, Vue BOM/newline/Unicode/external-source cases, every transactional-outbox crash point, and false-complete/false-no-database chains.

Implementation planning may proceed only from the base specification plus this amendment. A future integrated specification may merge the text without changing these semantics.