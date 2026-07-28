# LLM SQL Discover V1 Implementation Plan Bundle

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` task-by-task. Every task follows TDD and ends in a reviewable commit.

**Goal:** Build a deterministic V1 pipeline that snapshots Vue 2/C# repositories, produces exact analyzer-owned evidence, traces Frontend requests to database operations, normalizes SQL Server discovery, and independently generates MySQL and PostgreSQL conversion projections.

**Normative basis:** Base Architecture and Contract Specification plus `2026-07-29-fresh-context-sql-discovery-trace-amendment-v1.1.md`.

**Tech stack:** Python 3.12+, Pydantic v2, SQLAlchemy 2, Alembic, Typer, httpx, structlog, OpenTelemetry, pytest, Hypothesis, SQLGlot 27.x, openpyxl 3.1+, .NET 8/Roslyn, Node 22/TypeScript/Vitest, Vue 2 SFC compiler tooling, SQLite WAL.

## Global constraints

- V1 includes Discovery, Trace, and Conversion only.
- Exact byte-range Evidence Anchors come only from analyzers.
- Structural scanning precedes deterministic unitization.
- One LLM request contains one Analysis Unit from one file and no rolling history.
- C# is semantic-first with fact-level degradation.
- Vue parser offsets are translated and round-tripped to original SFC bytes.
- Operational state and outbox rows commit in one SQLite transaction.
- SQL candidates pass `CTR-SNR-001` before `CTR-SQL-001` exists.
- Resolver authority follows the proof matrix; LLM verification is advisory.
- MySQL and PostgreSQL projections are independently invalidated.
- Report regeneration performs no analyzer or provider calls.
- Release requires every benchmark, migration, privacy, performance, and cost gate.

## Bundle A — Foundation, state, and snapshot

### Task 1 — Project scaffold and contract registry

Creates lifecycle envelopes, `RunRequest`, `RunSpec`, contract/reason-code registries, compatibility matrix, JSON Schema checks, and Python dependency constraints.

Acceptance:

- no source-derived contract can exist without a real snapshot ID;
- every public/embedded contract is registered;
- unknown incompatible contracts are rejected or quarantined;
- migration behavior for the pre-envelope draft is tested.

### Task 2 — SQLite operational state and transitions

Creates Alembic migrations, run/file/unit/finding/edge/chain/projection tables, state-transition maps, leases, compare-and-set claims, fingerprints, and idempotent stage results.

Acceptance:

- invalid transitions fail transactionally;
- duplicate compatible completion is a no-op;
- same deterministic input with different output creates a nondeterminism diagnostic;
- stale entities cannot feed downstream stages.

### Task 3 — Transactional outbox and audit rebuild

Implements per-run sequences, canonical event rows, outbox publisher, 64 MiB/100,000-event JSONL rotation, segment hash chain, tail repair, reconciliation, and offline rebuild.

Acceptance:

- all specified crash points recover without event loss;
- duplicate delivery is idempotently detected;
- partial final lines are repaired;
- verified segments and retained payloads rebuild derived operational state without provider calls.

### Task 4 — Immutable snapshot, inventory, and bootstrap CLI

Implements Git-tree and content-addressed snapshots, original-byte storage, encoding/newline metadata, root containment, deterministic file IDs, and `init-run`, `snapshot`, and `reconcile` commands.

Acceptance:

- changing the working tree after snapshot does not change analyzed bytes;
- Git mode never mixes commit and mutable bytes;
- duplicate-content files at different paths have distinct file-instance IDs;
- every included file has an inventory/coverage record.

## Bundle B — Source fidelity and analyzers

### Task 5 — Source coordinate engine, anchors, and sidecar protocol

Implements byte/Unicode/UTF-16 indexes, line/column reconstruction, excerpt hashes, anchor validation, correlated JSONL sidecar requests, timeout/restart behavior, and exact-source fixture coverage.

Acceptance:

- BOM, CRLF, mixed newline, astral Unicode, and combining-character mappings are byte-exact;
- parser-local coordinates never enter persisted anchors;
- protocol correlation mismatches and invalid ranges fail deterministically.

### Task 6 — Semantic-first C# Roslyn analyzer

Implements solution/project loading, structural bundles, exact declarations/routes/calls/strings/DB/DTO/DI facts, compilation-profile fingerprints, and fact-level capability degradation.

Acceptance:

- overload-specific calls are authoritative only with semantic proof;
- missing references downgrade affected facts rather than all facts;
- syntax fallback never claims semantic call authority;
- complete, partial, syntax-only, and unsupported fixtures pass.

### Task 7 — Vue 2 analyzer with original-byte SFC mapping

Implements SFC block maps, template handlers, Options API symbols, imports, Axios/fetch/custom client calls, assignments/object shapes, external `src` provenance, and byte mapping.

Acceptance:

- TypeScript UTF-16 and template offsets round-trip to original bytes;
- malformed/recovered nodes without proven mapping create no exact finding;
- `script setup` is explicitly unsupported for V1 semantic facts;
- conditional/spread body fields preserve presence semantics.

### Task 8 — Deterministic unitization, aggregation, and classification

Consumes `FileStructureBundle`, creates whole-file or symbol units, separates primary/context anchors, aggregates retries, detects conflicting duplicate payloads, and emits `FULL_LLM`, `STATIC_ONLY`, `SKIPPED_IRRELEVANT`, or `UNSUPPORTED`.

Acceptance:

- same inputs produce identical unit boundaries and IDs;
- primary ranges do not overlap or cut symbols;
- context anchors cannot originate findings;
- file completion is derived solely from required unit and aggregation states.

## Bundle C — Analysis, normalization, and resolver

### Task 9 — Provider-neutral per-unit LLM gateway

Implements local/private, external-redacted, and static-only modes, structured-output schema, instruction isolation, anchor/identity validation, cache fingerprints, retry classes, cost reservation, timeout-after-dispatch handling, and retention policy.

Acceptance:

- every request contains one unit and no conversation history;
- unknown/cross-unit anchors are rejected;
- redaction preserves offsets and sends zero annotated secrets externally;
- reserved exposure prevents new dispatch beyond the configured cap.

### Task 10 — Finding normalization and canonical SQL promotion

Normalizes Frontend/Backend/DB findings; merges deterministic duplicates; introduces `SqlCandidate`, `SqlNormalizationResult`, reconstruction with typed unknown placeholders, false-positive rejection, conflict quarantine, and canonical `SqlFinding`.

Acceptance:

- LLM-only or unanchored SQL cannot be promoted;
- canonical SQL requires a DB operation or supported standalone resource;
- unknown/dynamic fragments are not guessed;
- conversion consumes only promoted canonical SQL.

### Task 11 — Typed indexes and resolver proof matrix

Builds route, symbol, call, DTO, DI, body, DB, and SQL indexes; implements authority/status separation and proof rules for routes, calls, DI, request binding, field mapping, parameters, SQL ownership, and schema references.

Acceptance:

- syntax name equality and route suffix are candidate-only;
- exact verb/route/prefix and semantic calls can be authoritative;
- multiple applicable targets are ambiguous;
- contradictory authoritative facts are conflict, never score-selected.

### Task 12 — Request lineage, chains, no-database proof, and focused verification

Resolves raw body → wire field → DTO/parameter → service/repository parameters → DB binding → SQL placeholder; computes chain state; proves conservative no-database terminals; builds compact advisory verification requests.

Acceptance:

- complete chains require all required edges authoritative/resolved;
- unresolved transformations preserve partial/conditional status;
- unresolved calls prevent no-database terminals;
- LLM verification cannot promote an edge directly.

## Bundle D — Projections, coordinator, CLI, and release

### Task 13 — Schema context and independent target projections

Loads optional SQL Server schema metadata, target runtime profiles, SQLGlot parsing, deterministic MySQL/PostgreSQL rewrites, target diagnostics, mandatory risks, and target-specific fingerprints.

Acceptance:

- MySQL rule changes do not stale PostgreSQL projections and vice versa;
- target parser acceptance is 100% for syntax-valid status;
- unsupported constructs and dynamic identifiers require manual review;
- schema changes do not trigger source reanalysis.

### Task 14 — End-to-end coordinator, resume, invalidation, budgets, and observability

Implements normative phase graph, bounded queues, leases, cancellation, parent-child reuse, stage fingerprints, fine-grained invalidation, OpenTelemetry metrics/traces, cost pause, and resume.

Acceptance:

- structural scan precedes unitization and SQL discovery precedes indexes/resolver;
- compatible completed stages are not repeated after interruption;
- cancellation and budget pause create terminal audit events;
- every log/metric carries run/file/unit/finding/chain correlation where applicable.

### Task 15 — Canonical artifacts, reports, and complete CLI

Implements canonical JSON/JSONL exports, artifact hashes/provenance, HTML/XLSX read-only views, `run`, `resume`, `inspect`, `report`, `reconcile`, `rebuild`, and `benchmark` commands, stdout/stderr discipline, and exit codes.

Acceptance:

- report regeneration creates zero provider/analyzer calls;
- every human view derives from canonical data;
- inspect commands expose evidence, unresolved reasons, and provenance;
- complete, partial, paused, validation, and fatal states have distinct exit codes.

### Task 16 — Frozen benchmark corpus and production release gate

Creates Layer A exact fixtures, dual-reviewed Layer B/holdout annotations, deterministic Layer C generation with seed `20260729` (6,000 files, 400,000–600,000 lines, 70/30 C# to Vue/JS/TS), denominator engine, Wilson intervals, migration/privacy/crash tests, and release runner.

Acceptance:

- all base-spec and amendment gates pass;
- duplicate predictions and required-scope unsupported cases affect metrics correctly;
- accepted anchors are 100% byte-exact;
- critical false authoritative edges are zero;
- performance, memory, token, and USD 25.00 exposure ceilings pass on the declared runtime profile.

## Dependency graph

```text
1 -> 2 -> 3
1 -> 4
1 -> 5 -> 6
5 -> 7
5,6,7 -> 8
2,3,4,8 -> 9
6,7,9 -> 10
6,7,10 -> 11
9,10,11 -> 12
10 -> 13
2,3,4,8,9,10,11,12,13 -> 14
12,13,14 -> 15
1..15 -> 16
```

## Review gates

- Bundle A: lifecycle, migrations, state transitions, outbox crash semantics.
- Bundle B: byte-exact fidelity, capability degradation, unit ownership.
- Bundle C: false-authoritative-edge risk, SQL promotion, chain completeness.
- Bundle D: full compatibility, benchmark, privacy, determinism, performance, and cost gates.

The GitHub Epic and task issues are the execution ledger for this plan. Each task issue contains exact files, interfaces, TDD steps, commands, dependencies, and commit boundary.