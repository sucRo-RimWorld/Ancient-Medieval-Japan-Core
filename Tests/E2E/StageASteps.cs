using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;
using RimWorks.Pickle;
using RimWorld;
using Verse;

namespace AncientMedievalJapanCore.E2E
{
    // Pickle can resume its scenario pipeline on a worker thread. Unity textures
    // and live Verse map collections must always be accessed in the driver Update.
    internal static class RuntimeThread
    {
        public static Task Run(Action assertion)
        {
            var completion = new TaskCompletionSource<bool>();
            RimWorks.Pickle.Runtime.PickleDriver.Post(delegate
            {
                try
                {
                    if (!UnityData.IsInMainThread)
                        throw new InvalidOperationException("AMJ runtime assertion must run on the Unity main thread.");
                    assertion();
                    completion.SetResult(true);
                }
                catch (Exception error) { completion.SetException(error); }
            });
            return completion.Task;
        }
    }

    [PickleSteps]
    public sealed class StageASteps
    {
        [Then("loaded AMJ Stage A crop and grain Defs match the design values")]
        public Task AssertLoadedCropAndGrainDefs(PickleContext ctx)
        {
            return RuntimeThread.Run(delegate { AssertLoadedCropAndGrainDefsOnMainThread(ctx); });
        }

        private void AssertLoadedCropAndGrainDefsOnMainThread(PickleContext ctx)
        {
            string checkpoint = "Awa crop";
            try
            {
            ThingDef awa = RequireThingDef(ctx, "AMJC_Plant_FoxtailMillet_Awa");
            if (awa.plant == null)
            {
                throw new InvalidOperationException("AMJC_Plant_FoxtailMillet_Awa is not a plant.");
            }

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

                checkpoint = "Hie and Kibi crop Defs";
            AssertLoadedMilletCrop(ctx, "AMJC_Plant_BarnyardMillet_Hie", 6f, 12f, 0.5f, 5f, 40f, 15f, 30f);
            AssertLoadedMilletCrop(ctx, "AMJC_Plant_ProsoMillet_Kibi", 5f, 11f, 0.3f, 8f, 42f, 18f, 32f);
                checkpoint = "Soba and Barley crop Defs";
            AssertLoadedCrop(ctx, "AMJC_Plant_Buckwheat_Soba", 4f, 8f, 0.4f, 0.25f, 5f, 35f, 12f, 25f, 1, "AMJC_RawBuckwheat");
            AssertLoadedCrop(ctx, "AMJC_Plant_Barley", 10f, 22f, 0.5f, 0.6f, 0f, 35f, 5f, 22f, 2, "AMJC_RawBarley");
            ThingDef barleyPlant = RequireThingDef(ctx, "AMJC_Plant_Barley");
            ctx.Assert(barleyPlant.plant.sowResearchPrerequisites == null
                || barleyPlant.plant.sowResearchPrerequisites.Count == 0,
                "AMJG barley must remain research-free with MO enabled.");
            ThingDef grainTable = RequireThingDef(ctx, "AMJC_GrainProcessingTable");
            ctx.Assert(grainTable.researchPrerequisites == null
                || grainTable.researchPrerequisites.Count == 0,
                "AMJG processing table must remain research-free with MO enabled.");
            ctx.Assert(grainTable.costList != null && grainTable.costList.Count == 1
                && grainTable.costList[0].thingDef.defName == "Steel"
                && grainTable.costList[0].count == 30,
                "AMJG processing table must retain its 30 Steel cost with MO enabled.");

                checkpoint = "grain ThingDef lookup and storage";
            ThingDef raw = RequireThingDef(ctx, "AMJC_RawMillet");
            ThingDef inHull = RequireThingDef(ctx, "AMJC_MilletInHull");
            ThingDef millet = RequireThingDef(ctx, "AMJC_Millet");
                checkpoint = "millet texture runtime resolution";
            AssertMilletTextures(ctx, raw, "RawMillet");
            AssertMilletTextures(ctx, inHull, "MilletInHull");
            AssertMilletTextures(ctx, millet, "Millet");
                checkpoint = "grain ThingDef lookup and storage";
            ThingDef rawBuckwheat = RequireThingDef(ctx, "AMJC_RawBuckwheat");
            ThingDef buckwheatInHull = RequireThingDef(ctx, "AMJC_BuckwheatInHull");
            ThingDef buckwheat = RequireThingDef(ctx, "AMJC_Buckwheat");
            ThingDef rawBarley = RequireThingDef(ctx, "AMJC_RawBarley");
            ThingDef barleyInHull = RequireThingDef(ctx, "AMJC_BarleyInHull");
            ThingDef barley = RequireThingDef(ctx, "AMJC_Barley");
            ThingDef rawWheat = RequireThingDef(ctx, "DankPyon_RawWheat");
            ThingDef wheat = RequireThingDef(ctx, "AMJC_Wheat");
            ThingDef flour = RequireThingDef(ctx, "DankPyon_Flour");
            ThingDef wheatPlant = RequireThingDef(ctx, "DankPyon_Plant_Wheat");

                checkpoint = "MO wheat patched crop Def";
            ctx.Assert(wheatPlant.thingClass == typeof(Plant), "MO wheat must use normal Plant after AMJ removes harvest-time secondary drop.");
            ctx.Assert(wheatPlant.plant != null, "MO wheat must remain a plant.");
            ctx.Assert(Math.Abs(wheatPlant.plant.growDays - 12f) < 0.001f, "MO wheat growDays should remain 12.");
            ctx.Assert(Math.Abs(wheatPlant.plant.harvestYield - 28f) < 0.001f, "MO wheat harvestYield should remain 28.");
            ctx.Assert(Math.Abs(wheatPlant.plant.fertilityMin - 0.7f) < 0.001f, "AMJ wheat fertilityMin should be 0.7.");
            ctx.Assert(Math.Abs(wheatPlant.plant.fertilitySensitivity - 0.9f) < 0.001f, "MO wheat fertilitySensitivity should remain 0.9.");
            ctx.Assert(
                wheatPlant.plant.harvestedThingDef != null
                && wheatPlant.plant.harvestedThingDef.defName == "DankPyon_RawWheat",
                "MO wheat must still harvest DankPyon_RawWheat.");
            ctx.Assert(
                wheatPlant.plant.sowResearchPrerequisites != null
                && wheatPlant.plant.sowResearchPrerequisites.Any(x => x != null && x.defName == "DankPyon_BasicAgriculture"),
                "MO wheat must retain DankPyon_BasicAgriculture.");
            ctx.Assert(
                wheatPlant.modExtensions == null
                || !wheatPlant.modExtensions.Any(x => x != null && x.GetType().FullName == "MedievalOverhaul.SecondaryPlantDropExtension"),
                "AMJ wheat must not retain the MO harvest-time secondary-drop extension.");

                checkpoint = "fertility 0.50 crop roles";
            AssertThinSoilCropRoles(ctx);

                checkpoint = "grain ThingDef lookup and storage";
            AssertRotDays(ctx, raw, 120f);
            AssertRotDays(ctx, inHull, 120f);
            AssertRotDays(ctx, millet, 90f);
            AssertRotDays(ctx, rawBuckwheat, 120f);
            AssertRotDays(ctx, buckwheatInHull, 120f);
            AssertRotDays(ctx, buckwheat, 60f);
            AssertRotDays(ctx, rawBarley, 120f);
            AssertRotDays(ctx, barleyInHull, 120f);
            AssertRotDays(ctx, barley, 90f);
            AssertRotDays(ctx, rawWheat, 120f);
            AssertRotDays(ctx, wheat, 90f);
            AssertRotDays(ctx, flour, 60f);

                checkpoint = "grain categories";
            ctx.Assert(!HasThingCategory(raw, "DankPyon_Cereal"), "Raw millet must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(inHull, "DankPyon_Cereal"), "Millet in hull must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(millet, "DankPyon_Cereal"), "Edible millet must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(rawBuckwheat, "DankPyon_Cereal"), "Raw buckwheat must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(buckwheatInHull, "DankPyon_Cereal"), "Buckwheat in hull must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(buckwheat, "DankPyon_Cereal"), "Edible buckwheat must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(rawBarley, "DankPyon_Cereal"), "Raw barley must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(barleyInHull, "DankPyon_Cereal"), "Barley in hull must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(barley, "DankPyon_Cereal"), "Edible barley must not be in DankPyon_Cereal.");
            ctx.Assert(!HasThingCategory(rawWheat, "DankPyon_Cereal"), "Unthreshed MO wheat must not remain in DankPyon_Cereal.");
            ctx.Assert(HasThingCategory(wheat, "DankPyon_Cereal"), "Threshed AMJ wheat grain must be in DankPyon_Cereal.");

                checkpoint = "grain ingestible and nutrition properties";
            ctx.Assert(raw.ingestible != null && raw.ingestible.preferability == FoodPreferability.NeverForNutrition, "Raw millet must be non-food for normal nutrition.");
            ctx.Assert(inHull.ingestible != null && inHull.ingestible.preferability == FoodPreferability.NeverForNutrition, "Millet in hull must be non-food for normal nutrition.");
            ctx.Assert(millet.ingestible != null, "Edible millet must have ingestible properties.");
            ctx.Assert(Math.Abs(ReadStatBase(ctx, millet, StatDefOf.Nutrition) - 0.05f) < 0.001f, "Edible millet nutrition should be 0.05.");
            ctx.Assert(rawBuckwheat.ingestible != null && rawBuckwheat.ingestible.preferability == FoodPreferability.NeverForNutrition, "Raw buckwheat must be non-food for normal nutrition.");
            ctx.Assert(buckwheatInHull.ingestible != null && buckwheatInHull.ingestible.preferability == FoodPreferability.NeverForNutrition, "Buckwheat in hull must be non-food for normal nutrition.");
            ctx.Assert(buckwheat.ingestible != null, "Edible buckwheat must have ingestible properties.");
            ctx.Assert(Math.Abs(ReadStatBase(ctx, buckwheat, StatDefOf.Nutrition) - 0.05f) < 0.001f, "Edible buckwheat nutrition should be 0.05.");
            ctx.Assert(rawBarley.ingestible != null && rawBarley.ingestible.preferability == FoodPreferability.NeverForNutrition, "Raw barley must be non-food for normal nutrition.");
            ctx.Assert(barleyInHull.ingestible != null && barleyInHull.ingestible.preferability == FoodPreferability.NeverForNutrition, "Barley in hull must be non-food for normal nutrition.");
            ctx.Assert(barley.ingestible != null, "Edible barley must have ingestible properties.");
            ctx.Assert(Math.Abs(ReadStatBase(ctx, barley, StatDefOf.Nutrition) - 0.05f) < 0.001f, "Edible barley nutrition should be 0.05.");
            ctx.Assert(rawWheat.ingestible != null && rawWheat.ingestible.preferability == FoodPreferability.NeverForNutrition, "Unthreshed wheat must remain non-food.");
            ctx.Assert(wheat.ingestible != null, "Threshed wheat grain must be edible.");
            ctx.Assert(Math.Abs(ReadStatBase(ctx, wheat, StatDefOf.Nutrition) - 0.05f) < 0.001f, "Edible wheat nutrition should be 0.05.");
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException(
                    "Stage A crop/grain validation failed at checkpoint '" + checkpoint
                    + "': " + ex.GetType().Name + ": " + ex.Message,
                    ex);
            }
        }

        [Then("loaded AMJ crop CCTO compatibility data matches the cold tolerance design")]
        public void AssertLoadedCropCctoCompatibility(PickleContext ctx)
        {
            AssertLoadedCctoExtension(ctx, "AMJC_Plant_FoxtailMillet_Awa", -3f);
            AssertLoadedCctoExtension(ctx, "AMJC_Plant_BarnyardMillet_Hie", -2f);
            AssertLoadedCctoExtension(ctx, "AMJC_Plant_ProsoMillet_Kibi", -3f);
            AssertLoadedCctoExtension(ctx, "AMJC_Plant_Buckwheat_Soba", -2f);
            AssertLoadedCctoExtension(ctx, "AMJC_Plant_Barley", -8f);
        }

        private static void AssertMilletTextures(PickleContext ctx, ThingDef def, string stem)
        {
            string path = "Things/Item/Resource/AMJC_Millet/" + stem;

            if (def.graphicData == null)
            {
                throw new InvalidOperationException(def.defName + " has no graphicData.");
            }

            ctx.Assert(def.graphicData.texPath == path, def.defName + " texture directory must match.");
            ctx.Assert(def.graphicData.graphicClass == typeof(Graphic_StackCount), def.defName + " must retain stack graphics.");

            foreach (string suffix in new[] { "a", "b", "c" })
            {
                UnityEngine.Texture2D texture = ContentFinder<UnityEngine.Texture2D>.Get(path + "/" + stem + "_" + suffix, false);
                ctx.Require(texture != null && texture != BaseContent.BadTex, "Unity must load " + stem + "_" + suffix);
                ctx.Assert(texture.width == 256 && texture.height == 256, "Loaded millet texture must be 256x256.");
            }

            Graphic_StackCount stackGraphic = def.graphicData.Graphic as Graphic_StackCount;
            if (stackGraphic == null)
            {
                throw new InvalidOperationException(
                    def.defName + " graphicData did not resolve to Graphic_StackCount at runtime.");
            }

            foreach (int count in new[] { 1, 2, def.stackLimit })
            {
                Graphic subGraphic = stackGraphic.SubGraphicForStackCount(count, def);
                if (subGraphic == null)
                {
                    throw new InvalidOperationException(
                        def.defName + " resolved a null subGraphic at stackCount " + count + ".");
                }

                UnityEngine.Material material = subGraphic.MatSingle;
                ctx.Assert(
                    material != null
                    && material.mainTexture != null
                    && material.mainTexture != BaseContent.BadTex,
                    def.defName + " must resolve a real stack texture at count " + count);
            }
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
            AssertRecipe(ctx, "AMJC_ThreshBuckwheat", 15f, "AMJC_RawBuckwheat", 1f,
                new Dictionary<string, int> { { "AMJC_BuckwheatInHull", 1 }, { "DankPyon_Straw", 1 } });
            AssertRecipe(ctx, "AMJC_ThreshBuckwheatBulk", 120f, "AMJC_RawBuckwheat", 10f,
                new Dictionary<string, int> { { "AMJC_BuckwheatInHull", 10 }, { "DankPyon_Straw", 10 } });
            AssertRecipe(ctx, "AMJC_HullBuckwheat", 10f, "AMJC_BuckwheatInHull", 1f,
                new Dictionary<string, int> { { "AMJC_Buckwheat", 1 } });
            AssertRecipe(ctx, "AMJC_HullBuckwheatBulk", 80f, "AMJC_BuckwheatInHull", 10f,
                new Dictionary<string, int> { { "AMJC_Buckwheat", 10 } });
            AssertRecipe(ctx, "AMJC_ThreshBarley", 15f, "AMJC_RawBarley", 1f,
                new Dictionary<string, int> { { "AMJC_BarleyInHull", 1 }, { "DankPyon_Straw", 1 } });
            AssertRecipe(ctx, "AMJC_ThreshBarleyBulk", 120f, "AMJC_RawBarley", 10f,
                new Dictionary<string, int> { { "AMJC_BarleyInHull", 10 }, { "DankPyon_Straw", 10 } });
            AssertRecipe(ctx, "AMJC_HullBarley", 10f, "AMJC_BarleyInHull", 1f,
                new Dictionary<string, int> { { "AMJC_Barley", 1 } });
            AssertRecipe(ctx, "AMJC_HullBarleyBulk", 80f, "AMJC_BarleyInHull", 10f,
                new Dictionary<string, int> { { "AMJC_Barley", 10 } });
            AssertRecipe(ctx, "AMJC_ThreshWheat", 15f, "DankPyon_RawWheat", 1f,
                new Dictionary<string, int> { { "AMJC_Wheat", 1 }, { "DankPyon_Straw", 1 } });
            AssertRecipe(ctx, "AMJC_ThreshWheatBulk", 120f, "DankPyon_RawWheat", 10f,
                new Dictionary<string, int> { { "AMJC_Wheat", 10 }, { "DankPyon_Straw", 10 } });

            AssertMoFlourRecipe(ctx, "DankPyon_CraftFlour_Manual", 1);
            AssertMoFlourRecipe(ctx, "DankPyon_CraftFlour", 1);
            AssertMoFlourRecipe(ctx, "DankPyon_CraftFlourBulk", 10);

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
            ctx.Assert(spotRecipes.Count == 14, "Both grain-processing stations should expose exactly fourteen Stage A grain-processing bills.");
        }

        [Then("stage A crops preserve distinct gameplay roles")]
        public void AssertDistinctCropRoles(PickleContext ctx)
        {
            ThingDef awa = RequireThingDef(ctx, "AMJC_Plant_FoxtailMillet_Awa");
            ThingDef hie = RequireThingDef(ctx, "AMJC_Plant_BarnyardMillet_Hie");
            ThingDef kibi = RequireThingDef(ctx, "AMJC_Plant_ProsoMillet_Kibi");
            ThingDef soba = RequireThingDef(ctx, "AMJC_Plant_Buckwheat_Soba");
            ThingDef barley = RequireThingDef(ctx, "AMJC_Plant_Barley");
            ThingDef wheat = RequireThingDef(ctx, "DankPyon_Plant_Wheat");

            ThingDef[] earlyCrops = { awa, hie, kibi, soba };
            for (int i = 0; i < earlyCrops.Length; i++)
            {
                ThingDef crop = earlyCrops[i];
                ctx.Assert(
                    crop.plant.sowResearchPrerequisites == null
                    || crop.plant.sowResearchPrerequisites.Count == 0,
                    crop.defName + " must remain available before Basic Agriculture.");
            }

            ctx.Assert(
                HasSowResearch(barley, "DankPyon_BasicAgriculture"),
                "Barley must remain a post-Basic-Agriculture crop.");
            ctx.Assert(
                HasSowResearch(wheat, "DankPyon_BasicAgriculture"),
                "Wheat must remain a post-Basic-Agriculture crop.");

            ctx.Assert(
                soba.plant.growDays < kibi.plant.growDays
                && kibi.plant.growDays < awa.plant.growDays
                && Math.Abs(awa.plant.growDays - hie.plant.growDays) < 0.001f
                && awa.plant.growDays < barley.plant.growDays
                && barley.plant.growDays < wheat.plant.growDays,
                "Stage A growth times must preserve the Soba < Kibi < Awa/Hie < Barley < Wheat progression.");

            ctx.Assert(
                soba.plant.harvestYield < kibi.plant.harvestYield
                && kibi.plant.harvestYield < hie.plant.harvestYield
                && hie.plant.harvestYield < awa.plant.harvestYield
                && awa.plant.harvestYield < barley.plant.harvestYield
                && barley.plant.harvestYield < wheat.plant.harvestYield,
                "Shorter Stage A crops must retain lower per-harvest output than the longer grain crops.");

            ctx.Assert(
                barley.plant.minGrowthTemperature < soba.plant.minGrowthTemperature
                && Math.Abs(soba.plant.minGrowthTemperature - hie.plant.minGrowthTemperature) < 0.001f
                && soba.plant.minGrowthTemperature < awa.plant.minGrowthTemperature
                && Math.Abs(awa.plant.minGrowthTemperature - kibi.plant.minGrowthTemperature) < 0.001f,
                "Cold-growth roles must remain Barley < Soba/Hie < Awa/Kibi.");

            ctx.Assert(
                soba.plant.fertilitySensitivity < kibi.plant.fertilitySensitivity
                && kibi.plant.fertilitySensitivity < awa.plant.fertilitySensitivity
                && awa.plant.fertilitySensitivity < hie.plant.fertilitySensitivity
                && hie.plant.fertilitySensitivity < barley.plant.fertilitySensitivity
                && barley.plant.fertilitySensitivity < wheat.plant.fertilitySensitivity,
                "Fertility sensitivity must preserve Soba < Kibi < Awa < Hie < Barley < Wheat.");

            AssertThinSoilCropRoles(ctx);

            ctx.Assert(
                soba.plant.growDays < awa.plant.growDays
                && soba.plant.harvestYield < awa.plant.harvestYield,
                "Soba's short-season advantage must retain a lower per-harvest yield tradeoff.");
            ctx.Assert(
                hie.plant.minGrowthTemperature < awa.plant.minGrowthTemperature
                && hie.plant.harvestYield < awa.plant.harvestYield
                && hie.plant.fertilitySensitivity > awa.plant.fertilitySensitivity,
                "Hie's cooler growth threshold must retain yield/fertility tradeoffs versus Awa.");
            ctx.Assert(
                kibi.plant.growDays < awa.plant.growDays
                && kibi.plant.harvestYield < awa.plant.harvestYield
                && kibi.plant.fertilitySensitivity < awa.plant.fertilitySensitivity,
                "Kibi must retain its shorter/lower-yield/low-fertility-sensitivity tradeoff versus Awa.");
            ctx.Assert(
                barley.plant.minGrowthTemperature < soba.plant.minGrowthTemperature
                && barley.plant.growDays > soba.plant.growDays
                && (barley.plant.sowResearchPrerequisites == null
                    || barley.plant.sowResearchPrerequisites.Count == 0),
                "Barley's cold-growth advantage must retain its longer season without an MO research gate.");
            ctx.Assert(
                wheat.plant.harvestYield > barley.plant.harvestYield
                && wheat.plant.growDays > barley.plant.growDays
                && wheat.plant.fertilityMin > barley.plant.fertilityMin
                && wheat.plant.fertilitySensitivity > barley.plant.fertilitySensitivity,
                "Wheat's high harvest output must retain longer growth and stronger fertility demands.");
        }

        [Then("stage A grain quantities are conserved through processing")]
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

            RecipeDef sobaThresh = RequireRecipe(ctx, "AMJC_ThreshBuckwheat");
            RecipeDef sobaHull = RequireRecipe(ctx, "AMJC_HullBuckwheat");
            int sobaInHull = 8 * ProductCount(ctx, sobaThresh, "AMJC_BuckwheatInHull");
            int sobaStraw = 8 * ProductCount(ctx, sobaThresh, "DankPyon_Straw");
            int sobaEdible = sobaInHull * ProductCount(ctx, sobaHull, "AMJC_Buckwheat");
            ctx.Assert(sobaInHull == 8, "Threshing one Soba harvest baseline should preserve 8 buckwheat in hull.");
            ctx.Assert(sobaStraw == 8, "Threshing one Soba harvest baseline should yield 8 straw.");
            ctx.Assert(sobaEdible == 8, "Hulling one Soba harvest baseline should preserve 8 edible buckwheat.");

            RecipeDef barleyThresh = RequireRecipe(ctx, "AMJC_ThreshBarley");
            RecipeDef barleyHull = RequireRecipe(ctx, "AMJC_HullBarley");
            int barleyInHullCount = 22 * ProductCount(ctx, barleyThresh, "AMJC_BarleyInHull");
            int barleyStraw = 22 * ProductCount(ctx, barleyThresh, "DankPyon_Straw");
            int barleyEdible = barleyInHullCount * ProductCount(ctx, barleyHull, "AMJC_Barley");
            ctx.Assert(barleyInHullCount == 22, "Threshing one Barley harvest baseline should preserve 22 barley in hull.");
            ctx.Assert(barleyStraw == 22, "Threshing one Barley harvest baseline should yield 22 straw.");
            ctx.Assert(barleyEdible == 22, "Hulling one Barley harvest baseline should preserve 22 edible barley.");

            RecipeDef wheatThresh = RequireRecipe(ctx, "AMJC_ThreshWheat");
            int wheatGrain = 28 * ProductCount(ctx, wheatThresh, "AMJC_Wheat");
            int wheatStraw = 28 * ProductCount(ctx, wheatThresh, "DankPyon_Straw");
            ctx.Assert(wheatGrain == 28, "Threshing one MO wheat harvest baseline should preserve 28 edible wheat grain.");
            ctx.Assert(wheatStraw == 28, "Threshing one MO wheat harvest baseline should yield 28 straw.");
        }

        [Then("edible AMJ grains are accepted by the vanilla simple meal ingredient filter")]
        public void AssertSimpleMealAcceptsMillet(PickleContext ctx)
        {
            ThingDef millet = RequireThingDef(ctx, "AMJC_Millet");
            RecipeDef simpleMeal = DefDatabase<RecipeDef>.GetNamedSilentFail("CookMealSimple");

            if (simpleMeal == null)
            {
                throw new InvalidOperationException("Vanilla CookMealSimple RecipeDef was not found.");
            }
            if (simpleMeal.fixedIngredientFilter == null)
            {
                throw new InvalidOperationException("CookMealSimple has no fixed ingredient filter.");
            }
            ctx.Assert(simpleMeal.fixedIngredientFilter.Allows(millet), "Edible AMJ millet should be accepted by the vanilla simple meal ingredient filter.");
            ThingDef buckwheat = RequireThingDef(ctx, "AMJC_Buckwheat");
            ctx.Assert(simpleMeal.fixedIngredientFilter.Allows(buckwheat), "Edible AMJ buckwheat should be accepted by the vanilla simple meal ingredient filter.");
            ThingDef barley = RequireThingDef(ctx, "AMJC_Barley");
            ctx.Assert(simpleMeal.fixedIngredientFilter.Allows(barley), "Edible AMJ barley should be accepted by the vanilla simple meal ingredient filter.");
            ThingDef wheat = RequireThingDef(ctx, "AMJC_Wheat");
            ctx.Assert(simpleMeal.fixedIngredientFilter.Allows(wheat), "Edible AMJ wheat grain should be accepted by the vanilla simple meal ingredient filter.");
        }

        private static void AssertLoadedCrop(
            PickleContext ctx, string defName, float growDays, float harvestYield,
            float fertilityMin, float fertilitySensitivity, float minGrowth, float maxGrowth,
            float minOptimal, float maxOptimal, int sowMinSkill, string harvestedDefName)
        {
            ThingDef crop = RequireThingDef(ctx, defName);
            if (crop.plant == null)
            {
                throw new InvalidOperationException(defName + " is not a plant.");
            }
            ctx.Assert(Math.Abs(crop.plant.growDays - growDays) < 0.001f, defName + " growDays mismatch.");
            ctx.Assert(Math.Abs(crop.plant.harvestYield - harvestYield) < 0.001f, defName + " harvestYield mismatch.");
            ctx.Assert(Math.Abs(crop.plant.fertilityMin - fertilityMin) < 0.001f, defName + " fertilityMin mismatch.");
            ctx.Assert(Math.Abs(crop.plant.fertilitySensitivity - fertilitySensitivity) < 0.001f, defName + " fertilitySensitivity mismatch.");
            ctx.Assert(Math.Abs(crop.plant.minGrowthTemperature - minGrowth) < 0.001f, defName + " minGrowthTemperature mismatch.");
            ctx.Assert(Math.Abs(crop.plant.maxGrowthTemperature - maxGrowth) < 0.001f, defName + " maxGrowthTemperature mismatch.");
            ctx.Assert(Math.Abs(crop.plant.minOptimalGrowthTemperature - minOptimal) < 0.001f, defName + " minOptimalGrowthTemperature mismatch.");
            ctx.Assert(Math.Abs(crop.plant.maxOptimalGrowthTemperature - maxOptimal) < 0.001f, defName + " maxOptimalGrowthTemperature mismatch.");
            ctx.Assert(crop.plant.sowMinSkill == sowMinSkill, defName + " sowMinSkill mismatch.");
            ctx.Assert(crop.plant.harvestedThingDef != null && crop.plant.harvestedThingDef.defName == harvestedDefName, defName + " harvestedThingDef mismatch.");
        }

        private static void AssertLoadedMilletCrop(
            PickleContext ctx, string defName, float growDays, float harvestYield,
            float fertilitySensitivity, float minGrowth, float maxGrowth, float minOptimal, float maxOptimal)
        {
            ThingDef crop = RequireThingDef(ctx, defName);
            if (crop.plant == null)
            {
                throw new InvalidOperationException(defName + " is not a plant.");
            }
            ctx.Assert(Math.Abs(crop.plant.growDays - growDays) < 0.001f, defName + " growDays mismatch.");
            ctx.Assert(Math.Abs(crop.plant.harvestYield - harvestYield) < 0.001f, defName + " harvestYield mismatch.");
            ctx.Assert(Math.Abs(crop.plant.fertilityMin - 0.5f) < 0.001f, defName + " fertilityMin mismatch.");
            ctx.Assert(Math.Abs(crop.plant.fertilitySensitivity - fertilitySensitivity) < 0.001f, defName + " fertilitySensitivity mismatch.");
            ctx.Assert(Math.Abs(crop.plant.minGrowthTemperature - minGrowth) < 0.001f, defName + " minGrowthTemperature mismatch.");
            ctx.Assert(Math.Abs(crop.plant.maxGrowthTemperature - maxGrowth) < 0.001f, defName + " maxGrowthTemperature mismatch.");
            ctx.Assert(Math.Abs(crop.plant.minOptimalGrowthTemperature - minOptimal) < 0.001f, defName + " minOptimalGrowthTemperature mismatch.");
            ctx.Assert(Math.Abs(crop.plant.maxOptimalGrowthTemperature - maxOptimal) < 0.001f, defName + " maxOptimalGrowthTemperature mismatch.");
            ctx.Assert(crop.plant.sowMinSkill == 0, defName + " sowMinSkill should be 0.");
            ctx.Assert(crop.plant.harvestedThingDef != null && crop.plant.harvestedThingDef.defName == "AMJC_RawMillet", defName + " must harvest AMJC_RawMillet.");
        }

        private static void AssertLoadedCctoExtension(PickleContext ctx, string defName, float expectedDeathTemperature)
        {
            ThingDef crop = RequireThingDef(ctx, defName);
            List<DefModExtension> extensions = crop.modExtensions == null
                ? new List<DefModExtension>()
                : crop.modExtensions.Where(x => x != null && x.GetType().FullName == "CropColdToleranceOverhaul.ColdToleranceExtension").ToList();
            ctx.Assert(extensions.Count == 1, defName + " must load exactly one CCTO ColdToleranceExtension.");
            if (extensions.Count != 1) return;
            object extension = extensions[0];
            Type extensionType = extension.GetType();
            FieldInfo deathField = extensionType.GetField("coldDeathTemperature", BindingFlags.Instance | BindingFlags.Public);
            FieldInfo dormancyField = extensionType.GetField("coldDormancy", BindingFlags.Instance | BindingFlags.Public);
            if (deathField == null)
            {
                throw new InvalidOperationException("CCTO fixture extension is missing coldDeathTemperature.");
            }
            if (dormancyField == null)
            {
                throw new InvalidOperationException("CCTO fixture extension is missing coldDormancy.");
            }
            float coldDeathTemperature = Convert.ToSingle(deathField.GetValue(extension));
            bool coldDormancy = Convert.ToBoolean(dormancyField.GetValue(extension));
            ctx.Assert(Math.Abs(coldDeathTemperature - expectedDeathTemperature) < 0.001f, defName + " CCTO cold-death temperature mismatch.");
            ctx.Assert(!coldDormancy, defName + " should use fixed cold death, not cold dormancy.");
        }

        private static void AssertThinSoilCropRoles(PickleContext ctx)
        {
            const float fertility = 0.50f;

            ThingDef soba = RequireThingDef(ctx, "AMJC_Plant_Buckwheat_Soba");
            ThingDef kibi = RequireThingDef(ctx, "AMJC_Plant_ProsoMillet_Kibi");
            ThingDef awa = RequireThingDef(ctx, "AMJC_Plant_FoxtailMillet_Awa");
            ThingDef hie = RequireThingDef(ctx, "AMJC_Plant_BarnyardMillet_Hie");
            ThingDef barley = RequireThingDef(ctx, "AMJC_Plant_Barley");
            ThingDef wheat = RequireThingDef(ctx, "DankPyon_Plant_Wheat");

            ThingDef[] sowable = { soba, kibi, awa, hie, barley };
            for (int i = 0; i < sowable.Length; i++)
            {
                ThingDef crop = sowable[i];
                ctx.Assert(
                    crop.plant != null && crop.plant.fertilityMin <= fertility + 0.0001f,
                    crop.defName + " must remain sowable at fertility 0.50.");
            }

            ctx.Assert(
                wheat.plant != null && wheat.plant.fertilityMin > fertility + 0.0001f,
                "MO wheat must remain unsowable at fertility 0.50.");

            AssertFertilityFactor(ctx, soba, fertility, 0.875f);
            AssertFertilityFactor(ctx, kibi, fertility, 0.85f);
            AssertFertilityFactor(ctx, awa, fertility, 0.80f);
            AssertFertilityFactor(ctx, hie, fertility, 0.75f);
            AssertFertilityFactor(ctx, barley, fertility, 0.70f);

            float[] factors =
            {
                FertilityFactor(soba, fertility),
                FertilityFactor(kibi, fertility),
                FertilityFactor(awa, fertility),
                FertilityFactor(hie, fertility),
                FertilityFactor(barley, fertility)
            };

            for (int i = 1; i < factors.Length; i++)
            {
                ctx.Assert(
                    factors[i - 1] > factors[i],
                    "Fertility 0.50 growth ordering must remain Soba > Kibi > Awa > Hie > Barley.");
            }
        }

        private static void AssertFertilityFactor(
            PickleContext ctx,
            ThingDef crop,
            float fertility,
            float expected)
        {
            float actual = FertilityFactor(crop, fertility);
            ctx.Assert(
                Math.Abs(actual - expected) < 0.0001f,
                crop.defName + " fertility growth factor mismatch at " + fertility + ".");
        }

        private static float FertilityFactor(ThingDef crop, float fertility)
        {
            if (crop == null || crop.plant == null)
            {
                throw new InvalidOperationException("Fertility factor requires a loaded plant ThingDef.");
            }

            float sensitivity = crop.plant.fertilitySensitivity;
            return fertility * sensitivity + (1f - sensitivity);
        }

        private static bool HasSowResearch(ThingDef crop, string researchDefName)
        {
            return crop != null
                && crop.plant != null
                && crop.plant.sowResearchPrerequisites != null
                && crop.plant.sowResearchPrerequisites.Any(
                    x => x != null && x.defName == researchDefName);
        }

        private static void AssertMoFlourRecipe(PickleContext ctx, string defName, int expectedFlourCount)
        {
            RecipeDef recipe = RequireRecipe(ctx, defName);
            ThingDef rawWheat = RequireThingDef(ctx, "DankPyon_RawWheat");
            ThingDef wheat = RequireThingDef(ctx, "AMJC_Wheat");

            if (recipe.fixedIngredientFilter == null)
            {
                throw new InvalidOperationException(defName + " has no fixed ingredient filter.");
            }

            ctx.Assert(!recipe.fixedIngredientFilter.Allows(rawWheat), defName + " must reject unthreshed wheat sheaves.");
            ctx.Assert(recipe.fixedIngredientFilter.Allows(wheat), defName + " must accept threshed AMJ wheat grain.");
            ctx.Assert(ProductCount(ctx, recipe, "DankPyon_Flour") == expectedFlourCount, defName + " flour output mismatch.");

            bool hasHay = recipe.products != null
                && recipe.products.Any(x => x.thingDef != null && x.thingDef.defName == "Hay");
            ctx.Assert(!hasHay, defName + " must not produce Hay after AMJ moves straw to threshing.");
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

            if (ingredient == null)
            {
                throw new InvalidOperationException(defName + " is missing expected input " + inputDefName + ".");
            }
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
            if (recipe.products == null)
            {
                throw new InvalidOperationException(recipe.defName + " has no products.");
            }
            ThingDefCountClass product = recipe.products.FirstOrDefault(
                x => x.thingDef != null && x.thingDef.defName == productDefName);
            if (product == null)
            {
                throw new InvalidOperationException(recipe.defName + " is missing product " + productDefName + ".");
            }
            return product.count;
        }

        private static void AssertRotDays(PickleContext ctx, ThingDef def, float expectedDays)
        {
            CompProperties_Rottable rot = def.comps == null
                ? null
                : def.comps.OfType<CompProperties_Rottable>().FirstOrDefault();

            if (rot == null)
            {
                throw new InvalidOperationException(def.defName + " is missing CompProperties_Rottable.");
            }
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
            if (def.statBases == null)
            {
                throw new InvalidOperationException(def.defName + " has no statBases.");
            }
            StatModifier modifier = def.statBases.FirstOrDefault(x => x.stat == stat);
            if (modifier == null)
            {
                throw new InvalidOperationException(def.defName + " is missing stat " + stat.defName + ".");
            }
            return modifier.value;
        }

        private static ThingDef RequireThingDef(PickleContext ctx, string defName)
        {
            ThingDef def = DefDatabase<ThingDef>.GetNamedSilentFail(defName);
            if (def == null)
            {
                throw new InvalidOperationException("Required ThingDef '" + defName + "' was not found.");
            }
            return def;
        }

        private static RecipeDef RequireRecipe(PickleContext ctx, string defName)
        {
            RecipeDef def = DefDatabase<RecipeDef>.GetNamedSilentFail(defName);
            if (def == null)
            {
                throw new InvalidOperationException("Required RecipeDef '" + defName + "' was not found.");
            }
            return def;
        }
    }
}
