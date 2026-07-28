# LLM SQL Discover V1 — Epic-Anchored File-Boundary Execution Policy

**Status:** Normative implementation-governance amendment  
**Applies to:** Epic `#27`, every approved implementation Round, and every executable sub-issue  
**Purpose:** Preserve file ownership, fresh-main planning, sequential integration, and semantic correctness while creating future Issues incrementally.

## 1. Permanent Epic anchor

Epic `#27` is the sole V1 project anchor. It owns the fixed mission, scope, non-goals, Definition of Done, Architecture Horizon, current Round, planning anchor SHA, Discovery Ledger, completed-round ledger, and Epic Completion Gate.

The Epic must not predeclare exact future files, interfaces, tests, or branches that have not been validated against the latest verified `main` state.

## 2. Incremental Round decomposition

Implementation is decomposed in Rounds. Each Round:

- is anchored to one exact verified `main` SHA;
- contains one to three native sub-issues;
- defines a strict execution order;
- has a Round-specific file-touch map;
- activates only one Issue at a time;
- closes with a Round completion report.

Round R1 contains only Issue `#11`. Its authoritative planning anchor SHA is recorded in Epic `#27`, Issue `#11`, and `file-touch-map.json` after governance migration reaches `main`.

Issues `#12`–`#26` are superseded planning history. Their capabilities remain in the Architecture Horizon, but their bodies, paths, and test commands are not executable instructions.

## 3. Round Transition Gate

A new Round must not be proposed or created until:

1. every current-Round Issue has independent Senior Expert Peer Review PASS;
2. every approved PR has merged sequentially;
3. post-merge smoke verification passes on the resulting `main`;
4. the resulting remote `main` SHA is recorded;
5. no Critical or Important finding remains;
6. no implementation PR remains open or queued;
7. the Discovery Ledger is triaged;
8. the V1 Definition of Done remains fixed or has an approved amendment;
9. governance and ownership maps are internally consistent.

## 4. Decomposition Planner rules

After the transition gate passes, the Planner must:

1. inspect the latest merged codebase and tests;
2. record the exact `planning_anchor_sha`;
3. compare remaining Architecture Horizon capabilities with the Epic Definition of Done;
4. choose the smallest coherent next capability slice;
5. propose no more than three Issues;
6. build a file-touch conflict matrix before Issue creation;
7. define strict predecessor and native blocked-by relationships;
8. specify validation, error, retry, tests, semantic review, discovery handling, and post-merge smoke gates;
9. obtain human approval;
10. create native sub-issues and activate only the first.

Archived Issue bodies may be consulted as historical analysis but must not be copied without revalidating every assumption against the planning anchor.

## 5. File-boundary and single-writer authority

An executable Issue is valid only when its production write set is exclusive within the active Round. The machine-readable authority is `docs/superpowers/plans/llm-sql-discover/file-touch-map.json`.

- Production and test write sets are declared separately.
- All undeclared files are read-only.
- A required cross-boundary change stops the task until the Issue and Round map are amended.
- Broad staging such as `git add -A` is prohibited.
- A hotspot has one owner and freezes after its owner merges unless an approved amendment changes the rule.
- No future-Round branch may be created before human approval of that Round.

## 6. Required executable Issue sections

Every executable sub-issue must contain:

1. Parent Epic and verified native relationship status.
2. Round ID and planning anchor SHA.
3. Capability slice, immediate predecessor, and native blocked-by dependencies.
4. Start and merge gates.
5. Exclusive production and test write sets.
6. Read-only dependencies and frozen hotspots.
7. Normative Contract IDs.
8. Input validation rules.
9. Error and state behavior.
10. Timeout, retry, cancellation, and idempotency policy.
11. Focused tests, regression tests, fixture expectations, and exact verification commands.
12. Semantic-review checklist.
13. Discovery handling rules.
14. Post-merge smoke gate.
15. Commit boundary, non-goals, and forbidden edits.

An Issue missing any required section is not executable.

## 7. Native relationship rule

A Markdown link to Epic `#27` is not equivalent to a native parent/sub-issue relationship.

- The Coding Agent and Reviewer must verify native parent and blocked-by relationships when tooling exposes them.
- When tooling cannot establish or verify the relationship, the limitation must be recorded explicitly.
- Implementation remains blocked unless Epic `#27` contains an explicit human-approved temporary exception for the named Issue and Round.
- Future Rounds must not silently replace native relationships with checklists.

## 8. Discovery classification

Discoveries are recorded before they become Issues:

- **Required in-scope correction:** implement inside the current Issue when required by acceptance criteria and inside its write set.
- **Out-of-scope blocker:** stop implementation, record it in the Epic Discovery Ledger, obtain human triage, then create or reorder a sub-issue only after approval.
- **Non-blocking discovery:** record it for the next Round; do not create an Issue immediately.
- **Normative discovery:** stop and require an approved specification, contract, scope, or Definition-of-Done amendment.

## 9. Review and merge protocol

For each active Issue:

1. create a fresh branch/worktree from eligible current `main`;
2. verify Round membership, planning-anchor ancestry, native parent, and blocked-by dependencies;
3. audit intended files against the Round map;
4. execute TDD and focused verification;
5. run required regression tests;
6. conduct independent semantic peer review;
7. fix every Critical and Important finding;
8. rerun fresh verification after any new commit;
9. merge as the only queued implementation PR;
10. run the post-merge smoke gate on `main`.

A reviewed head SHA must not change after PASS without a new review.

The final Issue of a Round receives `PASS — READY FOR ROUND COMPLETION AND REASSESSMENT`, not permission to implement the next horizon capability automatically.

## 10. Semantic review baseline

Reviewers inspect meaning, not only syntax:

- Round eligibility and planning-anchor ancestry;
- file ownership and frozen hotspots;
- exact-source coordinate fidelity;
- state, transaction, lease, retry, cancellation, race, and crash semantics;
- resolver proof authority and ambiguity preservation;
- SQL reconstruction without guessed fragments;
- cache keys and invalidation boundaries;
- request/DTO/parameter lineage;
- target-specific null, collation, case, timezone, and pagination behavior;
- MySQL/PostgreSQL isolation;
- reproducible report provenance;
- discovery classification and future-Round leakage.

## 11. Governance validation

Governance self-review fails when:

- an archived or future-Round Issue is selectable;
- a Round lacks an exact planning anchor SHA;
- more than three Issues are planned in a Round;
- more than one Issue or PR is active;
- two active-Round Issues own the same production path;
- an Issue lacks required execution-contract sections;
- a native relationship is claimed without verification;
- an Issue has no invalid-input/error expectation;
- semantic review is reduced to compile/lint/test status;
- a new Round is created before the transition gate passes.

## 12. Epic Completion Gate

Zero open sub-issues does not complete Epic `#27`. The Epic closes only when the fixed V1 Definition of Done, all required Architecture Horizon capabilities, production acceptance gates, exact-source gates, resolver-authority gates, target-isolation gates, migration checks, and release benchmark have evidence and no blocking discovery or Critical/Important finding remains.
