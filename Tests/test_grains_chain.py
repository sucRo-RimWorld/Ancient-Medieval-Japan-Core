"""Reject nutrition multiplication, bread-like storage and new research gates."""
import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile
import unittest
import xml.etree.ElementTree as ET
from amj_profile_xml import ROOT
from validate_grains_chain import validate, validate_mo_source


class ChainRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ('Defs','BaseWithoutMO','Compatibility','LegacyStartingScenarios'):
            shutil.copytree(ROOT/folder,self.root/folder)
        shutil.copyfile(ROOT/'loadFolders.xml',self.root/'loadFolders.xml')

    def mutate(self,path,xpath,text=None,new_element=None):
        f=self.root/path;xml=ET.parse(f);n=xml.find(xpath);assert n is not None
        if new_element is not None:n.append(ET.fromstring(new_element))
        else:n.text=text
        xml.write(f)
        with self.assertRaises(AssertionError):validate(self.root)

    def test_current_chain(self):validate(self.root)
    def test_flour_does_not_multiply_nutrition(self):
        self.mutate('BaseWithoutMO/Defs/Items_Flour.xml','ThingDef/statBases/Nutrition','0.1')
    def test_milling_does_not_create_straw(self):
        self.mutate('Defs/RecipeDefs/Recipes_GrainsMilling.xml','RecipeDef/products',new_element='<AMJC_Millet>1</AMJC_Millet>')
    def test_powder_food_not_bread_storage(self):
        self.mutate('Defs/ThingDefs_Items/Items_GrainsFood.xml','ThingDef/comps/li/daysToRotStart','8')
    def test_cooking_remains_research_free(self):
        self.mutate('Defs/RecipeDefs/Recipes_GrainsFood.xml','RecipeDef',new_element='<researchPrerequisite>Cooking</researchPrerequisite>')
    def test_mo_food_uses_mo_flour(self):
        self.mutate('Compatibility/MedievalOverhaul/Patches/MedievalOverhaul_GrainsFlour.xml','Operation[3]/value/li','AMJC_WheatFlour')
    def test_processing_workgiver_must_reach_its_benches(self):
        self.mutate('Defs/WorkGiverDefs/WorkGivers_Grains.xml','WorkGiverDef/fixedBillGiverDefs/li','CraftingSpot')
    def test_fallback_mill_requires_bill_worker(self):
        self.mutate('BaseWithoutMO/Defs/WorkGivers_Milling.xml','WorkGiverDef/giverClass','WorkGiver_PlantsCut')
    def test_real_simple_meal_jobs_are_wired_into_all_profiles(self):
        source = (ROOT/'Tests/E2E/GrainsSimulationSteps.cs').read_text(encoding='utf-8')
        ordered_inputs = ('AMJC_Millet', 'AMJC_Buckwheat', 'AMJC_Barley',
                          'AMJC_Wheat', 'RawRice')
        assert 'foreach (string grain in new[] { ' in source
        for name in ordered_inputs:
            assert source.count('"' + name + '"') >= 1, name
        assert 'await scope.SimpleMeal(grain)' in source
        assert 'public async Task SimpleMeal(string ingredient)' in source
        assert 'DefDatabase<RecipeDef>.GetNamed("CookMealSimple")' in source
        assert 'Campfire.BillStack.AddBill(bill)' in source
        assert 'bill.ingredientFilter.SetDisallowAll()' in source
        assert 'bill.ingredientFilter.SetAllow(grain, true)' in source
        assert 'giver.JobOnThing(worker, Campfire, true)' in source
        assert 'Count("MealSimple") == beforeMeals + outputCount' in source
        assert 'Count(ingredient) == beforeGrain - neededCount' in source
        assert 'Campfire.BillStack.Delete(bill)' in source
        assert source.count('await scope.Harvest("AMJC_Plant_Buckwheat_Soba", true)') >= 2
        for recipe in ('AMJC_ThreshMilletBulk', 'AMJC_HullMilletBulk',
                       'AMJC_ThreshBuckwheatBulk', 'AMJC_HullBuckwheatBulk',
                       'AMJC_ThreshBarleyBulk', 'AMJC_HullBarleyBulk',
                       'AMJC_ThreshWheatBulk'):
            assert 'await scope.Bill("' + recipe + '"' in source, recipe
        for name in ('vanilla', 'vanilla-ccto', 'mo', 'mo-ccto'):
            feature = (ROOT/'Tests/E2E/Profiles'/('grains-' + name + '.feature')).read_text(encoding='utf-8')
            assert '@quickstart:AmjStageAQuickstart @timeout:270' in feature
            assert 'Then Grains harvest and flour food Bills complete through real jobs' in feature
            assert feature.count('  Scenario:') == 6

    def test_mo_flour_job_accepts_declared_hay_only(self):
        source = (ROOT/'Tests/E2E/GrainsSimulationSteps.cs').read_text(encoding='utf-8')
        start = source.index('public async Task Bill(')
        end = source.index('public async Task SimpleMeal(', start)
        bill = source[start:end]
        # Every declared product (including Hay from MO CraftFlourBulk) must
        # increase by its exact recipe quantity. Undeclared Hay must not increase.
        assert 'recipe.products.ToDictionary(p => p.thingDef.defName' in bill
        assert 'products[p.thingDef.defName] + p.count' in bill
        assert 'if (!recipe.products.Any(p => p.thingDef.defName == "Hay"))' in bill
        assert 'ctx.Assert(Count("Hay") == hay,' in bill
        assert 'ctx.Assert(Count("Hay") == hay, recipeName + " must not create hay.");' not in bill
        assert 'if (!recipe.products.Any(p => p.thingDef.defName == "DankPyon_Straw"))' in bill
        # Actual MO 1.6 source contract is tested separately; don't assume
        # its native grinding recipe has no hay byproduct.

    def test_mo_16_archive_provider_contract(self):
        # Synthetic compressed MO provider: run without the proprietary game.
        things = """<Defs>
          <ThingDef><defName>DankPyon_Flour</defName><statBases><Nutrition>0.05</Nutrition></statBases></ThingDef>
          <ThingDef><defName>DankPyon_Millstone</defName><researchPrerequisites><li>DankPyon_BasicAgriculture</li></researchPrerequisites></ThingDef>
          <ThingDef><defName>DankPyon_Plant_Wheat</defName><plant><growDays>12</growDays><harvestYield>28</harvestYield><harvestedThingDef>DankPyon_RawWheat</harvestedThingDef></plant></ThingDef>
          <ThingDef><defName>DankPyon_RawWheat</defName></ThingDef>
        </Defs>"""
        recipes = """<Defs>
          <RecipeDef><defName>DankPyon_CraftFlour</defName><recipeUsers><li>DankPyon_Millstone</li></recipeUsers><ingredients><li><count>1</count></li></ingredients><products><DankPyon_Flour>1</DankPyon_Flour><Hay>1</Hay></products></RecipeDef>
          <RecipeDef><defName>DankPyon_CraftFlourBulk</defName><recipeUsers><li>DankPyon_Millstone</li></recipeUsers><ingredients><li><count>10</count></li></ingredients><products><DankPyon_Flour>10</DankPyon_Flour><Hay>10</Hay></products></RecipeDef>
        </Defs>"""
        worker = """<Defs><WorkGiverDef><defName>DankPyon_DoBillsMillstone</defName>
          <giverClass>WorkGiver_DoBill</giverClass><workType>Cooking</workType>
          <fixedBillGiverDefs><li>DankPyon_Millstone</li></fixedBillGiverDefs>
        </WorkGiverDef></Defs>"""
        archive = self.root/'3219596926.zip'
        def package(work):
            with ZipFile(archive,'w') as z:
                z.writestr('3219596926/1.6/Defs/Things.xml',things)
                z.writestr('3219596926/1.6/Defs/Recipes.xml',recipes)
                z.writestr('3219596926/1.6/Defs/WorkGivers.xml',work)
                z.writestr('3219596926/1.4/Defs/Things.xml',things)
        package(worker)
        validate_mo_source(archive)
        package(worker.replace('WorkGiver_DoBill','WorkGiver_PlantsCut'))
        with self.assertRaises(AssertionError):validate_mo_source(archive)
        package(worker.replace('DankPyon_Millstone</li>','OtherMillstone</li>'))
        with self.assertRaises(AssertionError):validate_mo_source(archive)

    def test_no_duplicate_fallback_in_mo(self):
        self.mutate('Defs/ThingDefs_Items/Items_GrainsFlour.xml','.',new_element='<ThingDef><defName>AMJC_WheatFlour</defName></ThingDef>')


if __name__ == '__main__':unittest.main()
