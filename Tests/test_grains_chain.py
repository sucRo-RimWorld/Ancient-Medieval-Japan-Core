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
        for folder in ('Defs','BaseWithoutMO','Compatibility','LegacyStartingScenarios','Textures'):
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
    def test_meal_must_replace_inherited_comp_list(self):
        target = self.root/'Defs/ThingDefs_Items/Items_GrainsFood.xml'
        xml = ET.parse(target)
        del xml.find('ThingDef/comps').attrib['Inherit']
        xml.write(target)
        with self.assertRaises(AssertionError): validate(self.root)

    def test_meal_must_not_reference_unavailable_vanilla_texture(self):
        self.mutate('Defs/ThingDefs_Items/Items_GrainsFood.xml',
                    'ThingDef/graphicData/texPath', 'Things/Item/Meal/Simple')

    def test_meal_must_use_packaged_stack_graphics(self):
        self.mutate('Defs/ThingDefs_Items/Items_GrainsFood.xml',
                    'ThingDef/graphicData/graphicClass', 'Graphic_Single')

    def test_meal_must_include_every_stack_variant(self):
        path = self.root/'Textures/Things/Item/Resource/AMJC_Buckwheat/Buckwheat/Buckwheat_c.png'
        path.unlink()
        with self.assertRaises(AssertionError):
            validate(self.root)

    def test_meal_recipe_graphic_paths_are_source_backed(self):
        doc = ET.parse(ROOT/'Defs/ThingDefs_Items/Items_GrainsFood.xml')
        for food in doc.findall('ThingDef'):
            texture = food.findtext('graphicData/texPath')
            self.assertTrue(texture.startswith('Things/Item/Resource/AMJC_'))
            self.assertEqual(food.findtext('graphicData/graphicClass'), 'Graphic_StackCount')
            for variant in 'abc':
                self.assertTrue((ROOT/'Textures'/texture/(Path(texture).name + '_' + variant + '.png')).is_file(),
                                (food.findtext('defName'),variant))


    def test_mood_memory_must_have_stage_description(self):
        self.mutate('Defs/ThoughtDefs/Thoughts_GrainsFood.xml',
                    'ThoughtDef/stages/li/description', '')

    def test_production_fixture_uses_prepared_disposable_center(self):
        source = (ROOT/'Tests/E2E/GrainsSimulationSteps.cs').read_text(encoding='utf-8')
        assert 'center = map.Center;' in source
        assert 'CellRect.CenteredOn(center, 7).Cells' in source
        assert 'Quickstart map needs a clear 15x15 test area.' not in source
        assert 'foreach (Thing thing in cell.GetThingList(map).ToList()) thing.Destroy(DestroyMode.Vanish);' in source
        assert 'map.terrainGrid.SetTerrain(cell, TerrainDefOf.Soil);' in source
        assert 'foreach (KeyValuePair<IntVec3,TerrainDef> cell in terrain)' in source

    def test_powder_food_not_bread_storage(self):
        self.mutate('Defs/ThingDefs_Items/Items_GrainsFood.xml',
                    'ThingDef/comps/li[@Class="CompProperties_Rottable"]/daysToRotStart','8')
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
        for recipe in ('AMJC_ThreshRiceBulk', 'AMJC_HullRiceBulk'):
            assert 'await scope.Bill("' + recipe + '"' in source, recipe
        assert 'ctx.Require(raw == "AMJC_RiceSheaf"' in source
        for name in ('vanilla', 'vanilla-ccto', 'mo', 'mo-ccto'):
            feature = (ROOT/'Tests/E2E/Profiles'/('grains-' + name + '.feature')).read_text(encoding='utf-8')
            assert '@quickstart:AmjStageAQuickstart @timeout:270' in feature
            assert 'Then Grains harvest and flour food Bills complete through real jobs' in feature
            assert feature.count('  Scenario:') == 6

    def test_real_seasonal_sow_and_growth_uses_actual_game_jobs(self):
        source = (ROOT/'Tests/E2E/GrainsSimulationSteps.cs').read_text(encoding='utf-8')
        start = source.index('public async Task NativeSeasonalSowAndGrowth()')
        end = source.index('public async Task Harvest(', start)
        seasonal = source[start:end]
        assert 'await scope.NativeSeasonalSowAndGrowth();' in source
        # Real job provider + driver: reject assertions that only check XML,
        # PlantUtility or directly create a plant via ThingMaker.MakeThing.
        assert 'new WorkGiver_GrowerSow()' in seasonal
        assert 'giver.JobOnCell(worker, cell, true)' in seasonal
        assert 'JobDefOf.Sow' in seasonal and 'Start(riceJob,' in seasonal
        assert 'Start(barleyJob,' in seasonal
        assert 'await Complete(riceJob,' in seasonal
        assert 'await Complete(barleyJob,' in seasonal
        assert 'Find.TickManager.DoSingleTick()' in seasonal
        assert 'PlantLifeStage.Sowing' in seasonal
        assert 'ricePlant.GrowthRateFactor_Temperature == 0f' in seasonal
        assert 'barleyPlant.GrowthRateFactor_Temperature > 0f' in seasonal
        assert 'ricePlant.Growth > riceBeforeWarm' in seasonal
        assert 'barleyPlant.Growth > barleyBeforeCold' in seasonal
        assert 'GenDate.TicksPerQuadrum' in seasonal
        assert 'DebugSetTicksGame' in seasonal
        assert 'map.Biome.constantOutdoorTemperature = savedBiomeTemperature;' in seasonal
        assert 'map.snowGrid.SetDepth(pair.Key, pair.Value)' in seasonal
        assert 'zone.Delete(false)' in seasonal
        assert 'if (failure != null) failure.Throw();' in seasonal
        assert 'ThingMaker.MakeThing(rice' not in seasonal
        assert 'ThingMaker.MakeThing(barley' not in seasonal

    def test_seasonal_job_contract_is_not_only_a_static_projection(self):
        source = (ROOT/'Tests/E2E/GrainsSimulationSteps.cs').read_text(encoding='utf-8')
        seasonal = source.split('public async Task NativeSeasonalSowAndGrowth()', 1)[1]
        assert 'NativeSowOffer(barleyCell) == null' in seasonal
        assert 'PlantUtility.GrowthSeasonNow(barleyCell, map, barley)' in seasonal
        assert 'await SimulatePlantTicks(2200, "RiceColdStall")' in seasonal
        assert 'await SimulatePlantTicks(2200, "BarleyColdGrowth")' in seasonal
        assert 'await SimulatePlantTicks(2200, "RiceWarmRecovery")' in seasonal
        assert 'private void SetSeasonTemperature(float temp' in seasonal
        assert 'room.TempTracker.EqualizeTemperature()' in seasonal
        # Sunset / Plant.Resting caused the MO-only fifth native run to fail.
        # Gate actual calendar daytime and updated game sky before recovering
        # growth; merely moving the 25 C threshold is not a valid fix.
        assert 'int warmHourShift = (12 - GenLocalDate.HourOfDay(map) + 24) % 24;' in seasonal
        assert 'Find.TickManager.TicksGame + warmHourShift * GenDate.TicksPerHour' in seasonal
        assert 'map.skyManager.SkyManagerUpdate();' in seasonal
        assert 'warmDayPercent > 0.25f && warmDayPercent < 0.8f' in seasonal
        assert 'ricePlant.GrowthRateFactor_Light > 0.001f' in seasonal
        assert 'ricePlant.GrowthRate > 0f' in seasonal
        assert 'ricePlant.LifeStage == PlantLifeStage.Growing' in seasonal
        assert 'dayPercent=' in seasonal and 'sunGlow=' in seasonal
        assert 'growthRate=' in seasonal


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

    def test_mo_hay_removal_is_not_lost(self):
        path = self.root/'Compatibility/MedievalOverhaul/Patches/MedievalOverhaul_StageA_Wheat.xml'
        doc = ET.parse(path)
        target = '/Defs/RecipeDef[defName="DankPyon_CraftFlourBulk"]/products/Hay'
        nodes = [op.find('xpath') for op in doc.getroot().findall('Operation')
                 if op.get('Class') == 'PatchOperationRemove' and op.findtext('xpath') == target]
        self.assertEqual(len(nodes), 1)
        nodes[0].text = target.replace('/products/Hay', '/products/Flour')
        doc.write(path)
        with self.assertRaises(AssertionError):
            validate(self.root)

    def test_docs_match_active_grains_ownership(self):
        design = (ROOT/'Docs/Design.md').read_text(encoding='utf-8')
        profile = (ROOT/'Docs/GrainsProfileTesting.md').read_text(encoding='utf-8')
        cold = (ROOT/'Docs/Balance/Crops/ColdTolerance.md').read_text(encoding='utf-8')
        scenario = (ROOT/'Docs/ScenarioExtraction.md').read_text(encoding='utf-8')
        self.assertNotIn('Rice Cultivationは水田・稲・籾・米・稲作一次加工を所有する', design)
        self.assertNotIn('- 米・水田', design)
        self.assertNotIn('### 8.1 米・水田（Rice Cultivationへ移管）', design)
        self.assertNotIn('蕎麦粉を実装する場合は30日', design)
        self.assertIn('MedievalOverhaul_StageA_Wheat.xml', design)
        self.assertIn('Grains適用後の製粉成果物は小麦粉のみ', design)
        self.assertIn('Patches/UplandRice.xml', cold)
        self.assertIn('LegacyStartingScenarios/Defs/Scenarios/Scenarios_NewVillage.xml', scenario)
        self.assertNotIn('not a claim that the Production patch is already implemented', profile)

    def test_mo_16_archive_provider_contract(self):
        # Synthetic compressed MO provider: run without the proprietary game.
        things = """<Defs>
          <ThingDef><defName>DankPyon_Flour</defName><statBases><Nutrition>0.05</Nutrition></statBases></ThingDef>
          <ThingDef><defName>DankPyon_Millstone</defName><researchPrerequisites><li>DankPyon_BasicAgriculture</li></researchPrerequisites></ThingDef>
          <ThingDef><defName>DankPyon_Plant_Wheat</defName><plant><growDays>12</growDays><harvestYield>28</harvestYield><harvestedThingDef>DankPyon_RawWheat</harvestedThingDef></plant></ThingDef>
          <ThingDef><defName>DankPyon_RawWheat</defName></ThingDef>
        </Defs>"""
        recipes = """<Defs>
          <RecipeDef><defName>DankPyon_CraftFlour_Manual</defName><workAmount>300</workAmount><recipeUsers><li>CraftingSpot</li></recipeUsers><ingredients><li><count>1</count></li></ingredients><products><DankPyon_Flour>1</DankPyon_Flour><Hay>1</Hay></products></RecipeDef>
          <RecipeDef><defName>DankPyon_CraftFlour</defName><workAmount>100</workAmount><recipeUsers><li>DankPyon_Millstone</li></recipeUsers><ingredients><li><count>1</count></li></ingredients><products><DankPyon_Flour>1</DankPyon_Flour><Hay>1</Hay></products></RecipeDef>
          <RecipeDef><defName>DankPyon_CraftFlourBulk</defName><workAmount>800</workAmount><recipeUsers><li>DankPyon_Millstone</li></recipeUsers><ingredients><li><count>10</count></li></ingredients><products><DankPyon_Flour>10</DankPyon_Flour><Hay>10</Hay></products></RecipeDef>
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
        # Work values are balance data: stale MO provider work must not pass.
        with ZipFile(archive,'w') as z:
            z.writestr('3219596926/1.6/Defs/Things.xml',things)
            z.writestr('3219596926/1.6/Defs/Recipes.xml',
                       recipes.replace('<workAmount>800</workAmount>', '<workAmount>30</workAmount>'))
            z.writestr('3219596926/1.6/Defs/WorkGivers.xml',worker)
        with self.assertRaises(AssertionError):validate_mo_source(archive)
        package(worker.replace('DankPyon_Millstone</li>','OtherMillstone</li>'))
        with self.assertRaises(AssertionError):validate_mo_source(archive)

    def test_no_duplicate_fallback_in_mo(self):
        self.mutate('Defs/ThingDefs_Items/Items_GrainsFlour.xml','.',new_element='<ThingDef><defName>AMJC_WheatFlour</defName></ThingDef>')


if __name__ == '__main__':unittest.main()
