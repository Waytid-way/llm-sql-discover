# Epic-Anchored Incremental Decomposition Design

Status: Approved approach, pending user review of this written design before repository migration

Repository: `Waytid-way/llm-sql-discover`

Parent Epic: `#27`

Initial executable Issue: `#11`

## 1. Purpose

This document defines the governance model for replacing the current fully pre-created implementation backlog with an Epic-anchored, round-based, incremental decomposition workflow.

The goal is to preserve the fixed V1 architecture and Definition of Done while ensuring that executable sub-issues are generated from the latest verified `main` state instead of from assumptions made before implementation exists.

## 2. Decision

The repository SHALL adopt Approach B: True Incremental Reset.

The migration SHALL:

1. Keep Epic `#27` as the permanent V1 anchor.
2. Keep Issue `#11` as the only executable implementation Issue in Round 1.
3. Close Issues `#12` through `#26` with state reason `not_planned` and a supersession comment preserving their role as planning history.
4. Retain their intended capabilities in an Architecture Horizon rather than treating their current file paths and task descriptions as executable requirements.
5. Create later implementation sub-issues only after the current round has passed review, merge, and post-merge verification.
6. Limit each future round to no more than three native sub-issues.
7. Allow only one implementation Issue to be active or queued for merge at any time.

## 3. Fixed Epic Anchor

Epic `#27` remains the sole project-level parent and SHALL contain or link to:

- V1 mission and scope;
- explicit non-goals;
- Architecture and Contract Specification;
- Normative Amendment v1.1;
- immutable V1 Definition of Done;
- architecture invariants;
- release and benchmark gates;
- current round identifier;
- current planning anchor SHA;
- current active sub-issue;
- completed round ledger;
- discovery ledger;
- Architecture Horizon;
- change-control rules;
- Epic Completion Gate.

The Epic SHALL NOT predeclare exact future implementation files, interfaces, branches, or tests that have not yet been validated against the latest merged codebase.

## 4. Architecture Horizon

The existing implementation plan remains authoritative only as a capability horizon.

It defines capabilities that V1 is expected to deliver, including:

### Foundation horizon

- lifecycle contracts and registries;
- operational state;
- transactional audit outbox and rebuild;
- immutable snapshots and inventory.

### Source-analysis horizon

- exact source coordinates and evidence anchors;
- semantic-first C# analysis;
- Vue 2 original-byte mapping;
- deterministic analysis units and aggregation.

### Semantic-analysis horizon

- bounded per-unit LLM analysis;
- canonical finding and SQL normalization;
- typed indexes and proof-classified resolution;
- request lineage, execution chains, and no-database proof.

### Delivery horizon

- independent MySQL and PostgreSQL projections;
- resumable orchestration and invalidation;
- canonical reports and CLI surfaces;
- frozen benchmark and production release gate.

The horizon SHALL NOT be used as an instruction to implement archived Issues `#12`–`#26` verbatim.

## 5. Round Model

A Round is a bounded planning and delivery unit anchored to one verified `main` commit.

Each Round SHALL define:

- `round_id`;
- `planning_anchor_sha`;
- parent Epic number;
- one to three native sub-issues;
- strict execution order;
- per-Issue exclusive production write sets;
- test write sets;
- read-only dependencies and frozen hotspots;
- blocked-by relationships;
- round acceptance gate;
- round completion report.

A Round MAY contain fewer than three sub-issues when the next capability boundary remains uncertain.

Round 1 SHALL contain only Issue `#11`.

## 6. Mandatory Round Transition Gate

A new Round MUST NOT be planned or created until all conditions below are true:

1. Every sub-issue in the current Round has received `PASS` from independent Senior Expert Peer Review.
2. Every approved PR in the current Round has been merged sequentially.
3. The post-merge smoke gate has passed on the resulting `main` commit.
4. The remote `main` SHA has been recorded.
5. No Critical or Important review finding remains unresolved.
6. No implementation PR from the current Round remains open or queued.
7. The discovery ledger has been triaged.
8. The fixed V1 Definition of Done remains unchanged, or an approved normative amendment exists.
9. The repository governance and file ownership maps are internally consistent.

Failure of any condition blocks creation of the next Round.

## 7. Incremental Decomposition Workflow

After the Round Transition Gate passes, the Decomposition Planner SHALL:

1. Clone or fetch the latest `main`.
2. Record the exact `planning_anchor_sha`.
3. Read Epic `#27`, the specification, amendment, governance documents, completed round reports, and discovery ledger.
4. Inspect the actual codebase and test surfaces created so far.
5. Identify current frozen hotspots and file ownership constraints.
6. Evaluate remaining Architecture Horizon capabilities against the Epic Definition of Done.
7. Select the smallest coherent next capability slice.
8. Propose no more than three implementation sub-issues.
9. Produce a file-touch conflict map before issue creation.
10. Define strict predecessor and blocked-by relationships.
11. Define validation, error, timeout/retry, testing, semantic review, and post-merge smoke requirements for every issue.
12. Present the Round proposal for human approval.
13. Create native sub-issues under Epic `#27` only after approval.
14. Activate only the first issue in the Round.

The Planner SHALL NOT copy an archived issue body without revalidating every path, interface, dependency, acceptance criterion, and test command against the planning anchor SHA.

## 8. Required Native Sub-Issue Contract

Every executable sub-issue SHALL include:

- Parent Epic: `#27`;
- Round ID;
- Planning Anchor SHA;
- capability slice;
- immediate predecessor;
- native blocked-by relationships;
- merge gate;
- exclusive production write set;
- test write set;
- read-only dependencies;
- frozen hotspots;
- normative Contract IDs;
- required work;
- input validation rules;
- error and state behavior;
- timeout, retry, cancellation, and idempotency policy;
- required tests and exact verification commands;
- semantic review checklist;
- discovery handling rules;
- post-merge smoke gate;
- commit boundary;
- explicit non-goals.

An issue without these fields is not executable.

## 9. Single-Writer and Sequential Execution

The following invariants remain mandatory:

- only one implementation Issue may be active;
- only one implementation PR may be queued for merge;
- an Issue branch must be created from `main` after its predecessor is merged and verified;
- no future-round branch may exist before that Round is approved;
- every production file has one writer during an active Issue;
- undeclared production edits stop the task;
- frozen hotspots may change only through an approved governance or architecture amendment;
- the next Issue may not start until review PASS, merge, and post-merge smoke verification complete.

Incremental planning does not permit parallel implementation.

## 10. Discovery Classification

Discoveries SHALL be recorded before being converted into issues.

### 10.1 Required in-scope correction

A correction required by the current acceptance criteria and inside the declared write set SHALL be implemented in the current Issue.

### 10.2 Out-of-scope blocker

A discovery that blocks the current Issue and requires an undeclared file, contract, or architectural change SHALL:

1. stop implementation;
2. be recorded in the Epic discovery ledger;
3. receive human triage;
4. become a native sub-issue only after approval;
5. be inserted as an explicit dependency when required.

### 10.3 Non-blocking discovery

A useful but non-blocking improvement SHALL be recorded in the discovery ledger and reconsidered during the next Round planning cycle. It SHALL NOT automatically create an issue.

### 10.4 Normative discovery

A discovery that changes the Architecture Specification, Contract semantics, V1 scope, or Definition of Done SHALL require a reviewed normative amendment before implementation planning continues.

## 11. Migration of Existing Issues

### 11.1 Issue #11

Issue `#11` remains open and becomes:

- Round: `R1`;
- Planning Anchor SHA: the verified migration-time `main` SHA;
- Parent Epic: `#27`;
- Status: the sole executable Issue;
- Successor behavior: after PASS, merge, and smoke verification, enter Round Reassessment instead of selecting `#12` automatically.

Its current file-boundary and acceptance criteria remain subject to a final anchor-SHA consistency check before implementation starts.

### 11.2 Issues #12–#26

Issues `#12` through `#26` SHALL be closed with state reason `not_planned`.

Each SHALL receive a comment containing:

- that it is superseded by Epic-Anchored Incremental Decomposition;
- that it is preserved as planning history;
- that its capability remains represented in the Architecture Horizon;
- that it must not be implemented directly;
- that future work will be regenerated from the latest verified `main` state;
- a link to this design document and Epic `#27`.

No issue content SHALL be deleted.

### 11.3 Epic #27

Epic `#27` SHALL be revised to remove the fixed `#11 -> #26` executable sequence and replace it with:

- Round 1 containing only `#11`;
- Architecture Horizon;
- Round Transition Gate;
- discovery ledger;
- incremental decomposition rules;
- Epic Completion Gate.

## 12. Coding Agent Selection Rules

When no target issue is supplied, the Coding Agent SHALL:

1. read Epic `#27` native sub-issues;
2. identify the current approved Round;
3. select only the earliest open executable sub-issue in that Round;
4. verify its native parent is Epic `#27`;
5. verify every blocked-by dependency is closed and merged;
6. verify `planning_anchor_sha` is an ancestor of current `main`;
7. verify no other implementation Issue or PR is active;
8. reject archived, superseded, horizon-only, or future-round issues.

The Coding Agent SHALL NOT infer that every open issue is executable.

## 13. Reviewer Rules

The Senior Reviewer SHALL verify:

- native Epic relationship;
- current Round membership;
- planning anchor SHA ancestry;
- predecessor and blocked-by relationships;
- file-boundary compliance;
- absence of future-round implementation;
- discovery classification;
- all existing semantic and verification requirements.

The reviewer SHALL return one of:

- `PASS — READY FOR SEQUENTIAL MERGE`;
- `PASS — READY FOR ROUND COMPLETION AND REASSESSMENT`;
- `FAIL — CHANGES REQUIRED`;
- `REVIEW INCOMPLETE — EVIDENCE MISSING`.

The second PASS verdict applies only to the final Issue of a Round.

## 14. Reviewer Follow-Up Prompt Semantics

For a normal PASS inside a Round, the generated Coding Agent prompt SHALL direct merge handoff and post-merge smoke verification, while prohibiting the next Issue until authorized.

For final-Round PASS, the generated prompt SHALL:

1. prohibit implementation of another capability;
2. complete authorized merge and post-merge smoke verification;
3. record the latest `main` SHA;
4. enter Round Reassessment Mode;
5. inspect the current codebase and discovery ledger;
6. propose no more than three next-round sub-issues;
7. produce file-touch and dependency maps;
8. wait for human approval before creating issues.

FAIL and REVIEW INCOMPLETE behavior remain unchanged except that the prompt SHALL preserve Round ID and planning anchor information.

## 15. Epic Completion Gate

Epic `#27` SHALL close only when all conditions are satisfied:

- every fixed V1 Definition of Done item has evidence;
- every required Architecture Horizon capability is implemented or explicitly removed by approved amendment;
- all production acceptance and benchmark gates pass;
- no Critical or Important review finding remains;
- no blocking discovery remains untriaged;
- contract migration checks pass;
- exact-source fidelity gates pass;
- resolver authority gates pass;
- MySQL/PostgreSQL isolation gates pass;
- release benchmark passes;
- final `main` SHA is recorded;
- architecture-to-implementation traceability is complete.

Having zero open sub-issues is insufficient by itself.

If the Epic Definition of Done is incomplete, a new Round SHALL be planned.

Non-blocking discoveries outside V1 SHALL move to a separate V2 Epic instead of expanding V1.

## 16. Governance File Changes Required After Approval

Repository migration will require updates to:

- `AGENTS.md`;
- `docs/superpowers/plans/2026-07-29-file-boundary-execution-policy.md`;
- `docs/superpowers/plans/2026-07-29-llm-sql-discover-implementation-plan.md`;
- `docs/superpowers/plans/llm-sql-discover/file-touch-map.json`;
- Epic `#27`;
- Issue `#11`;
- Issues `#12`–`#26` state and comments;
- Coding Agent prompt;
- Senior Reviewer prompt.

These changes SHALL be performed as a governance migration, not as V1 implementation work.

## 17. Native Sub-Issue Capability Constraint

Native parent/sub-issue relationships are preferred and required when the available GitHub tooling supports them.

If the active connector cannot create native relationships, the migration SHALL NOT pretend that Markdown links are equivalent. The migration report SHALL identify the limitation and either:

- use an authenticated GitHub CLI/API path that supports native sub-issues; or
- pause native relationship creation while completing all other governance changes.

## 18. Migration Verification

The migration is complete only when verification proves:

- Epic `#27` reflects the round-based model;
- Issue `#11` is the only executable implementation Issue;
- Issues `#12`–`#26` are closed as superseded planning history;
- archived issues retain their content;
- no prompt selects issues merely by numeric range;
- all prompts verify Round ID and planning anchor SHA;
- the fixed sequence `#11 -> #26` is removed as an execution rule;
- Architecture Horizon remains complete;
- the Definition of Done remains unchanged;
- governance documents do not contradict each other;
- no implementation source is modified.

## 19. Rollback

Before migration, the current Issue and governance states SHALL be recorded.

Rollback SHALL restore:

- previous Epic body;
- previous Issue states;
- previous governance documents;
- previous prompt artifacts.

Issue history and comments remain append-only evidence and SHALL not be deleted.

## 20. Initial State After Migration

The expected state is:

```text
Epic #27 — Fresh-Context SQL Discovery & Trace V1
|
|-- Round R1
|   `-- #11 Project scaffold and contract registry [executable]
|
|-- Superseded planning history
|   `-- #12–#26 [closed, not planned]
|
|-- Architecture Horizon
|   |-- State and audit
|   |-- Snapshot and evidence
|   |-- C# and Vue analyzers
|   |-- LLM and SQL normalization
|   |-- Resolver and execution chains
|   |-- Target projections
|   |-- Orchestration and reporting
|   `-- Release benchmark
|
`-- Future rounds
    `-- Created only from the latest verified main SHA
```

## 21. Non-Goals

This governance migration does not:

- implement Issue `#11`;
- create Round 2;
- alter V1 product scope;
- weaken the V1 Definition of Done;
- permit parallel implementation;
- delete the planning history of Issues `#12`–`#26`;
- treat Markdown checklists as native sub-issue relationships;
- automatically close Epic `#27` when child issues close.
