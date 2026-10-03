# AMJ Core Agent Instructions

This repository is part of the **Ancient & Medieval Japan (AMJ)** project.

Before starting work in this repository:

1. Read this file.
2. Read the authoritative coordination log at `main:Docs/Coordination.md`.
3. Check for OPEN / IN PROGRESS items owned by the current workstream before starting new work.

## Cross-chat / cross-agent coordination

Do not use the user as a messenger between chats, agents, or workstreams.

When another AMJ workstream needs to be consulted, leave the request and relevant context in:

`main:Docs/Coordination.md`

When another repository is the actual owner of the requested work, record the request in that repository's authoritative `main:Docs/Coordination.md` rather than duplicating competing coordination records here.

## Source-of-truth rule

`Docs/Coordination.md` is only for handoff, status, blockers, and cross-workstream notes.

Durable decisions must also be reflected in the appropriate source of truth, such as:

- `Docs/Design.md`;
- C# code;
- XML/Defs/Patches;
- localization files;
- other repository-owned implementation/design documents.

Do not treat a coordination note as the final specification.

## Branch rule

The authoritative coordination log exists only on `main`.

Do not create branch-specific copies of `Docs/Coordination.md`.

If working on another branch, read and update `main:Docs/Coordination.md` separately when a coordination item changes.

## Consistency rule

When a design or implementation policy changes, do not edit only the immediately affected line.

Check the existing design, implementation, related systems, balance values, documentation, and tests for consistency before applying the change.

## Reporting GitHub changes

Only report that a GitHub file was updated when the change was actually committed to GitHub.

When reporting repository changes, include the actual commit SHA.

## Automated runtime-error gate

For any automated test that launches RimWorld, a passing scenario/test count is not sufficient by itself.

The test harness must capture an isolated runtime log and fail the overall test run if the repository-owned mod emits any ERROR-level entry. Do this even when all Pickle/RimTest scenarios otherwise pass. Warnings remain non-fatal unless a repository-specific test explicitly promotes them.

Any new RimWorld runtime-test harness added to this repository must include this mod-origin ERROR gate from the start. Static-only validation does not fabricate a runtime-log result; add the gate when runtime automation is introduced.
