# Development Golden Path Guidelines

This document defines the shared AMJ rule for turning successful development work into a reproducible workflow.

## Rule

When a non-trivial task succeeds after investigation, debugging, iteration, or multiple failed attempts, do not stop at the successful result.

Before moving on, capture the successful path as a **Golden Path** and reduce the chance of recurrence.

The closeout for that task should include, where applicable:

1. identify the exact sequence that produced the accepted result;
2. record the sequence in the owning repository as durable documentation;
3. automate deterministic or repetitive parts of that sequence;
4. add regression/static/runtime checks for the failure modes that were discovered;
5. make the automated path the default entry point for the next similar task;
6. keep human review only for judgments that cannot be automated, such as visual quality or gameplay feel.

A success that depends on remembered chat context, one-off manual commands, hand-transcribed binary data, or an undocumented special case is not considered fully operationalized.

## Where to store it

- Shared project-wide policy belongs in this document and the repositories' `AGENTS.md`.
- Repository-specific Golden Paths belong under that repository's `Docs/GoldenPaths/` or another clearly owned durable design/tooling document.
- Commands/scripts used by the Golden Path must live in the owning repository.
- `Docs/Coordination.md` may record status and handoff only; it is not the canonical procedure.

## Automation expectations

Prefer automation for:
- syntax and structural validation;
- file/asset integrity checks;
- path/reference checks;
- repeatable build/test setup;
- fixed test scenarios and runtime error gates;
- reproducible conversion/import steps.

Do not automate away:
- final visual acceptance;
- subjective UX/readability judgments;
- design approval;
- historical/editorial review that requires author judgment.

## Failure-to-Golden-Path rule

When a failure reveals a missing guard, add the guard to the Golden Path if the same class of failure could recur.

Examples include:
- parser/syntax checks before running larger test suites;
- binary/PNG integrity checks before changing Def paths;
- choosing the correct biome/test fixture for the target asset;
- verifying that the same checked file/script is used locally and in CI.

## Completion criterion

For recurring or likely-to-repeat work, the task is complete only when:
- the accepted implementation exists;
- the relevant automated checks pass;
- the reusable procedure is documented;
- the next similar task can follow that procedure without rediscovering the same steps.
