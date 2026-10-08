"""Static upland-rice contract and seven-crop balance regression; no game launch."""
from pathlib import Path
from collections import Counter
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NAME = 'Plant_Rice'
PATCH = ROOT / 'Patches/UplandRice.xml'
FIELDS = {'growDays': 5, 'harvestYield': 11, 'fertilityMin': .7,
          'fertilitySensitivity': .8, 'minGrowthTemperature': 10,
          'minOptimalGrowthTemperature': 18, 'maxOptimalGrowthTemperature': 32,
          'maxGrowthTemperature': 42}


def validate():
    operations = ET.parse(PATCH).getroot().findall('.//li')
    values = {}
    for operation in operations:
        if operation.attrib.get('Class') not in ('PatchOperationAdd', 'PatchOperationReplace'):
            continue
        xpath = operation.findtext('xpath', '')
        if 'ThingDef[defName="Plant_Rice"]' not in xpath:
            raise AssertionError('Upland patch must only target existing Plant_Rice')
        value = operation.find('value')
        for node in value:
            if node.tag in FIELDS:
                if node.tag in values:
                    raise AssertionError('duplicate field ' + node.tag)
                values[node.tag] = float(node.text)
            if node.tag == 'sowTags':
                assert [child.text for child in node] == ['Ground']
    assert values == FIELDS, 'Unexpected upland-rice balance or missing patch fields'
    xml = PATCH.read_text(encoding='utf-8')
    assert 'RawRice' in xml and 'AMJC_UplandRice' not in xml
    jp = ET.parse(ROOT / 'Languages/Japanese/DefInjected/ThingDef/AMJC_UplandRice.xml').getroot()
    assert jp.findtext('Plant_Rice.label') == '陸稲'
    assert jp.findtext('Plant_Rice.description')
    ccto = (ROOT / 'Patches/Compatibility/CCTO_StageA.xml').read_text(encoding='utf-8')
    assert 'Plant_Rice' not in ccto, 'Do not add duplicate CCTO rice extension'
    fixture = json.loads((ROOT / 'Tests/Fixtures/Grains_Environment.json').read_text())
    for profile in ('vanilla', 'mo'):
        rows = fixture[profile]
        assert len(rows) == 27
        wins = Counter()
        viable = 0
        for row in rows:
            f, t, season = row['fertility'], row['temperature'], row['season']
            a = FIELDS
            if f < a['fertilityMin']:
                rice = 0
            else:
                low, optimal_low = a['minGrowthTemperature'], a['minOptimalGrowthTemperature']
                optimal_high, high = a['maxOptimalGrowthTemperature'], a['maxGrowthTemperature']
                factor = (t-low)/(optimal_low-low) if t < optimal_low else (
                    (high-t)/(high-optimal_high) if t > optimal_high else 1)
                factor = max(0, min(1, factor))
                rate = factor * (1-a['fertilitySensitivity']+f*a['fertilitySensitivity'])
                rice = int((season*rate/a['growDays'])+0.000001) * a['harvestYield']
            yields = row['yields'] + [rice]
            best = max(yields)
            if best <= 0:
                continue
            viable += 1
            for i, value in enumerate(yields):
                if value == best:
                    wins[i] += 1
        assert set(wins) == set(range(7)), 'A grain lost its representative niche: ' + str(wins)
        assert max(wins.values()) * 3 < viable * 2, 'Single-crop dominance: ' + str(wins)
    return True


if __name__ == '__main__':
    validate()
    print('Upland rice XML and seven-crop analytical regression: PASS (27 cells/profile)')
