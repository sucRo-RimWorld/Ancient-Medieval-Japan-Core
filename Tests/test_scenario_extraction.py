"""Disposable package ownership, ordering and current-contract regressions.

This projects explicit XML only; it is not the engine, inheritance or a save load.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from amj_profile_xml import ROOT, profile_xml, contract_signature
sys.path.insert(0,str(ROOT/'Scripts'))
from prepare_scenario_extraction import build, LEGACY

GRAINS_ID = 'sucro.amj.grains.extractiontest'
SCENARIO_ID = 'sucro.amj.scenarios.extractiontest'
MO_ID = 'dankpyon.medieval.overhaul'
OWNED = {'ScenarioDef':'AMJC_NewVillage','FactionDef':'AMJC_PlayerVillage','PawnKindDef':'AMJC_Villager'}


def roots(package, active):
    active = {x.lower() for x in active}
    result = []
    for node in ET.parse(package/'loadFolders.xml').findall('v1.6/li'):
        checks = {key:{x.strip().lower() for x in node.get(key,'').split(',') if x.strip()}
                  for key in ('IfModActive','IfModActiveAll','IfModNotActive')}
        if checks['IfModActive'] and not (checks['IfModActive'] & active):continue
        if checks['IfModActiveAll'] and not checks['IfModActiveAll'] <= active:continue
        if checks['IfModNotActive'] & active:continue
        path = package if node.text == '/' else package/node.text
        assert path.is_dir(),'Missing loaded folder: '+str(path)
        result.append(path)
    return result


def project(packages, active):
    doc = ET.Element('Defs');patches = []
    for package in packages:
        for root in roots(package,active):
            if (root/'Defs').exists():
                for file in sorted((root/'Defs').rglob('*.xml')):
                    doc.extend(deepcopy(list(ET.parse(file).getroot())))
            if (root/'Patches').exists():
                for file in sorted((root/'Patches').rglob('*.xml')):
                    patches.extend(deepcopy(list(ET.parse(file).getroot())))
    names = [n.findtext('defName') for n in doc if n.findtext('defName')]
    assert len(names) == len(set(names)),'Duplicate loaded DefName'
    for op in patches:
        selector = op.findtext('xpath') or ''
        # Only explicit AMJ-owned operations are projected. External MO wheat,
        # FindMod/CCTO, inheritance and all other engine behavior are out of scope.
        if not selector.startswith('/Defs/') or 'AMJC_' not in selector:continue
        targets = doc.findall('./'+selector[len('/Defs/'):])
        assert len(targets) == 1,'Patch target count: '+selector
        target = targets[0];value = op.find('value')
        assert value is not None
        if op.get('Class') == 'PatchOperationAdd':target.extend(deepcopy(list(value)))
        elif op.get('Class') == 'PatchOperationReplace':
            parents = {child:parent for parent in doc.iter() for child in parent}
            parent = parents[target];index = list(parent).index(target);parent.remove(target)
            for offset,child in enumerate(value):parent.insert(index+offset,deepcopy(child))
        else:raise AssertionError('Unprojected AMJ operation: '+str(op.attrib))
    return doc


def check(packages, grains, scenario, mo):
    active = ([GRAINS_ID] if grains else []) + ([SCENARIO_ID] if scenario else []) + ([MO_ID] if mo else [])
    doc = project(packages,active)
    defs = {n.findtext('defName'):n for n in doc if n.findtext('defName')}
    for typ,name in OWNED.items():
        assert name in defs and defs[name].tag == typ,'Missing/mistyped preserved Def: '+name
    faction = defs['AMJC_PlayerVillage'];pawn = defs['AMJC_Villager'];village = defs['AMJC_NewVillage']
    assert village.findtext('scenario/playerFaction/factionDef') == faction.findtext('defName')
    assert faction.findtext('basicMemberKind') == pawn.findtext('defName')
    assert pawn.findtext('defaultFactionDef') == faction.findtext('defName')
    items = village.findall('scenario/parts/li[@Class="ScenPart_StartingThing_Defined"]')
    supplied = {n.findtext('thingDef'):int(n.findtext('count')) for n in items}
    assert len(supplied) == len(items),'Duplicate starting stock'
    for node in (village,faction,pawn):
        for child in node.iter():
            text = (child.text or '').strip()
            if text.startswith('AMJC_') and '.' not in text and child.tag != 'textKey':
                assert text in defs,'Unresolved AMJ reference: '+text
            if not mo:assert 'DankPyon_' not in text,'Unguarded MO reference'
    assert bool(village.findall('scenario/parts/li[@Class="ScenPart_StartingResearch"]')) == mo
    assert ('DankPyon_Peasant' in [n.text for n in pawn.findall('apparelTags/li')]) == mo
    if grains:
        expected = {n.findtext('defName'):n for n in profile_xml('mo' if mo else 'vanilla') if n.findtext('defName')}
        # Exact current explicit scenario/grain contracts, including part order.
        assert defs.keys() == expected.keys(),'Definition inventory changed'
        for name in expected:
            assert contract_signature(defs[name]) == contract_signature(expected[name]),'Changed contract: '+name
        assert 'RawRice' not in supplied and supplied['AMJC_Millet'] == 200 and supplied['AMJC_RawMillet'] == 100
    else:
        assert set(defs) == set(OWNED.values()),'Scenario package must own only its three Defs'
        assert supplied['RawRice'] == 300 and not any(x.startswith('AMJC_') for x in supplied)
        assert faction.get('ParentName') == 'PlayerFactionBase' and pawn.get('ParentName') == 'BasePlayerPawnKind'
    return doc


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)/'pair'
        self.grains,self.scenario = build(self.output,GRAINS_ID,SCENARIO_ID)

    def test_all_six_ownership_configurations(self):
        # Legacy Grains alone + all four requested independent-scenario variants.
        for mo in (False,True):
            for grains,scenario in ((True,False),(False,True),(True,True)):
                with self.subTest(mo=mo,grains=grains,scenario=scenario):
                    check(([self.grains] if grains else [])+([self.scenario] if scenario else []),grains,scenario,mo)

    def test_production_sources_and_localization_are_unchanged(self):
        report = json.loads((self.output/'source-state.json').read_text())
        for path,expected in report['sourceHashes'].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),expected)
        for path,expected in report['generatedHashes'].items():
            self.assertEqual(hashlib.sha256((self.output/path).read_bytes()).hexdigest(),expected)
        manifest = json.loads((ROOT/'Tests/Fixtures/ScenarioExtraction/manifest.json').read_text())
        for path in manifest['localization']:
            self.assertEqual((self.scenario/path).read_bytes(),(ROOT/path).read_bytes())
            self.assertEqual((self.grains/LEGACY/path).read_bytes(),(ROOT/path).read_bytes())
            self.assertFalse((self.grains/path).exists())
        for typ,item in manifest['definitions'].items():
            self.assertFalse((self.grains/item['path']).exists())
            self.assertEqual((self.grains/LEGACY/item['path']).read_bytes(),(ROOT/item['path']).read_bytes())
        self.assertFalse(ET.parse(self.scenario/'About/About.xml').findall('modDependencies/li'))
        self.assertFalse(ET.parse(self.grains/'About/About.xml').findall('modDependencies/li'))

    def test_original_core_cannot_be_combined_with_new_provider(self):
        # An unchanged old Core still owns the names. Do not promise that mix.
        with self.assertRaisesRegex(AssertionError,'Duplicate'):
            project([ROOT,self.scenario],[SCENARIO_ID,MO_ID])

    def test_duplicate_definitions_if_legacy_guard_is_lost(self):
        path = self.grains/'loadFolders.xml';doc = ET.parse(path)
        doc.findall('v1.6/li')[3].attrib.clear();doc.write(path)
        with self.assertRaisesRegex(AssertionError,'Duplicate'):
            check([self.grains,self.scenario],True,True,False)

    def test_legacy_mo_patch_must_be_guarded_with_its_definitions(self):
        path = self.grains/'loadFolders.xml';doc = ET.parse(path)
        del doc.findall('v1.6/li')[4].attrib['IfModNotActive'];doc.write(path)
        with self.assertRaises(AssertionError):check([self.grains,self.scenario],True,True,True)

    def test_grains_integration_must_follow_mo_parts_replacement(self):
        path = self.scenario/'loadFolders.xml';doc = ET.parse(path);version = doc.find('v1.6')
        mo,grain = list(version)[1:];version.remove(mo);version.remove(grain);version.extend([grain,mo]);doc.write(path)
        with self.assertRaises(AssertionError):check([self.grains,self.scenario],True,True,True)

    def test_optional_grain_stock_cannot_leak_into_standalone(self):
        path = self.scenario/'loadFolders.xml';doc = ET.parse(path)
        doc.findall('v1.6/li')[2].attrib.clear();doc.write(path)
        with self.assertRaises(AssertionError):check([self.scenario],False,True,False)

    def test_existing_output_and_production_identity_are_rejected(self):
        state = (self.output/'source-state.json').read_bytes()
        with self.assertRaises(FileExistsError):build(self.output,GRAINS_ID,SCENARIO_ID)
        self.assertEqual((self.output/'source-state.json').read_bytes(),state)
        with self.assertRaises(ValueError):build(Path(self.temp.name)/'wrong','sucro.ancientmedievaljapan.core',SCENARIO_ID)
        self.assertFalse((Path(self.temp.name)/'wrong').exists())
        with self.assertRaises(ValueError):build(Path(self.temp.name)/'same',GRAINS_ID,GRAINS_ID)
        self.assertFalse((Path(self.temp.name)/'same').exists())


if __name__ == '__main__':unittest.main()
