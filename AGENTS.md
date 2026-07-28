# AGENTS.md

## Project mission

Build the V1 Fresh-Context SQL Discovery & Trace pipeline defined by the normative specification, amendment, implementation plan, and GitHub Epic. V1 discovers and traces source behavior and produces MySQL/PostgreSQL conversion projections. It does not execute APIs/databases or rewrite source code.

## Read before any work

1. `docs/superpowers/specs/2026-07-29-fresh-context-sql-discovery-trace-design.md`
2. `docs/superpowers/specs/2026-07-29-fresh-context-sql-discovery-trace-amendment-v1.1.md`
3. `docs/superpowers/plans/2026-07-29-llm-sql-discover-implementation-plan.md`
4. `docs/superpowers/plans/2026-07-29-file-boundary-execution-policy.md`
5. `docs/superpowers/plans/llm-sql-discover/file-touch-map.json`
6. The assigned GitHub Issue and all of its dependencies

The specification and amendment are normative. An Issue or implementation detail may not silently change contract semantics.

## Strict sequential workflow

- Implement Issues in numeric order: `#11 -> #12 -> ... -> #26`.
- Only one implementation Issue may be active at a time.
- Merge the current Issue into `main` before starting the next Issue.
- After every merge, delete or retire the completed worktree/branch and create or rebase the next branch from the new `main`.
- Do not maintain a queue of implementation branches based on stale `main`.
- Each Issue must be independently reviewable and end at its declared commit boundary.

## File-boundary and single-writer rules

- The Issue's `exclusive_write_set` is the complete set of production files it may create or modify.
- Files outside the declared write set are read-only.
- A required undeclared edit stops the task. Amend the Issue and `file-touch-map.json` before coding.
- Never use broad staging such as `git add -A`; stage explicit paths from the Issue.
- A shared/hotspot file has one owner. Do not edit it from another Issue.
- `src/sqltrace/cli.py` is owned by Issue #11 and becomes a stable registry shell. Later commands are added under `src/sqltrace/commands/`.
- Configuration is split by subsystem under `src/sqltrace/config/`; do not recreate a shared `config.py` hotspot.
- `pyproject.toml`, contract registries, root governance files, and the initial migration are frozen after their owner Issue. Later changes require an explicit amendment or a new migration file.

## Architecture invariants

- Static analyzers own source coordinates and Evidence Anchors.
- One LLM request contains one Analysis Unit from one file and no rolling history.
- C# analysis is semantic-first with fact-level degradation.
- Vue parser-local offsets must round-trip to original snapshot bytes before persistence.
- SQLite state and outbox rows commit atomically.
- LLM output is advisory/non-authoritative until schema, identity, anchor, ownership, and invariant validation pass.
- Resolver confidence cannot override missing, ambiguous, or conflicting deterministic proof.
- SQL candidates must be promoted through normalization before conversion.
- MySQL and PostgreSQL projections are independently versioned and invalidated.
- Reports are read-only projections and must not trigger analyzer/provider calls.

## Required Issue contract

Every implementation Issue must state:

- exclusive production write set and test write set;
- predecessor and start gate;
- input validation rules;
- error and state-transition behavior;
- timeout, cancellation, and retry policy, including when retry is not applicable;
- focused test commands and bundle regression commands;
- minimum coverage/fixture expectations;
- semantic-review checklist;
- explicit non-goals and forbidden edits.

## Validation and error behavior

- Reject invalid identities, ranges, schema versions, and state transitions deterministically.
- Preserve reason codes and diagnostics; do not coerce unknown or conflicting data into a successful state.
- Retry only transient operations explicitly listed by the Issue. Deterministic validation failures are not retryable.
- Tests must cover success, invalid input, terminal failure, retryable failure where applicable, and idempotent repeat behavior.

## Testing

Use TDD: failing test, observed failure, minimal production-capable implementation, focused pass, bundle regression pass.

Before merge run:

1. Every command listed in the Issue.
2. The owning bundle test suite.
3. Contract/registry checks if public contracts are involved.
4. `git diff --check`.
5. A clean-status check limited to declared files.

Do not claim completion from partial tests.

## Semantic peer review

Review must go beyond compile/lint/test status. Check at minimum:

- source byte/line/Unicode coordinate correctness;
- stale snapshot or stale stage-result use;
- transaction, lease, crash, cancellation, and race behavior;
- incorrect promotion of candidate/ambiguous evidence to authoritative evidence;
- duplicate/dedup and idempotency semantics;
- cache fingerprint and invalidation boundaries;
- route, DI, DTO, and parameter-lineage meaning;
- timezone, collation, case sensitivity, null semantics, and target-dialect assumptions;
- cross-target contamination between MySQL and PostgreSQL;
- report provenance and accidental provider/analyzer calls.

Critical and Important review findings must be fixed before merge. Minor findings must be recorded or fixed; they may not be silently ignored.

## Coding conventions

- Python 3.12+, typed public APIs, Pydantic v2 contracts, SQLAlchemy 2/Alembic state.
- Keep files focused by responsibility. Avoid generic `utils.py` and cross-layer helper dumping grounds.
- Public names and contract fields must match the specification exactly.
- Use deterministic IDs and canonical serialization where required.
- Keep stdout machine-readable for JSON/JSONL CLI modes; progress and diagnostics go to stderr.
- Do not add V2 scope, API execution, database execution, source rewriting, or automatic PR creation.

## Git and merge discipline

- Branch from current `main` only after the predecessor Issue is merged.
- Rebase before final verification if `main` changed.
- Merge one Issue at a time.
- After merge, rerun the predecessor-to-current bundle smoke gate on `main` before opening the next Issue.
- Do not resolve semantic conflicts by choosing one side of a merge without re-running the relevant acceptance tests.
