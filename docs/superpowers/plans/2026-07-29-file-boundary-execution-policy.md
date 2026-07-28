# LLM SQL Discover V1 — File-Boundary and Sequential Execution Policy

**Status:** Normative implementation-planning amendment  
**Applies to:** GitHub Issues #11–#27 and the V1 Implementation Plan  
**Purpose:** Prevent file ownership collisions, stale parallel branches, hidden shared-file edits, and semantic drift between coding-agent sessions.

## 1. Decomposition rule

Implementation work is decomposed by both capability and exact file/module ownership. An Issue is valid only when its production write set is exclusive. The machine-readable authority is `docs/superpowers/plans/llm-sql-discover/file-touch-map.json`.

A task may read dependencies from prior tasks, but it may not modify their files. If implementation reveals a required cross-boundary change, work stops until the plan, Issue body, and ownership map are amended.

## 2. Resolved hotspots

The original plan had one direct overlap and one latent hotspot:

- `src/sqltrace/cli.py` was created by Task 04 and modified by Task 15.
- a shared `src/sqltrace/config.py` would accumulate snapshot, LLM, target, and runtime policy.

The revised boundary is:

- Issue #11 owns the stable `src/sqltrace/cli.py` registry shell and `src/sqltrace/commands/registry.py`.
- Issue #14 adds only `src/sqltrace/commands/bootstrap.py`.
- Issue #25 adds only `src/sqltrace/commands/reporting.py`, `inspection.py`, and `benchmark.py`.
- Configuration is split into `config/base.py`, `snapshot.py`, `llm.py`, `targets.py`, and `runtime.py`, each owned by one Issue.

## 3. Strict total merge order

The V1 implementation merge order is:

```text
#11 -> #12 -> #13 -> #14 -> #15 -> #16 -> #17 -> #18
    -> #19 -> #20 -> #21 -> #22 -> #23 -> #24 -> #25 -> #26
```

Only one implementation Issue may be active. A successor branch is created only after the predecessor is merged and the post-merge smoke gate passes on `main`.

This total order is stricter than the dependency DAG by design. It trades parallel throughput for lower conflict and semantic-drift risk during initial architecture construction.

## 4. Single-writer hotspots

| File or family | Owner | Rule after owner merge |
|---|---:|---|
| `AGENTS.md` | planning governance | Change only through explicit governance amendment. |
| `pyproject.toml` | #11 | Frozen; later dependency change requires an amended Issue. |
| `src/sqltrace/cli.py` | #11 | Frozen registry shell; add command modules instead. |
| `contracts/compatibility-matrix.json` | #11 | Normative change only. |
| `contracts/reason-codes.json` | #11 | Normative reason-code change only. |
| `migrations/versions/0001_initial_state.py` | #12 | Frozen; later schema changes use a new migration. |
| `src/sqltrace/state/models.py` | #12 | Later tasks consume the schema; no silent table additions. |
| `benchmarks/v1/benchmark-manifest.yaml` | #26 | Release corpus authority. |

## 5. Required Issue sections

Each Issue must include:

1. Merge predecessor and start gate.
2. Exclusive production and test write sets.
3. Read-only dependencies.
4. Input validation rules.
5. Error/state behavior.
6. Timeout/retry/cancellation policy or an explicit “not applicable”.
7. Focused tests and bundle regression gate.
8. Coverage/fixture minimums.
9. Semantic-review checklist.
10. Non-goals and forbidden edits.

A global rule is not a substitute for issue-specific behavior. Each Issue must state the failure modes relevant to its subsystem.

## 6. Review and merge protocol

For each Issue:

1. Create a fresh branch/worktree from current `main`.
2. Verify the predecessor Issue is closed and merged.
3. Confirm all intended files are inside the declared write set.
4. Execute TDD and focused verification.
5. Run the bundle regression suite.
6. Conduct semantic peer review.
7. Fix all Critical and Important findings.
8. Rebase on current `main` if it changed; rerun verification.
9. Merge to `main` as the only queued implementation merge.
10. Run the post-merge smoke gate on `main` before starting the next Issue.

## 7. Semantic review baseline

Reviewers must inspect meaning, not only syntax:

- exact-source coordinate fidelity;
- state, transaction, lease, retry, and crash semantics;
- resolver proof authority and ambiguity preservation;
- SQL reconstruction without guessed fragments;
- cache keys and invalidation boundaries;
- request/DTO/parameter lineage correctness;
- target-specific null, collation, case, timezone, and pagination behavior;
- isolation between MySQL and PostgreSQL projections;
- reproducible report provenance.

## 8. Governance validation

Planning self-review must fail when:

- two Issues own the same production path;
- an Issue lacks required execution-contract sections;
- the numeric merge chain has a gap or cycle;
- a hotspot is edited outside its owner rule;
- an Issue has no invalid-input/error test expectation;
- semantic review is reduced to compile/lint/test status.
