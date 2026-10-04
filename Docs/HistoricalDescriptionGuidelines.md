# AMJ Historical Description Guidelines

## Purpose

AMJ descriptions are part of the historical presentation, not neutral Vanilla/Medieval Overhaul flavor text.

When AMJ uses, patches, retextures, selects, or otherwise presents an existing Vanilla or Medieval Overhaul item, plant, or animal, audit its label/description from the perspective of ancient and medieval Japan. Do not keep inherited text merely because the underlying Def is reused.

## Scope

This policy applies across the AMJ project to AMJ-facing descriptions for:

- Vanilla items, resources, foods, tools, equipment, plants, trees, animals, and similar content;
- Medieval Overhaul items, resources, foods, tools, equipment, plants, trees, animals, and similar content;
- AMJ-owned content that is intended to represent a historical Japanese counterpart.

The audit is required when the content enters AMJ's intended gameplay/presentation scope, especially when AMJ explicitly patches, retextures, rebalances, selects, or localizes it.

A description rewrite is presentation/localization work only. It does not change gameplay mechanics unless a separate design decision explicitly does so.

## Historical audit rule

For each affected Def:

1. Read the existing Vanilla/MO label and description.
2. Check whether the wording fits the historical role, use, distribution, material culture, cultivation, ecology, or social meaning appropriate to ancient/medieval Japan.
3. Rewrite the description when the inherited wording is anachronistic, culturally mismatched, misleading, overly modern, or tonally unsuitable for AMJ.
4. Do not invent a medieval-Japanese counterpart for content that lacks one. If the content itself is historically unsuitable, flag it for a separate keep/replace/remove decision rather than hiding the mismatch with prose alone.

## Required description content

AMJ-authored historical descriptions should include:

- at least one concrete historical fact relevant to the object, plant, or animal in Japan;
- its historical role, use, ecology, cultivation, distribution, material, or social/economic context when relevant;
- a meaningful difference from modern Japan, modern use, modern distribution, or modern production where that difference can be supported.

Modern comparison is not license to invent contrast. If a reliable historical/modern difference cannot be established, prefer an accurate narrower description and record the research gap rather than fabricating one.

Avoid generic encyclopedia trivia that does not help explain the content's place in ancient/medieval Japan.

## Evidence and source notes

Historical claims should be grounded in reliable sources. Prefer, where practical:

- academic or scholarly publications;
- museum, archive, university, cultural-property, or government sources;
- primary/translated historical materials when the claim genuinely depends on them.

In-game descriptions do not need citation clutter, but the repository should retain enough source/rationale notes to reconstruct why a historical rewrite was made. Put durable source notes in the owning design/localization documentation rather than only in `Docs/Coordination.md`.

Use cautious wording when the evidence is regional, period-specific, debated, or indirect. Do not flatten “Japan” into one uniform practice across all centuries and regions.

## Authoring and translation workflow

Historical description text is authored Japanese-first:

1. research and draft the Japanese description;
2. present the Japanese wording to the author for review;
3. revise until the author approves the Japanese text;
4. only then translate the approved Japanese text into English;
5. keep the English version semantically aligned with the approved Japanese source and do not independently add or remove historical claims.

Do not translate an unapproved Japanese draft merely to keep localization files synchronized during review.

## Vanilla / Medieval Overhaul ownership

Reusing a Vanilla or Medieval Overhaul Def does not require preserving its original prose.

However:

- keep labels unchanged unless there is a separate concrete naming issue;
- do not imply AMJ changed mechanics that remain Vanilla/MO-owned;
- for MO fantasy or deliberately non-historical content that AMJ intentionally retains, preserve its gameplay identity and do not falsely historicize it;
- if historical fit is poor enough that prose cannot solve the issue, escalate to the owning design workstream for a keep/replace/remove decision.

## Validation

Description work should be checked for:

- Japanese XML/localization validity;
- DefInjected key coverage where applicable;
- Japanese/English semantic parity after approval;
- consistency with the owning Def's actual mechanics and AMJ design;
- absence of unsupported or anachronistic historical claims.

Historical accuracy and natural Japanese wording require human review; these are not treated as fully automatable checks.
