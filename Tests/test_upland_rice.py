"""Static upland-rice contract and seven-crop balance regression; no game launch."""
from pathlib import Path
from collections import Counter
import json
import xml.etree.ElementTree as ET
from amj_profile_xml import profile_xml

ROOT = Path(__file__).resolve().parents[1]
NAME = 'Plant_Rice'
PATCH = ROOT / 'Patches/UplandRice.xml'
FIELDS = {'growDays': 5, 'harvestYield': 11, 'fertilityMin': .7,
          'fertilitySensitivity': .8, 'minGrowthTemperature': 10,
          'minOptimalGrowthTemperature': 18, 'maxOptimalGrowthTemperature': 32,
          'maxGrowthTemperature': 42}


def validate():
    operations = ET.parse(PATCH).getroot().findall('./Operation/operations/li')
    assert len(operations) == 12, 'Six replaces and six guarded additions'
    values, guarded, replaced = {}, set(), set()
    for op in operations:
        kind, xpath = op.attrib.get('Class'), op.findtext('xpath', '')
        assert xpath.startswith('/Defs/ThingDef[defName="Plant_Rice"]/')
        key = xpath.rsplit('/', 1)[-1]
        if kind == 'PatchOperationConditional':
            assert key in FIELDS and key not in guarded
            guarded.add(key)
            m, n = op.find('match'), op.find('nomatch')
            assert m is not None and n is not None
            assert m.get('Class') == 'PatchOperationReplace' and n.get('Class') == 'PatchOperationAdd'
            assert m.findtext('xpath') == xpath
            assert n.findtext('xpath') == '/Defs/ThingDef[defName="Plant_Rice"]/plant'
            a, b = m.find('value'), n.find('value')
            assert a is not None and b is not None and len(a) == len(b) == 1
            assert a[0].tag == b[0].tag == key
            assert float(a[0].text) == float(b[0].text) == FIELDS[key]
            values[key] = float(a[0].text)
        else:
            assert kind == 'PatchOperationReplace' and xpath not in replaced
            replaced.add(xpath)
            value = op.find('value')
            assert value is not None and len(value) == 1 and value[0].tag == key
            if key == 'harvestedThingDef':
                assert value[0].text == 'AMJC_RiceSheaf'
            elif key == 'sowTags':
                assert [child.text for child in value[0]] == ['Ground']
            elif key in FIELDS:
                values[key] = float(value[0].text)
    assert len(replaced) == 6 and guarded == set(FIELDS) - {'growDays', 'harvestYield'}
    assert values == FIELDS
    xml = PATCH.read_text(encoding='utf-8')
    assert 'RawRice' in xml and 'AMJC_UplandRice' not in xml
    assert '/Defs/ThingDef[defName="Plant_Rice"]/plant/harvestedThingDef' in replaced
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
    # Both actual Grains projections must make intermediate rice inedible,
    # bind thresh/hull Bills to the existing processing benches, and exclude
    # Straw from the Vanilla profile only.
    for profile in ('vanilla', 'mo'):
        projected = profile_xml(profile)
        defs = {node.findtext('defName'): node for node in projected if node.findtext('defName')}
        for name, graphic in (
            ('AMJC_RiceSheaf', 'Things/Item/Resource/AMJC_Millet/RawMillet'),
            ('AMJC_RiceInHull', 'Things/Item/Resource/AMJC_Millet/MilletInHull'),
        ):
            item = defs[name]
            assert item.findtext('ingestible/preferability') == 'NeverForNutrition'
            assert float(item.findtext('comps/li/daysToRotStart')) == 120
            assert item.findtext('graphicData/texPath') == graphic
        for op, ingredient, result, single_work, bulk_work in (
            ('Thresh', 'AMJC_RiceSheaf', 'AMJC_RiceInHull', 15, 120),
            ('Hull', 'AMJC_RiceInHull', 'RawRice', 10, 80),
        ):
            for bulk, count, work in ((False, 1, single_work), (True, 10, bulk_work)):
                recipe = defs['AMJC_' + op + 'Rice' + ('Bulk' if bulk else '')]
                assert recipe.findtext('ingredients/li/filter/thingDefs/li') == ingredient
                assert recipe.findtext('fixedIngredientFilter/thingDefs/li') == ingredient
                assert float(recipe.findtext('ingredients/li/count')) == count
                assert float(recipe.findtext('workAmount')) == work
                products = [(node.tag, int(node.text)) for node in recipe.findall('products/*')]
                expected = [(result, count)]
                if profile == 'mo' and op == 'Thresh':
                    expected.append(('DankPyon_Straw', count))
                assert products == expected, (profile, op, bulk, products)
                assert recipe.get('ParentName') == 'AMJC_RiceProcessingBase'
    for name in ('AMJC_RiceSheaf', 'AMJC_RiceInHull'):
        jp = ET.parse(ROOT / 'Languages/Japanese/DefInjected/ThingDef/AMJC_RiceProcessing.xml').getroot()
        assert jp.findtext(name + '.label') and jp.findtext(name + '.description')
    rice_recipes = ET.parse(ROOT / 'Languages/Japanese/DefInjected/RecipeDef/AMJC_RiceProcessing.xml').getroot()
    for op in ('Thresh', 'Hull'):
        for suffix in ('', 'Bulk'):
            name = 'AMJC_' + op + 'Rice' + suffix
            assert all(rice_recipes.findtext(name + '.' + field) for field in ('label', 'description', 'jobString'))
    return True


if __name__ == '__main__':
    validate()
    print('Upland rice XML and seven-crop analytical regression: PASS (27 cells/profile)')
