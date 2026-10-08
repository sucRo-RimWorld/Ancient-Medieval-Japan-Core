"""Read-only grain/save inventory conservation checks for RimWorld 1.6 XML .rws.

The checker neither launches the game nor repairs or rewrites save files. A
passing XML comparison is not a successful engine migration or release gate.
Scenario/Faction/PawnKind migration belongs to the separate Scenarios owner.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

CORE = 'sucro.ancientmedievaljapan.core'
MO = 'dankpyon.medieval.overhaul'
# These are selected shared Vanilla defs touched/produced by Grains. The
# package-specific AMJC prefix captures its persisted crop/food/equipment IDs.
SHARED = {'Plant_Rice', 'RawRice'}


class ContractError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise ContractError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def grain_def(name):
    return name.startswith('AMJC_') or name in SHARED


def canonical(node):
    return [node.tag, sorted(node.attrib.items()), (node.text or '').strip(),
            [canonical(child) for child in node]]


def inspect_bytes(data):
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise ContractError('Expected UTF-8 RimWorld XML save.') from exc
    require('\x00' not in text and '<!DOCTYPE' not in text.upper() and
            '<!ENTITY' not in text.upper(), 'Unsafe or unsupported save encoding/DTD.')
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ContractError(f'Invalid XML save: {exc}') from exc
    require(root.tag == 'savegame', 'Expected RimWorld savegame root.')
    version = root.findtext('meta/gameVersion', '')
    require(version.startswith('1.6.'), 'Only RimWorld 1.6 saves are supported.')
    mods = [(n.text or '').strip().lower() for n in root.findall('meta/modIds/li')]
    require(mods and all(mods) and len(mods) == len(set(mods)), 'Invalid recorded mod IDs.')
    require(CORE in mods and MO in mods and 'ludeon.rimworld' in mods,
            'Legacy Grains/Core migration requires recorded Core, MO and Vanilla IDs.')
    require(not any(word in m for m in mods for word in ('e2e', 'fixture', 'extractiontest')),
            'Production-save inspector rejects test package aliases.')
    maps = root.find('game/maps')
    require(maps is not None and len(maps) > 0, 'Missing map data; unsupported save shape.')
    ticks = root.findtext('game/tickManager/ticksGame', '')
    require(ticks.isdigit(), 'Missing/invalid ticksGame.')
    things = {}
    recipes = []
    for node in maps.iter():
        def_name = node.findtext('def')
        ident = node.findtext('id')
        if def_name and ident and grain_def(def_name):
            require(ident not in things, 'Duplicate grain thing id: ' + ident)
            count = node.findtext('stackCount', '1')
            require(count.isdigit() and int(count) > 0,
                    'Invalid grain stackCount: ' + ident)
            things[ident] = {'def': def_name, 'stackCount': int(count)}
        # Production Bill records have an immediate recipe Def reference.
        recipe = node.findtext('recipe')
        if recipe and recipe.startswith('AMJC_'):
            recipes.append(canonical(node))
    require(any(x['def'].startswith('AMJC_') for x in things.values()),
            'No persisted AMJC grain things; input does not exercise Grains migration.')
    require(any(x['def'] in SHARED for x in things.values()),
            'No persisted RawRice/Plant_Rice; input does not exercise Vanilla rice coexistence.')
    return {'sha256': digest(data), 'gameVersion': version,
            'modIds': mods, 'ticksGame': int(ticks),
            'things': dict(sorted(things.items())),
            'counts': dict(sorted(Counter({name: sum(t['stackCount'] for t in things.values()
                                                    if t['def'] == name)
                                           for name in {t['def'] for t in things.values()}}).items())),
            'grainBills': recipes}


def inspect(path):
    path = Path(path)
    require(path.suffix.lower() == '.rws', 'Input must be an .rws save.')
    return inspect_bytes(path.read_bytes())


def compare(before, after):
    require(before['gameVersion'] == after['gameVersion'], 'Game version changed.')
    require(set(before['modIds']) == set(after['modIds']),
            'Mod configuration changed; use the separate Scenarios provider-transition gate.')
    # Paused immediately after load. Simulation ticks can change crops and bills.
    for key in ('ticksGame', 'things', 'counts', 'grainBills'):
        require(before[key] == after[key], 'Grains conservation changed: ' + key)
    return {'schemaVersion': 1, 'status': 'xml-contracts-checked',
            'runtimeVerified': False, 'beforeSha256': before['sha256'],
            'afterSha256': after['sha256'],
            'limits': 'Does not prove game loading, missing-Def resolution, graphics, runtime ERROR 0 or safe Mod removal.'}


def prepare(save, output, legacy_commit, updated_commit):
    for name, sha in (('legacy', legacy_commit), ('updated', updated_commit)):
        require(bool(re.fullmatch(r'[0-9a-f]{40}', sha)), name + ' requires full 40-digit SHA.')
    require(legacy_commit != updated_commit, 'Legacy and updated commits must differ.')
    source = Path(save).resolve()
    require(source.suffix.lower() == '.rws', 'Input must be an .rws save.')
    data = source.read_bytes()
    baseline = inspect_bytes(data)
    output = Path(output).resolve()
    require(not output.exists(), 'Never overwrite an existing migration evidence directory.')
    output.mkdir(parents=True)
    (output/'baseline.rws').write_bytes(data)
    plan = {'schemaVersion': 1, 'status': 'prepared-not-run',
            'runtimeVerified': False, 'baselineSha256': digest(data),
            'sourceCommitClaims': {'legacyCore': legacy_commit, 'updatedGrains': updated_commit},
            'sourceProvenanceNote': 'Caller-supplied SHA values do not authenticate the originating save.',
            'baseline': baseline, 'cases': [
                {'name': 'same-provider-upgrade', 'input': 'baseline.rws',
                 'output': 'same-provider-upgrade/resaved.rws', 'providerChanges': []}],
            'requiredRuntimeEvidence': ['actual RimWorld engine paused load/resave',
                                        'real mod/provider/DLL/source hashes',
                                        'per-case ERROR 0', 'persisted Grains items and Bills']}
    (output/'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n',
                                    encoding='utf-8')
    require(source.read_bytes() == data, 'Original save changed during preparation.')
    return plan


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('prepare')
    p.add_argument('--save', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--legacy-commit', required=True)
    p.add_argument('--updated-commit', required=True)
    c = commands.add_parser('compare')
    c.add_argument('--before', required=True)
    c.add_argument('--after', required=True)
    args = parser.parse_args(argv)
    try:
        result = prepare(args.save, args.output, args.legacy_commit, args.updated_commit) \
            if args.command == 'prepare' else compare(inspect(args.before), inspect(args.after))
        print(json.dumps(result if args.command == 'compare' else
                         {'status': result['status'], 'runtimeVerified': False},
                         ensure_ascii=False, indent=2))
        return 0
    except (ContractError, OSError) as exc:
        print('[FAIL] ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
