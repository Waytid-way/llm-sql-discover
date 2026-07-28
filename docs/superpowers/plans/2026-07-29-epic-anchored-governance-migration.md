# Epic-Anchored Governance Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate repository governance from a fully pre-created implementation backlog to Epic-anchored incremental rounds while preserving the fixed V1 scope, Definition of Done, planning history, single-writer rule, and sequential merge gates.

**Architecture:** Epic #27 remains the permanent V1 anchor. Round R1 contains only Issue #11. Issues #12–#26 become non-executable planning history, while their intended capabilities remain in the Architecture Horizon. Later rounds are generated from the latest verified `main` SHA and contain no more than three issues.

**Tech Stack:** GitHub Issues, Markdown governance files, JSON file-touch maps, Git branches and pull requests.

## Global Constraints

- Do not modify implementation source code.
- Do not delete Issue content or history.
- Keep V1 scope and Definition of Done unchanged.
- Only Issue #11 is executable after migration.
- Issues #12–#26 must close with reason `not_planned` and retain supersession comments.
- Do not claim a native parent/sub-issue relationship unless GitHub tooling confirms it exists.
- Future rounds contain one to three issues and are anchored to the latest verified `main` SHA.
- Only one implementation Issue and one implementation PR may be active at a time.

---

### Task 1: Record and preserve the pre-migration state

**Files:**
- Read: `AGENTS.md`
- Read: `docs/superpowers/plans/2026-07-29-file-boundary-execution-policy.md`
- Read: `docs/superpowers/plans/2026-07-29-llm-sql-discover-implementation-plan.md`
- Read: `docs/superpowers/plans/llm-sql-discover/file-touch-map.json`
- Read: Epic `#27`
- Read: Issues `#11`–`#26`

- [ ] Record the migration branch base and current `main` state.
- [ ] Capture the current Epic and Issue bodies before mutation.
- [ ] Verify that no implementation PR or implementation source exists.
- [ ] Verify Issue #11 remains open and Issues #12–#26 are still open before migration.

### Task 2: Update repository governance documents

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/superpowers/plans/2026-07-29-file-boundary-execution-policy.md`
- Modify: `docs/superpowers/plans/2026-07-29-llm-sql-discover-implementation-plan.md`
- Modify: `docs/superpowers/plans/llm-sql-discover/file-touch-map.json`
- Create: `docs/prompts/coding-agent-implementation.md`
- Create: `docs/prompts/senior-peer-reviewer.md`

- [ ] Replace numeric-range issue selection with current-Round selection through Epic #27.
- [ ] Define Round ID, planning anchor SHA, native parent verification, blocked-by verification, and discovery classification.
- [ ] Convert the fixed task list into an Architecture Horizon.
- [ ] Restrict the active file-touch map to Round R1 / Issue #11 and preserve archived mappings as planning history only.
- [ ] Add Coding Agent and Senior Reviewer prompts adapted to incremental rounds.
- [ ] Ensure the Reviewer prompt produces a final copyable Coding Agent prompt for all verdicts.

### Task 3: Update Epic #27 and Issue #11

**GitHub objects:**
- Modify: Epic `#27`
- Modify: Issue `#11`

- [ ] Replace the fixed #11→#26 execution sequence with Round R1 containing only #11.
- [ ] Add Architecture Horizon, Round Transition Gate, Discovery Ledger, completed-round ledger, and Epic Completion Gate to #27.
- [ ] Add Round ID, planning anchor SHA, parent Epic declaration, successor behavior, and final-round review semantics to #11.
- [ ] State honestly whether a native sub-issue relationship is verified or pending due to tooling limitations.

### Task 4: Archive Issues #12–#26

**GitHub objects:**
- Comment and close: Issues `#12` through `#26`

- [ ] Add a supersession comment to each issue.
- [ ] Preserve the original body unchanged.
- [ ] Explain that the capability remains in the Architecture Horizon.
- [ ] State that the issue must not be implemented directly.
- [ ] Link Epic #27 and the approved design document.
- [ ] Close with state reason `not_planned`.

### Task 5: Verify the migrated governance state

**Verification:**
- [ ] Confirm Epic #27 describes the round-based model.
- [ ] Confirm Issue #11 is the sole executable implementation Issue.
- [ ] Confirm Issues #12–#26 are closed as `not_planned` and retain original content.
- [ ] Confirm prompts no longer select issues by numeric range.
- [ ] Confirm all executable issue rules require Round ID and planning anchor SHA.
- [ ] Confirm the Architecture Horizon still covers every original V1 capability.
- [ ] Confirm Definition of Done and V1 scope are unchanged.
- [ ] Confirm no implementation source files changed.
- [ ] Confirm governance documents are internally consistent.

### Task 6: Publish the governance migration

- [ ] Compare the migration branch against `main`.
- [ ] Open a pull request containing only governance changes.
- [ ] Review the PR diff and issue-state verification evidence.
- [ ] Merge only after the governance verification passes.
- [ ] Re-read governance files and Issues from `main` after merge.
