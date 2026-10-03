# AMJ Core Coordination

This file is the authoritative coordination surface for separate chats, agents, and workstreams working on **Ancient & Medieval Japan Core**.

Use it instead of asking the user to manually relay messages between workstreams.

## Working rule

At the start of AMJ Core work:

1. Read `AGENTS.md`.
2. Read this file from `main`.
3. Check whether there are OPEN / IN PROGRESS items relevant to the current workstream.
4. Perform the work directly when possible.
5. Update this file when an item's status, owner, blocker, or result materially changes.
6. Put confirmed specifications and implementation decisions into the actual source-of-truth files as well.

This file is for coordination only. It is **not** the final design document.

## Source of truth

Current primary design source:

`Docs/Design.md`

Confirmed implementation details must also be reflected in the relevant C#/XML/Defs/Patches/localization files.

## Repository boundaries

AMJ-related standalone mods may have their own repositories and their own authoritative coordination logs.

When work belongs to another repository, create/update the handoff in that repository's:

`main:Docs/Coordination.md`

Do not use the user as the transport layer between repositories.

## Status vocabulary

- **OPEN** — needs work
- **IN PROGRESS** — currently being investigated or implemented
- **BLOCKED** — waiting on a specific prerequisite
- **DONE** — completed and reflected in the proper source of truth
- **ARCHIVED** — retained for history but no longer active

## Suggested workstream labels

Use whichever label best fits the task:

- **Core/design**
- **Agriculture/XML**
- **Food/cooking**
- **Buildings/furniture**
- **Research/progression**
- **Compatibility**
- **C#/framework**
- **Art/graphics**
- **Localization**
- **Testing/release**

## Current coordination items

No active AMJ Core handoff items have been registered yet.

Add new items using the following form.

### AMJ-XXX — Short title

**Requested by:** <workstream/chat/repository>  
**Owner:** <workstream>  
**Status:** OPEN

Context, constraints, and exact question/request.

**Next action:** concrete next step.

**Result / references:** add commit SHA, PR, design section, or other durable reference when available.

## Completed handoffs

### AMJ-001 — Stage A crop balance baseline recovery

**Requested by:** Core/design  \
**Owner:** Agriculture/XML  \
**Status:** DONE

Recovered the previously confirmed Stage A balance values for the six first-Alpha field crops (Awa, Hie, Kibi, barley, MO wheat, buckwheat) from repository history and reconciled them with the current MO-required / standalone-CCTO architecture.

The restored authoritative design now includes:
- growDays;
- final edible-grain yield baselines;
- fertilityMin / fertilitySensitivity;
- growth-temperature design values;
- sowMinSkill and research unlocks;
- grain processing/storage tiers;
- CCTO-compatible fixed cold-death temperatures, using CCTO only when installed rather than duplicating its C# framework in Core.

Historical design references used for recovery include `9b6807b48cf43da50a70caf1a99a5989391473ca` (growDays), `768665413e70ad7451b6b2255c67eb349ea32099` (yield/fertility/temperature), `33430521c97e22e2a52fe1ca661deeb6faf5c025` (skill/storage), and `36f271de4d82162fb002922bbb295ae5f68f31ae` (later grain-processing/storage structure). Current CCTO AMJ values are sourced from CCTO `Docs/ImplementationTable.md`.

**Result / references:** `Docs/Design.md` commit `f8190ecdaf5ca2d2313e54496b928f8eb66b5685`.
