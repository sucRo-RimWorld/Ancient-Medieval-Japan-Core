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

## Japanese name form and aliases

For Japanese descriptions, identify the subject clearly at the start of the prose.

- When an established and appropriate kanji form exists, begin the description with that kanji form, followed by the ordinary Japanese reading/name as needed.
- When a recognized alias, alternate name, or common alternate written form exists, include it immediately with the opening name rather than omitting it from the description.
- Do not invent kanji, force uncommon ateji, or mechanically list weakly sourced/local names only to satisfy this rule.
- When several forms exist, prefer the form best supported for the AMJ historical/ecological context and record important alternatives without turning the opening into an exhaustive name list.
- The Japanese opening-name form is part of the approved Japanese source. English localization should translate the approved meaning and may romanize or explain the Japanese names where useful; it must not independently add or remove aliases.

## Required description content

AMJ descriptions should help the player learn something concrete about ancient and medieval Japan while remaining useful as in-game text. For AMJ-facing historical descriptions, use the following content order as the default structure:

1. **Name and aliases:** begin with the established kanji form when one exists, then give the ordinary reading/name and recognized aliases / alternate written forms as appropriate.
2. **Distribution and ecological/material context in Japan:** explain where the plant, animal, material, object, or practice belongs in the Japanese environment or material culture when relevant.
3. **Ancient/medieval Japanese role:** include at least one supported fact about its use, cultivation, gathering, production, trade, social meaning, construction, food culture, ecology, or other relationship to life in ancient/medieval Japan.
4. **Difference from modern Japan:** when a clear, supportable difference exists, explain how its distribution, use, production, social role, or availability differs from modern Japan.

The purpose is not to pad descriptions with trivia. Prefer facts that teach why the subject matters in the ancient/medieval Japanese setting.

Not every description needs four equally long parts. If one category is irrelevant or cannot be supported reliably, omit it rather than inventing content. However, for historical AMJ content, a description that contains only generic appearance or ecology and gives no ancient/medieval-Japan context is normally incomplete.

Modern comparison is not license to invent contrast. If a reliable historical/modern difference cannot be established, prefer an accurate narrower description and record the research gap rather than fabricating one.

Avoid generic encyclopedia trivia that does not help explain the content's place in ancient/medieval Japan.

### In-game paragraph formatting

Long RimWorld descriptions should be split into a small number of readable paragraphs using the literal `\n\n` sequence in Def / DefInjected text.

Use paragraph breaks by meaning rather than after every sentence. The default shape for longer AMJ historical descriptions is:

1. name / aliases + distribution / ecology or material context;
2. ancient / medieval Japanese role, use, evidence, or cultural context;
3. modern difference or present-day use, when relevant and supportable.

Two paragraphs are sufficient when the material does not justify three. Short descriptions should remain a single paragraph. Do not add padding merely to satisfy the structure.

After the Japanese text is approved, keep the English translation's paragraph structure broadly aligned where natural.

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

## Gameplay-feature ownership in descriptions

Do not describe a planned gameplay function in a base mod merely because the underlying historical object, plant, or animal could support that function.

- If a later Addon introduces a concrete gameplay function such as harvesting acorns, nuts, fruit, fiber, resin, medicinal material, or another resource, the Addon that owns and implements that function also owns the gameplay-facing description update for that function.
- The base mod may describe accurate historical, botanical, ecological, or material facts, but it must not imply that an unimplemented harvest/use mechanic already exists.
- When the Addon is active, its localization/description patch may add the relevant functional explanation while preserving the approved base description and historical facts.
- Keep this ownership aligned with code/XML ownership: the mod that adds the mechanic is the mod that explains that mechanic to the player.

Example: AMJ Environment may describe Sudajii or Japanese beech as trees with historically edible nuts where appropriate, but an explicit explanation of harvestable acorns/nuts belongs to the Addon that actually adds that harvesting feature.

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
