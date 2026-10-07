"""Static Base/MO flour-chain contracts; no XML inheritance/game execution claim."""
import xml.etree.ElementTree as ET
from pathlib import Path
from amj_profile_xml import ROOT, profile_xml

SHARED_NAMES = {
    'AMJC_BuckwheatFlour','AMJC_MilletFlour','AMJC_Houtou','AMJC_Sobagaki',
    'AMJC_MilletDumplings','AMJC_AteFlourFood','AMJC_MillBuckwheat','AMJC_MillMillet',
    'AMJC_CookHoutou','AMJC_CookSobagaki','AMJC_CookMilletDumplings',
}
FALLBACK_NAMES = {'AMJC_Plant_Wheat','AMJC_RawWheat','AMJC_WheatFlour','AMJC_ManualMillstone','AMJC_MillWheat'}


def validate(root=ROOT):
    for profile in ('vanilla','mo'):
        doc = profile_xml(profile, root)
        defs = {n.findtext('defName'): n for n in doc if n.findtext('defName')}
        assert len(defs) == len([n for n in doc if n.findtext('defName')]), 'Duplicate DefName'
        assert SHARED_NAMES <= defs.keys()
        if profile == 'mo':
            assert FALLBACK_NAMES.isdisjoint(defs), 'Fallback wheat/flour/mill leaked into MO'
        else:
            assert FALLBACK_NAMES <= defs.keys()
            p = defs['AMJC_Plant_Wheat'].find('plant')
            for key, value in {'growDays':12,'harvestYield':28,'fertilityMin':0.7,'fertilitySensitivity':0.9,
                               'minGrowthTemperature':0,'sowMinSkill':0}.items():
                assert float(p.findtext(key)) == value, key
            assert p.findtext('harvestedThingDef') == 'AMJC_RawWheat'
            assert p.find('sowResearchPrerequisites') is None
            assert float(defs['AMJC_RawWheat'].findtext('comps/li/daysToRotStart')) == 120
            assert defs['AMJC_RawWheat'].findtext('ingestible/preferability') == 'NeverForNutrition'
            stone = defs['AMJC_ManualMillstone']
            assert stone.find('researchPrerequisites') is None
            assert stone.findtext('costList/BlocksGranite') == '30' and stone.findtext('costList/WoodLog') == '20'
        for name, count in [('AMJC_ThreshWheat',1), ('AMJC_ThreshWheatBulk',10)]:
            rec = defs[name]
            expected = 'DankPyon_RawWheat' if profile == 'mo' else 'AMJC_RawWheat'
            assert rec.findtext('ingredients/li/filter/thingDefs/li') == expected
            assert float(rec.findtext('ingredients/li/count')) == count
            assert int(rec.findtext('products/AMJC_Wheat')) == count
            assert [n.tag for n in rec.findall('products/*')] == (['AMJC_Wheat','DankPyon_Straw'] if profile == 'mo' else ['AMJC_Wheat'])
        chains = [('AMJC_MillBuckwheat','AMJC_Buckwheat','AMJC_BuckwheatFlour'),
                  ('AMJC_MillMillet','AMJC_Millet','AMJC_MilletFlour')]
        if profile == 'vanilla':chains += [('AMJC_MillWheat','AMJC_Wheat','AMJC_WheatFlour')]
        for recipe, grain, flour in chains:
            rec = defs[recipe]
            assert rec.findtext('ingredients/li/filter/thingDefs/li') == grain
            amount = float(rec.findtext('ingredients/li/count'))
            output = float(rec.findtext('products/'+flour))
            assert len(rec.findall('products/*')) == 1
            assert amount * float(defs[grain].findtext('statBases/Nutrition')) == output * float(defs[flour].findtext('statBases/Nutrition'))
            assert rec.findtext('recipeUsers/li') == ('DankPyon_Millstone' if profile == 'mo' else 'AMJC_ManualMillstone')
            assert rec.find('researchPrerequisite') is None and rec.find('researchPrerequisites') is None
            assert float(defs[flour].findtext('comps/li/daysToRotStart')) == 60
            assert defs[flour].findtext('ingestible/preferability') == 'NeverForNutrition'
        for suffix, flour in [('Houtou','DankPyon_Flour' if profile == 'mo' else 'AMJC_WheatFlour'),
                              ('Sobagaki','AMJC_BuckwheatFlour'),('MilletDumplings','AMJC_MilletFlour')]:
            rec = defs['AMJC_Cook'+suffix];food=defs['AMJC_'+suffix]
            assert rec.findtext('ingredientValueGetterClass') == 'IngredientValueGetter_Nutrition'
            assert rec.findtext('ingredients/li/filter/thingDefs/li') == flour
            assert rec.findtext('fixedIngredientFilter/thingDefs/li') == flour
            assert float(rec.findtext('ingredients/li/count')) == 0.5
            assert rec.findtext('products/AMJC_'+suffix) == '1'
            assert len(rec.findall('products/*')) == 1
            assert float(food.findtext('statBases/Nutrition')) == 0.9
            assert float(food.findtext('comps/li/daysToRotStart')) == 2.5
            assert food.findtext('ingestible/tasteThought') == 'AMJC_AteFlourFood'
            assert food.findtext('ingestible/preferability') == 'MealSimple'
            assert rec.find('researchPrerequisite') is None and rec.find('researchPrerequisites') is None
            assert [n.text for n in rec.findall('recipeUsers/li')] == ['Campfire','ElectricStove','FueledStove']
        assert float(defs['AMJC_AteFlourFood'].findtext('stages/li/baseMoodEffect')) == 2
    patch = ET.parse(root/'BaseWithoutMO/Patches/CCTO_Wheat.xml')
    assert patch.findtext('.//coldDeathTemperature') == '-6'
    assert patch.findtext('.//xpath') == '/Defs/ThingDef[defName="AMJC_Plant_Wheat"]'
    mill_patch = ET.parse(root/'Compatibility/MedievalOverhaul/Patches/MedievalOverhaul_GrainsMillstone.xml')
    assert mill_patch.findtext('Operation/xpath') == '/Defs/ThingDef[defName="DankPyon_Millstone"]/researchPrerequisites'
    assert mill_patch.find('Operation/match').get('Class') == 'PatchOperationRemove'
    print('Grains Base/MO wheat/flour/milling/minimum-food static contracts: PASS')


def validate_mo_source(mo_root):
    source = Path(mo_root)
    defs_root = source/'1.6/Defs' if (source/'1.6/Defs').is_dir() else source/'Defs'
    index = {}
    for path in defs_root.rglob('*.xml'):
        for n in ET.parse(path).getroot():
            name = n.findtext('defName')
            if name:index.setdefault((n.tag,name),[]).append(n)
    def get(typ,name):
        matches=index.get((typ,name),[]);assert len(matches)==1, name
        return matches[0]
    flour=get('ThingDef','DankPyon_Flour')
    assert float(flour.findtext('statBases/Nutrition')) == 0.05
    stone=get('ThingDef','DankPyon_Millstone')
    assert stone.find('researchPrerequisites') is not None
    recipe=get('RecipeDef','DankPyon_CraftFlour')
    assert recipe.findtext('recipeUsers/li') == 'DankPyon_Millstone'
    assert float(recipe.findtext('ingredients/li/count')) == float(recipe.findtext('products/DankPyon_Flour'))
    assert recipe.find('products/Hay') is not None
    print('Supplied MO 1.6 flour nutrition/mill/recipe/research patch target audit: PASS')


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mo-root',type=Path)
    args=parser.parse_args()
    validate()
    if args.mo_root:validate_mo_source(args.mo_root)
