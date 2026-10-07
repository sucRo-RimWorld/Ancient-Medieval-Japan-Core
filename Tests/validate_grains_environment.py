"""Finite-season yield model; not a calendar/weather/survival simulation."""
from itertools import product
from collections import Counter
from math import floor
from amj_profile_xml import ROOT, profile_xml

CROPS = ('AMJC_Plant_FoxtailMillet_Awa', 'AMJC_Plant_BarnyardMillet_Hie',
         'AMJC_Plant_ProsoMillet_Kibi', 'AMJC_Plant_Buckwheat_Soba',
         'AMJC_Plant_Barley', 'AMJC_Plant_Wheat')
FERTILITIES = (0.5, 1.0, 1.4)
TEMPERATURES = (10, 20, 30)
SEASONS = (5, 10, 20)  # effective full-light, non-resting growth days
FIELDS = ('growDays','harvestYield','fertilityMin','fertilitySensitivity',
          'minGrowthTemperature','minOptimalGrowthTemperature',
          'maxOptimalGrowthTemperature','maxGrowthTemperature')
# External MO wheat uses PlantProperties defaults for temperature. This is an
# explicit source assumption; loaded Pickle checks use the real game utility.
MO_WHEAT = (12,28,0.7,0.9,0,6,42,58)


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
        if profile == 'mo' and name == CROPS[-1]:
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
    expected = json.loads((ROOT/'Tests/Fixtures/Grains_Environment.json').read_text())
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
    print('Grains environment: PASS (27 cells/profile, six niches; analytical only)')
