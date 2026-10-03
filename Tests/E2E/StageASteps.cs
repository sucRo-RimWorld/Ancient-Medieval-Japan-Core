using System;
using System.Collections.Generic;
using System.Linq;
using RimWorks.Pickle;
using RimWorld;
using Verse;

namespace AncientMedievalJapanCore.E2E
{
    [PickleSteps]
    public sealed class StageASteps
    {
        [Then("loaded AMJ Stage A crop and grain Defs match the design values")]
        public void AssertLoadedCropAndGrainDefs(PickleContext ctx)
        {
            ThingDef awa = RequireThingDef(ctx, "AMJC_Plant_FoxtailMillet_Awa");
            ctx.Require(awa.plant != null, "AMJC_Plant_FoxtailMillet_Awa is not a plant.");

            ctx.Assert(Math.Abs(awa.plant.growDays - 6f) < 0.001f, "Awa growDays should be 6.");
            ctx.Assert(Math.Abs(awa.plant.fertilityMin - 0.5f) < 0.001f, "Awa fertilityMin should be 0.5.");
            ctx.Assert(Math.Abs(awa.plant.fertilitySensitivity - 0.4f) < 0.001f, "Awa fertilitySensitivity should be 0.4.");
            ctx.Assert(Math.Abs(awa.plant.minGrowthTemperature - 8f) < 0.001f, "Awa minimum growth temperature should be 8 C.");
            ctx.Assert(Math.Abs(awa.plant.maxGrowthTemperature - 42f) < 0.001f, "Awa maximum growth temperature should be 42 C.");
            ctx.Assert(Math.Abs(awa.plant.minOptimalGrowthTemperature - 18f) < 0.001f, "Awa minimum optimal growth temperature should be 18 C.");
            ctx.Assert(Math.Abs(awa.plant.maxOptimalGrowthTemperature - 32f) < 0.001f, "Awa maximum optimal growth temperature should be 32 C.");
            ctx.Assert(awa.plant.sowMinSkill == 0, "Awa sowMinSkill should be 0.");
            ctx.Assert(Math.Abs(awa.plant.harvestYield - 13f) < 0.001f, "Awa harvest yield should be 13.");
            ctx.Assert(awa.plant.harvestedThingDef != null && awa.plant.harvestedThingDef.defName == "AMJC_RawMillet", "Awa must harvest AMJC_RawMillet.");

            ThingDef raw = RequireThingDef(ctx, "AMJC_RawMillet");
            ThingDef inHull = RequireThingDef(ctx, "AMJC_MilletInHull");
            ThingDef millet = RequireThingDef(ctx, "AMJC_Millet");

            AssertRotDays(ctx, raw, 120f);
            AssertRotDays(ctx, inHull, 120f);
            AssertRotDays(ctx, millet, 90f);

            ctx.Assert(!HasThingCategory(raw, "DankPyon_Cereal"), "Raw millet must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(inHull, "DankPyon_Cereal"), "Millet in hull must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(millet, "DankPyon_Cereal"), "Edible millet must not be in DankPyon_Cereal.");

            ctx.Assert(raw.ingestible != null && raw.ingestible.preferability == FoodPreferability.NeverForNutrition, "Raw millet must be non-food for normal nutrition.");
            ctx.Assert(inHull.ingestible != null && inHull.ingestible.preferability == FoodPreferability.NeverForNutrition, "Millet in hull must be non-food for normal nutrition.");
            ctx.Assert(millet.ingestible != null, "Edible millet must have ingestible properties.");
            ctx.Assert(Math.Abs(ReadStatBase(ctx, millet, StatDefOf.Nutrition) - 0.05f) < 0.001f, "Edible millet nutrition should be 0.05.");
        }

        [Then("loaded AMJ grain processing buildings and recipes match the design values")]
        public void AssertLoadedProcessingDefs(PickleContext ctx)
        {
            ThingDef spot = RequireThingDef(ctx, "AMJC_GrainProcessingSpot");
            ThingDef table = RequireThingDef(ctx, "AMJC_GrainProcessingTable");

            ctx.Assert(Math.Abs(ReadStatBase(ctx, spot, StatDefOf.WorkTableWorkSpeedFactor) - 0.5f) < 0.001f, "Simple grain processing spot speed should be 0.5.");
            ctx.Assert(Math.Abs(ReadStatBase(ctx, table, StatDefOf.WorkTableWorkSpeedFactor) - 1f) < 0.001f, "Grain processing table speed should be 1.0.");

            ctx.Assert(
                table.researchPrerequisites != null
                && table.researchPrerequisites.Any(x => x != null && x.defName == "DankPyon_BasicAgriculture"),
                "Grain processing table should require DankPyon_BasicAgriculture.");

            AssertRecipe(ctx, "AMJC_ThreshMillet", 15f, "AMJC_RawMillet", 1f,
                new Dictionary<string, int> { { "AMJC_MilletInHull", 1 }, { "DankPyon_Straw", 1 } });
            AssertRecipe(ctx, "AMJC_ThreshMilletBulk", 120f, "AMJC_RawMillet", 10f,
                new Dictionary<string, int> { { "AMJC_MilletInHull", 10 }, { "DankPyon_Straw", 10 } });
            AssertRecipe(ctx, "AMJC_HullMillet", 10f, "AMJC_MilletInHull", 1f,
                new Dictionary<string, int> { { "AMJC_Millet", 1 } });
            AssertRecipe(ctx, "AMJC_HullMilletBulk", 80f, "AMJC_MilletInHull", 10f,
                new Dictionary<string, int> { { "AMJC_Millet", 10 } });

            List<string> spotRecipes = DefDatabase<RecipeDef>.AllDefs
                .Where(x => x.recipeUsers != null && x.recipeUsers.Contains(spot) && x.defName.StartsWith("AMJC_"))
                .Select(x => x.defName)
                .OrderBy(x => x)
                .ToList();

            List<string> tableRecipes = DefDatabase<RecipeDef>.AllDefs
                .Where(x => x.recipeUsers != null && x.recipeUsers.Contains(table) && x.defName.StartsWith("AMJC_"))
                .Select(x => x.defName)
                .OrderBy(x => x)
                .ToList();

            ctx.Assert(spotRecipes.SequenceEqual(tableRecipes), "Both grain-processing stations should expose the same AMJ recipes.");
            ctx.Assert(spotRecipes.Count == 4, "Both grain-processing stations should expose exactly four Stage A millet bills.");
        }

        [Then("thirteen raw millet is conserved through bulk plus remainder processing")]
        public void AssertThirteenUnitConservation(PickleContext ctx)
        {
            RecipeDef threshOne = RequireRecipe(ctx, "AMJC_ThreshMillet");
            RecipeDef threshBulk = RequireRecipe(ctx, "AMJC_ThreshMilletBulk");
            RecipeDef hullOne = RequireRecipe(ctx, "AMJC_HullMillet");
            RecipeDef hullBulk = RequireRecipe(ctx, "AMJC_HullMilletBulk");

            const int rawCount = 13;
            int bulkRuns = rawCount / 10;
            int remainder = rawCount % 10;

            int inHull = bulkRuns * ProductCount(ctx, threshBulk, "AMJC_MilletInHull")
                + remainder * ProductCount(ctx, threshOne, "AMJC_MilletInHull");
            int straw = bulkRuns * ProductCount(ctx, threshBulk, "DankPyon_Straw")
                + remainder * ProductCount(ctx, threshOne, "DankPyon_Straw");

            int hullBulkRuns = inHull / 10;
            int hullRemainder = inHull % 10;
            int edible = hullBulkRuns * ProductCount(ctx, hullBulk, "AMJC_Millet")
                + hullRemainder * ProductCount(ctx, hullOne, "AMJC_Millet");

            ctx.Assert(inHull == 13, "Threshing 13 raw millet as x10 plus 3 singles should yield 13 millet in hull.");
            ctx.Assert(straw == 13, "Threshing 13 raw millet should yield 13 straw.");
            ctx.Assert(edible == 13, "Hulling the 13 millet in hull should yield 13 edible millet.");
            ctx.Assert(threshBulk.workAmount < threshOne.workAmount * 10f, "Bulk threshing should save work versus ten single jobs.");
            ctx.Assert(hullBulk.workAmount < hullOne.workAmount * 10f, "Bulk hulling should save work versus ten single jobs.");
        }

        [Then("edible millet is accepted by the vanilla simple meal ingredient filter")]
        public void AssertSimpleMealAcceptsMillet(PickleContext ctx)
        {
            ThingDef millet = RequireThingDef(ctx, "AMJC_Millet");
            RecipeDef simpleMeal = DefDatabase<RecipeDef>.GetNamedSilentFail("CookMealSimple");

            ctx.Require(simpleMeal != null, "Vanilla CookMealSimple RecipeDef was not found.");
            ctx.Require(simpleMeal.fixedIngredientFilter != null, "CookMealSimple has no fixed ingredient filter.");
            ctx.Assert(simpleMeal.fixedIngredientFilter.Allows(millet), "Edible AMJ millet should be accepted by the vanilla simple meal ingredient filter.");
        }

        private static void AssertRecipe(
            PickleContext ctx,
            string defName,
            float expectedWorkAmount,
            string inputDefName,
            float expectedInputCount,
            IDictionary<string, int> expectedProducts)
        {
            RecipeDef recipe = RequireRecipe(ctx, defName);

            ctx.Assert(Math.Abs(recipe.workAmount - expectedWorkAmount) < 0.001f, defName + " workAmount mismatch.");
            ctx.Assert(recipe.workSpeedStat == StatDefOf.GeneralLaborSpeed, defName + " should use GeneralLaborSpeed.");
            ctx.Assert(recipe.workSkill == SkillDefOf.Crafting, defName + " should use Crafting.");

            List<string> users = recipe.recipeUsers == null
                ? new List<string>()
                : recipe.recipeUsers.Where(x => x != null).Select(x => x.defName).OrderBy(x => x).ToList();

            ctx.Assert(
                users.SequenceEqual(new[] { "AMJC_GrainProcessingSpot", "AMJC_GrainProcessingTable" }.OrderBy(x => x)),
                defName + " must be available on both grain-processing stations and no others.");

            ThingDef inputDef = RequireThingDef(ctx, inputDefName);
            IngredientCount ingredient = recipe.ingredients == null
                ? null
                : recipe.ingredients.FirstOrDefault(x => x.filter != null && x.filter.Allows(inputDef));

            ctx.Require(ingredient != null, defName + " is missing expected input " + inputDefName + ".");
            ctx.Assert(Math.Abs(ingredient.GetBaseCount() - expectedInputCount) < 0.001f, defName + " input count mismatch.");

            foreach (KeyValuePair<string, int> expected in expectedProducts)
            {
                ctx.Assert(
                    ProductCount(ctx, recipe, expected.Key) == expected.Value,
                    defName + " product count mismatch for " + expected.Key + ".");
            }
        }

        private static int ProductCount(PickleContext ctx, RecipeDef recipe, string productDefName)
        {
            ctx.Require(recipe.products != null, recipe.defName + " has no products.");
            ThingDefCountClass product = recipe.products.FirstOrDefault(
                x => x.thingDef != null && x.thingDef.defName == productDefName);
            ctx.Require(product != null, recipe.defName + " is missing product " + productDefName + ".");
            return product.count;
        }

        private static void AssertRotDays(PickleContext ctx, ThingDef def, float expectedDays)
        {
            CompProperties_Rottable rot = def.comps == null
                ? null
                : def.comps.OfType<CompProperties_Rottable>().FirstOrDefault();

            ctx.Require(rot != null, def.defName + " is missing CompProperties_Rottable.");
            ctx.Assert(
                Math.Abs(rot.daysToRotStart - expectedDays) < 0.001f,
                def.defName + " daysToRotStart mismatch.");
        }

        private static bool HasThingCategory(ThingDef def, string categoryDefName)
        {
            return def.thingCategories != null
                && def.thingCategories.Any(x => x != null && x.defName == categoryDefName);
        }

        private static float ReadStatBase(PickleContext ctx, ThingDef def, StatDef stat)
        {
            ctx.Require(def.statBases != null, def.defName + " has no statBases.");
            StatModifier modifier = def.statBases.FirstOrDefault(x => x.stat == stat);
            ctx.Require(modifier != null, def.defName + " is missing stat " + stat.defName + ".");
            return modifier.value;
        }

        private static ThingDef RequireThingDef(PickleContext ctx, string defName)
        {
            ThingDef def = DefDatabase<ThingDef>.GetNamedSilentFail(defName);
            ctx.Require(def != null, "Required ThingDef '" + defName + "' was not found.");
            return def;
        }

        private static RecipeDef RequireRecipe(PickleContext ctx, string defName)
        {
            RecipeDef def = DefDatabase<RecipeDef>.GetNamedSilentFail(defName);
            ctx.Require(def != null, "Required RecipeDef '" + defName + "' was not found.");
            return def;
        }
    }
}
