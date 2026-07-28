# LLM SQL Discover V1 Implementation Plan Bundle

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:subagent-driven-development` or `superpowers:executing-plans` task-by-task. Every task follows TDD and ends in a reviewable commit.

**Goal:** Build a deterministic V1 pipeline that snapshots Vue 2/C# repositories, produces exact analyzer-owned evidence, traces Frontend requests to database operations, normalizes SQL Server discovery, and independently generates MySQL and PostgreSQL conversion projections.

**Normative basis:**

- `docs/superpowers/specs/2026-07-29-fresh-context-sql-discovery-trace-design.md`
- `docs/superpowers/specs/2026-07-29-fresh-context-sql-discovery-trace-amendment-v1.1.md`
- `docs/superpowers/plans/2026-07-29-file-boundary-execution-policy.md`
- `docs/superpowers/plans/llm-sql-discover/file-touch-map.json`
- root `AGENTS.md`

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

## File-boundary and merge governance

- Issues merge in strict numeric order: `#11 -> #12 -> ... -> #26`.
- Only one implementation Issue may be active at a time.
- The successor starts only after the predecessor is merged and its branch/worktree is recreated or rebased from current `main`.
- Each Issue has an exclusive production write set in `file-touch-map.json`; undeclared production edits are forbidden until the plan and Issue are amended.
- `src/sqltrace/cli.py`, `pyproject.toml`, contract registries, root governance files, and the initial migration are single-writer hotspots and freeze after their owner Issue.
- CLI commands are isolated under `src/sqltrace/commands/`; configuration is isolated under `src/sqltrace/config/` by subsystem.
- Every Issue states validation, error, timeout/retry, test, coverage, semantic-review, and non-goal constraints.

## Sequential task ledger

| Issue | Task | Exclusive module boundary |
|---:|---|---|
| #11 | Project scaffold, lifecycle contracts, registries, stable CLI shell | `pyproject.toml`, `contracts/`, `src/sqltrace/contracts/`, `src/sqltrace/cli.py`, command registry |
| #12 | SQLite operational state | initial migration and `src/sqltrace/state/{database,models,transitions,repository}.py` |
| #13 | Transactional outbox and rebuild | event/outbox/segment/reconcile/rebuild modules |
| #14 | Immutable snapshot and bootstrap commands | `snapshot/`, `config/{base,snapshot}.py`, `commands/bootstrap.py` |
| #15 | Coordinates, anchors, analyzer protocol | source coordinate modules and analyzer protocol/supervisor |
| #16 | C# analyzer | C# sidecar and C# client only |
| #17 | Vue analyzer | Vue sidecar and Vue client only |
| #18 | Unitization, aggregation, classification | unitizer/aggregation/classification and analysis contract |
| #19 | Per-unit LLM gateway | `config/llm.py`, `llm/`, `pipeline/per_unit.py` |
| #20 | Finding normalization and canonical SQL | normalization, SQL candidate/reconstruction/normalization, finding/SQL contracts |
| #21 | Typed indexes and proof matrix | resolver index/proof/route/symbol/DI/edge modules |
| #22 | Lineage and chains | resolver body/lineage/chain/no-database/verification and chain contract |
| #23 | Target projections | `config/targets.py` and projection/schema/validation SQL modules |
| #24 | Coordinator and runtime policy | `config/runtime.py`, coordinator/scheduler/fingerprint/invalidation, observability |
| #25 | Reports and CLI command modules | `commands/{reporting,inspection,benchmark}.py`, `reporting/` |
| #26 | Frozen benchmark and release gate | `benchmarks/v1/`, `benchmark/`, release tools/tests |

## Dependency and merge order

The architectural DAG remains useful for understanding dependencies, but implementation and merge use this strict total order:

```text
#11 -> #12 -> #13 -> #14 -> #15 -> #16 -> #17 -> #18
    -> #19 -> #20 -> #21 -> #22 -> #23 -> #24 -> #25 -> #26
```

## Required completion contract for every task

Before an Issue can close:

1. All edits are inside its declared write set.
2. Input validation and invalid-input tests pass.
3. Error/state behavior is tested.
4. Timeout/retry/cancellation behavior is tested or explicitly declared not applicable.
5. Focused tests and the owning bundle regression suite pass.
6. `git diff --check` passes.
7. Semantic peer review finds no unresolved Critical or Important issue.
8. The branch is based on current `main` and is the only queued implementation merge.
9. Post-merge smoke verification passes on `main` before the successor starts.

## Semantic review baseline

Review must examine source-coordinate fidelity, stale-state use, transaction/race/crash behavior, proof authority, duplicate and idempotency semantics, cache invalidation, route/DI/DTO/parameter lineage, SQL reconstruction, timezone/collation/case/null behavior, MySQL/PostgreSQL isolation, and report provenance.

## Bundle review gates

- Bundle A (#11–#14): lifecycle, migrations, state transitions, outbox crash semantics, immutable snapshot fidelity.
- Bundle B (#15–#18): byte-exact fidelity, capability degradation, unit ownership and deduplication.
- Bundle C (#19–#22): provider isolation, SQL promotion, false-authoritative-edge prevention, chain completeness.
- Bundle D (#23–#26): independent target projections, resume/invalidation, canonical reporting, benchmark/privacy/performance/cost gates.

The GitHub Epic and task Issues are the execution ledger. The exact per-Issue file sets are authoritative in `file-touch-map.json` and the Issue body.
