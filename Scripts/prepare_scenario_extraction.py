#!/usr/bin/env python3
"""Build disposable Grains/Starting Scenarios prototypes without editing production.

Never installs, publishes, rewrites saves or assigns a permanent package identity.
The caller must provide two test package IDs and a fresh output directory.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'Tests/Fixtures/ScenarioExtraction/manifest.json'
MO = 'DankPyon.Medieval.Overhaul'
LEGACY = 'LegacyStartingScenarios'


def write_xml(path, node):
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(node, space='  ')
    ET.ElementTree(node).write(path, encoding='utf-8', xml_declaration=True)


def replace_grains(parts, candidate):
    found = [n for n in parts if n.findtext('thingDef') in ('AMJC_Millet','AMJC_RawMillet')]
    assert [n.findtext('thingDef') for n in found] == ['AMJC_Millet','AMJC_RawMillet']
    assert [n.findtext('count') for n in found] == ['200','100']
    index = list(parts).index(found[0])
    for node in found: parts.remove(node)
    rice = deepcopy(found[0]);rice.find('thingDef').text = candidate['defName']
    rice.find('count').text = str(candidate['count']);parts.insert(index,rice)
    return found


def build(output, grains_id, scenario_id, source=ROOT):
    output = Path(output).resolve();source = Path(source).resolve()
    ids = (grains_id, scenario_id)
    for id_ in ids:
        if not re.fullmatch(r'[a-z0-9]+(?:[.][a-z0-9]+)+',id_) or not id_.endswith('.extractiontest'):
            raise ValueError('Prototype package IDs must be lower-case and end in .extractiontest')
    if grains_id == scenario_id: raise ValueError('Two distinct package IDs are required')
    if output.exists(): raise FileExistsError('Use a fresh output directory; existing files are never overwritten')
    if output == source or source in output.parents: raise ValueError('Output must be outside the repository')
    manifest = json.loads((source/'Tests/Fixtures/ScenarioExtraction/manifest.json').read_text())
    grains = output/'Grains';scenario = output/'StartingScenarios'
    output.mkdir(parents=True)
    for folder in ('About','Defs','Patches','Textures','Languages','Compatibility','BaseWithoutMO','Assemblies','1.6'):
        if (source/folder).exists(): shutil.copytree(source/folder,grains/folder)
    paths = [v['path'] for v in manifest['definitions'].values()] + manifest['localization']
    for relative in paths:
        assert (source/relative).is_file(),relative
        for target in (grains/LEGACY/relative, scenario/relative):
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/relative,target)
        (grains/relative).unlink()
    # Split the existing MO compatibility by owned target, preserving grain ops.
    patch = ET.parse(source/manifest['moPatch']).getroot()
    owned = ET.Element('Patch');remaining = ET.Element('Patch')
    for op in patch:
        xpath = op.findtext('xpath') or ''
        dest = owned if xpath.startswith('/Defs/ScenarioDef[') or xpath.startswith('/Defs/PawnKindDef[') else remaining
        dest.append(deepcopy(op))
    assert len(owned) == 2,'Scenario patch inventory changed; review extraction'
    write_xml(grains/manifest['moPatch'],remaining)
    write_xml(grains/LEGACY/'Compatibility/MedievalOverhaul/Patches/StartingScenarios.xml',owned)
    # Scenario Base contains Vanilla refs only; MO variant keeps the source
    # ordering, then Grains integration replaces the single rice proxy in place.
    scenario_def = ET.parse(scenario/manifest['definitions']['ScenarioDef']['path']).getroot()
    grain_parts = replace_grains(scenario_def.find('ScenarioDef/scenario/parts'),manifest['standaloneGrainCandidate'])
    write_xml(scenario/manifest['definitions']['ScenarioDef']['path'],scenario_def)
    replace_grains(owned.find('Operation/value/parts'),manifest['standaloneGrainCandidate'])
    write_xml(scenario/'Compatibility/MedievalOverhaul/Patches/StartingScenarios.xml',owned)
    compat = ET.Element('Patch');op = ET.SubElement(compat,'Operation',{'Class':'PatchOperationReplace'})
    ET.SubElement(op,'xpath').text = '/Defs/ScenarioDef[defName="AMJC_NewVillage"]/scenario/parts/li[thingDef="RawRice"]'
    ET.SubElement(op,'value').extend(grain_parts)
    write_xml(scenario/'Compatibility/Grains/Patches/StartingGrains.xml',compat)
    # Positive + negative loader conditions are conjunctive (LoadFolder.ShouldLoad).
    loader = ET.parse(source/'loadFolders.xml').getroot();version = loader.find('v1.6')
    ET.SubElement(version,'li',{'IfModNotActive':scenario_id}).text = LEGACY
    ET.SubElement(version,'li',{'IfModActive':MO,'IfModNotActive':scenario_id}).text = LEGACY+'/Compatibility/MedievalOverhaul'
    write_xml(grains/'loadFolders.xml',loader)
    loader = ET.Element('loadFolders');version = ET.SubElement(loader,'v1.6')
    ET.SubElement(version,'li').text = '/'
    ET.SubElement(version,'li',{'IfModActive':MO}).text = 'Compatibility/MedievalOverhaul'
    ET.SubElement(version,'li',{'IfModActive':grains_id}).text = 'Compatibility/Grains'
    write_xml(scenario/'loadFolders.xml',loader)
    about = ET.parse(source/'About/About.xml').getroot()
    about.find('name').text = 'AMJ Grains extraction test'
    about.find('packageId').text = grains_id
    about.find('description').text = 'Disposable extraction test. Not a release; save compatibility is unverified.'
    deps = about.find('modDependencies')
    for dep in list(deps):
        if dep.findtext('packageId','').lower() == MO.lower():deps.remove(dep)
    if len(deps) == 0:about.remove(deps)
    write_xml(grains/'About/About.xml',about)
    about = ET.Element('ModMetaData')
    for tag,text in (('name','AMJ Starting Scenarios extraction test'),('author','sucRo0629'),('packageId',scenario_id)):
        ET.SubElement(about,tag).text = text
    ET.SubElement(ET.SubElement(about,'supportedVersions'),'li').text = '1.6'
    after = ET.SubElement(about,'loadAfter')
    for id_ in (MO,grains_id):ET.SubElement(after,'li').text = id_
    ET.SubElement(about,'description').text = 'Disposable independent-scenario test. Not a release; safe removal is unverified.'
    write_xml(scenario/'About/About.xml',about)
    audit_paths = paths + [manifest['moPatch'],'loadFolders.xml','About/About.xml','Tests/Fixtures/ScenarioExtraction/manifest.json','Scripts/prepare_scenario_extraction.py']
    report = {'status':'prototype only; no game run or save migration', 'grainsPackageId':grains_id,
              'scenarioPackageId':scenario_id,'standaloneGrainCandidate':manifest['standaloneGrainCandidate'],
              'sourceHashes':{p:hashlib.sha256((source/p).read_bytes()).hexdigest() for p in audit_paths}}
    report['generatedHashes'] = {p.relative_to(output).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                for package in (grains,scenario) for p in sorted(package.rglob('*')) if p.is_file()}
    (output/'source-state.json').write_text(json.dumps(report,indent=2)+'\n')
    return grains,scenario


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--grains-package-id',required=True)
    parser.add_argument('--scenario-package-id',required=True)
    args = parser.parse_args()
    build(args.output,args.grains_package_id,args.scenario_package_id)
    print('Prepared disposable extraction pair; no runtime/save compatibility PASS claimed.')
