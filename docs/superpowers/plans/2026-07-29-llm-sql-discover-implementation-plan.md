# LLM SQL Discover V1 — Architecture Horizon and Incremental Round Plan

> **For agentic workers:** Implement only the current approved Round and its active Issue. The capability horizon is not an executable backlog.

**Goal:** Build a deterministic V1 pipeline that snapshots Vue 2/C# repositories, produces exact analyzer-owned evidence, traces Frontend requests to database operations, normalizes SQL Server discovery, and independently generates MySQL and PostgreSQL conversion projections.

## Normative basis

- `docs/superpowers/specs/2026-07-29-fresh-context-sql-discovery-trace-design.md`
- `docs/superpowers/specs/2026-07-29-fresh-context-sql-discovery-trace-amendment-v1.1.md`
- `docs/superpowers/specs/2026-07-29-epic-anchored-incremental-decomposition-design.md`
- `docs/superpowers/plans/2026-07-29-file-boundary-execution-policy.md`
- `docs/superpowers/plans/llm-sql-discover/file-touch-map.json`
- root `AGENTS.md`
- Epic `#27`

**Expected technology horizon:** Python 3.12+, Pydantic v2, SQLAlchemy 2, Alembic, Typer, httpx, structlog, OpenTelemetry, pytest, Hypothesis, SQLGlot 27.x, openpyxl 3.1+, .NET 8/Roslyn, Node 22/TypeScript/Vitest, Vue 2 SFC compiler tooling, SQLite WAL. Exact dependencies and versions become executable only when validated in an approved Round.

## Fixed V1 constraints

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

## Operating model

Epic `#27` is the permanent anchor. Work is planned incrementally in Rounds of one to three Issues from the latest verified `main` state. Only one Issue may be active or queued for merge. Future Issues are not created until the current Round passes peer review, sequential merge, post-merge smoke verification, and discovery-ledger triage.

Issues `#12`–`#26` are superseded planning history. Their original analysis may inform future decomposition, but their file paths, interfaces, dependencies, and test commands are not executable instructions.

## Current approved Round

### Round R1

- Parent Epic: `#27`
- Planning anchor SHA: `4d65c683c8cc61d8de399479a4799560b7675685`
- Issue count: 1
- Sole planned Issue: `#11 — Project scaffold and contract registry`
- Native parent relationship: must be verified before implementation or covered by an explicit human-approved temporary exception in Epic `#27`
- Successor behavior: after PASS, merge, and smoke verification, enter Round Reassessment Mode; do not select archived Issue `#12`

### R1 capability slice

Round R1 establishes:

- Python project and dependency foundation;
- lifecycle envelopes and `RunRequest`/`RunSpec`;
- public and embedded contract ownership registry;
- compatibility and reason-code registries;
- stable CLI command-registry shell;
- deterministic validation and idempotent registry checks.

The exact R1 file boundaries and tests are authoritative in Issue `#11` and `file-touch-map.json`.

## Architecture Horizon

The horizon records capabilities required for V1. It does not pre-authorize Issues, files, interfaces, or branches.

### Foundation horizon

- lifecycle contracts and registries;
- durable operational state, transitions, leases, and idempotent results;
- transactional audit outbox, JSONL segmentation, reconciliation, and rebuild;
- immutable Git/content-addressed snapshots and deterministic inventory.

### Source-analysis horizon

- exact byte/line/Unicode/UTF-16 coordinates and Evidence Anchors;
- semantic-first C# Roslyn analysis with fact-level degradation;
- Vue 2 SFC analysis mapped back to original bytes;
- deterministic Analysis Units, aggregation, deduplication, and coverage decisions.

### Semantic-analysis horizon

- bounded provider-neutral per-unit LLM analysis;
- anchored finding normalization and canonical target-independent SQL;
- typed indexes and proof-classified resolver edges;
- request-body/DTO/argument/parameter/DB/SQL lineage;
- execution-chain completeness and conservative no-database proof.

### Delivery horizon

- independently versioned MySQL and PostgreSQL projections;
- resumable coordinator, scheduling, budgets, cancellation, invalidation, and observability;
- canonical JSON/JSONL reports and read-only HTML/XLSX/CLI projections;
- immutable layered benchmark and production release gate.

## Round planning contract

After the Round Transition Gate passes, the Decomposition Planner must:

1. record the latest verified `main` SHA;
2. inspect the actual codebase, tests, interfaces, and frozen hotspots;
3. triage the Discovery Ledger;
4. compare remaining horizon capabilities with the fixed Epic Definition of Done;
5. select the smallest coherent next capability slice;
6. propose one to three Issues;
7. create a file-touch conflict matrix before Issue creation;
8. define strict predecessors and native blocked-by relationships;
9. define complete validation, error, retry, tests, semantic review, discovery, and smoke-gate requirements;
10. obtain human approval;
11. create native sub-issues and activate only the first.

## Required executable Issue contract

Every executable Issue must include:

- Parent Epic and verified relationship status;
- Round ID and planning anchor SHA;
- capability slice, predecessor, and blocked-by relationships;
- start/merge gate;
- exclusive production and test write sets;
- read-only dependencies and frozen hotspots;
- Contract IDs;
- validation rules;
- error and state behavior;
- timeout, retry, cancellation, and idempotency policy;
- focused and regression tests with exact commands;
- fixture/coverage expectations;
- semantic-review checklist;
- discovery handling rules;
- post-merge smoke gate;
- commit boundary, non-goals, and forbidden edits.

## Completion contract for every Issue

Before an Issue can close:

1. eligibility and Round relationship gates pass;
2. all edits are inside declared write sets;
3. validation and negative tests pass;
4. error/state behavior is tested;
5. timeout/retry/cancellation behavior is tested or explicitly not applicable;
6. focused and regression suites pass with fresh evidence;
7. `git diff --check` and changed-file ownership audits pass;
8. independent semantic review has no unresolved Critical or Important finding;
9. the reviewed head SHA remains unchanged until merge;
10. post-merge smoke verification passes before another Issue starts.

The final Issue of a Round requires `PASS — READY FOR ROUND COMPLETION AND REASSESSMENT`.

## Discovery Ledger policy

- Required in-scope corrections remain in the active Issue when inside its acceptance criteria and write set.
- Out-of-scope blockers stop work and require Epic triage and approved dependency changes.
- Non-blocking discoveries remain ledger entries until the next Round.
- Normative discoveries require an approved specification or Definition-of-Done amendment.

## Semantic review baseline

Review must examine Round eligibility, source-coordinate fidelity, stale-state use, transaction/race/crash behavior, proof authority, duplicate and idempotency semantics, cache invalidation, route/DI/DTO/parameter lineage, SQL reconstruction, timezone/collation/case/null behavior, MySQL/PostgreSQL isolation, report provenance, and future-Round leakage.

## Round Transition Gate

No new Round is created until every current-Round Issue passes review, merges sequentially, passes post-merge smoke verification, leaves no Critical/Important findings or queued implementation PRs, records the resulting `main` SHA, and completes Discovery Ledger triage.

## Epic Completion Gate

Epic `#27` closes only when every fixed V1 Definition-of-Done item and required Architecture Horizon capability has evidence, every production and benchmark gate passes, no blocking discovery or Critical/Important finding remains, and final architecture-to-implementation traceability is complete. Zero open sub-issues is insufficient.
