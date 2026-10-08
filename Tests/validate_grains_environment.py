"""Seven-crop finite-season yield model; not a calendar/weather/survival simulation."""
from itertools import product
from collections import Counter
from math import floor
import xml.etree.ElementTree as ET
from amj_profile_xml import ROOT, profile_xml

CROPS = ('AMJC_Plant_FoxtailMillet_Awa', 'AMJC_Plant_BarnyardMillet_Hie',
         'AMJC_Plant_ProsoMillet_Kibi', 'AMJC_Plant_Buckwheat_Soba',
         'AMJC_Plant_Barley', 'AMJC_Plant_Wheat', 'Plant_Rice')
FERTILITIES = (0.5, 1.0, 1.4)
TEMPERATURES = (10, 20, 30)
SEASONS = (5, 10, 20)
FIELDS = ('growDays','harvestYield','fertilityMin','fertilitySensitivity',
          'minGrowthTemperature','minOptimalGrowthTemperature',
          'maxOptimalGrowthTemperature','maxGrowthTemperature')
MO_WHEAT = (12,28,0.7,0.9,0,6,42,58)
UPLAND_RICE = (8,20,0.7,0.9,10,20,35,42)


def upland_rice_values(root=ROOT):
    patch = ET.parse(root/'Patches/UplandRice.xml').getroot()
    operations = patch.findall('Operation')
    assert len(operations) == 9, 'Upland rice patch must own eight numeric fields plus sowTags'
    for operation in operations:
        xpath = operation.findtext('xpath') or ''
        assert 'Plant_Rice' in xpath and 'RawRice' not in xpath, 'Upland patch must target only Plant_Rice'
    for field, expected in zip(FIELDS, UPLAND_RICE):
        values = [float(node.text) for node in patch.findall('.//value/'+field)]
        assert len(values) == 2 and all(value == expected for value in values), 'Upland rice patch differs for '+field
    tags = patch.findall('.//value/sowTags')
    assert len(tags) == 2
    for node in tags:
        assert [li.text for li in node.findall('li')] == ['Ground'], (
            'Upland rice must be field-sown only; Hydroponic must stay removed')
    return UPLAND_RICE


def output(values, fertility, temperature, season):
    days, yield_, minimum, sensitivity, low, ideal_low, ideal_high, high = values
    assert days > 0 and yield_ > 0 and 0 <= minimum and 0 <= sensitivity <= 1
    assert low < ideal_low <= ideal_high < high, 'Invalid temperature interval'
    if fertility < minimum:
        return 0
    temp_factor = (temperature-low)/(ideal_low-low) if temperature < ideal_low else (
        (high-temperature)/(high-ideal_high) if temperature > ideal_high else 1)
    rate = max(0,min(1,temp_factor)) * (1-sensitivity+fertility*sensitivity)
    return floor(season*rate/days + 1e-6)*yield_


def matrix(root=ROOT, profile='vanilla'):
    defs = {n.findtext('defName'): n for n in profile_xml(profile,root)}
    crops = []
    for name in CROPS:
        if name == 'Plant_Rice':
            crops.append(upland_rice_values(root))
        elif profile == 'mo' and name == 'AMJC_Plant_Wheat':
            crops.append(MO_WHEAT)
        else:
            crops.append(tuple(float(defs[name].findtext('plant/'+field)) for field in FIELDS))
    rows = []
    for fertility, temperature, season in product(FERTILITIES,TEMPERATURES,SEASONS):
        yields = [output(c,fertility,temperature,season) for c in crops]
        best = max(yields)
        winners = [CROPS[i] for i,y in enumerate(yields) if y == best and best > 0]
        rows.append(dict(fertility=fertility,temperature=temperature,season=season,
                         yields=yields,winners=winners))
    return rows


def validate(root=ROOT):
    import json
    expected = json.loads((root/'Tests/Fixtures/Grains_Environment.json').read_text())
    for profile in ('vanilla','mo'):
        rows = matrix(root,profile)
        assert rows == expected[profile], 'Environmental yield/choice changed: '+profile
        viable = [row for row in rows if row['winners']]
        wins = Counter(name for row in viable for name in row['winners'])
        assert set(wins) == set(CROPS), 'Every grain must retain a representative niche'
        assert max(wins.values())*3 < len(viable)*2, 'One crop wins >=2/3 of viable cells'
    return True


if __name__ == '__main__':
    validate()
    print('Grains environment: PASS (27 cells/profile, seven niches; analytical only)')
