using System;
using System.Linq;
using System.Threading.Tasks;
using RimWorks.Pickle;
using RimWorld;
using Verse;

namespace AncientMedievalJapanCore.E2E
{
    // Migration smoke contracts. The legacy fixture suite remains independent.
    [PickleSteps]
    public sealed class GrainsProfileSteps
    {
        private static bool Active(string id)
        {
            return LoadedModManager.RunningModsListForReading.Any(
                mod => string.Equals(mod.PackageIdPlayerFacing, id, StringComparison.OrdinalIgnoreCase));
        }

        private static void AssertProviders(PickleContext ctx, bool mo, bool ccto)
        {
            ctx.Assert(Active("dankpyon.medieval.overhaul") == mo, "Real MO presence must match the requested profile.");
            ctx.Assert(Active("sucro.cropcoldtoleranceoverhaul") == ccto, "Real CCTO presence must match the requested profile.");
            ctx.Assert(!Active("sucro.ancientmedievaljapan.core.mofixture"), "MO API fixture must be absent.");
            ctx.Assert(!Active("sucro.ancientmedievaljapan.core.cctofixture"), "CCTO API fixture must be absent.");
            ctx.Assert(!Active("sucro.ancientmedievaljapan.core"), "Production Core must not load alongside its test copy.");
        }

        [Then("the real vanilla Grains providers are active")]
        public void Vanilla(PickleContext ctx) { AssertProviders(ctx, false, false); }
        [Then("the real vanilla CCTO Grains providers are active")]
        public void VanillaCcto(PickleContext ctx) { AssertProviders(ctx, false, true); }
        [Then("the real MO Grains providers are active")]
        public void Mo(PickleContext ctx) { AssertProviders(ctx, true, false); }
        [Then("the real MO CCTO Grains providers are active")]
        public void MoCcto(PickleContext ctx) { AssertProviders(ctx, true, true); }

        [Then("the Grains primary grain loop resolves")]
        public Task PrimaryLoop(PickleContext ctx)
        {
            return RuntimeThread.Run(delegate
            {
                foreach (string name in new[] { "AMJC_Plant_FoxtailMillet_Awa", "AMJC_Plant_BarnyardMillet_Hie",
                    "AMJC_Plant_ProsoMillet_Kibi", "AMJC_Plant_Buckwheat_Soba", "AMJC_Plant_Barley" })
                {
                    ThingDef crop = DefDatabase<ThingDef>.GetNamed(name);
                    ctx.Require(crop.plant != null && crop.plant.harvestedThingDef != null, name + " must resolve a harvest.");
                    ctx.Assert(crop.plant.sowResearchPrerequisites == null || crop.plant.sowResearchPrerequisites.All(r => r != null),
                        name + " must have no unresolved research.");
                }
                foreach (RecipeDef recipe in DefDatabase<RecipeDef>.AllDefsListForReading.Where(r => r.defName.StartsWith("AMJC_")))
                {
                    ctx.Require(recipe.products != null && recipe.products.Count > 0, recipe.defName + " must resolve products.");
                    ctx.Assert(recipe.products.All(p => p.thingDef != null), recipe.defName + " has an unresolved output.");
                    ctx.Require(recipe.ingredients != null && recipe.ingredients.Count > 0, recipe.defName + " must resolve ingredients.");
                    ctx.Assert(recipe.ingredients.All(i => i.filter.AllowedThingDefs.Any()), recipe.defName + " has an empty ingredient filter.");
                }
                if (!Active("dankpyon.medieval.overhaul"))
                {
                    ThingDef barley = DefDatabase<ThingDef>.GetNamed("AMJC_Plant_Barley");
                    ctx.Assert(barley.plant.sowResearchPrerequisites == null || barley.plant.sowResearchPrerequisites.Count == 0,
                        "Base barley must be research-free.");
                    ThingDef table = DefDatabase<ThingDef>.GetNamed("AMJC_GrainProcessingTable");
                    ctx.Assert(table.researchPrerequisites == null || table.researchPrerequisites.Count == 0,
                        "Base processing table must be research-free.");
                    ctx.Assert(table.costList.Count == 1 && table.costList[0].thingDef.defName == "Steel" && table.costList[0].count == 30,
                        "Base processing table must use 30 steel.");
                    foreach (RecipeDef recipe in DefDatabase<RecipeDef>.AllDefsListForReading.Where(r => r.defName.StartsWith("AMJC_Thresh")))
                        ctx.Assert(recipe.products.Count == 1 && recipe.products.All(p => p.thingDef.defName.StartsWith("AMJC_")),
                            "Base threshing must produce only its AMJ grain: " + recipe.defName);
                }
                ThingDef rice = DefDatabase<ThingDef>.GetNamed("Plant_Rice");
                ThingDef rawRice = DefDatabase<ThingDef>.GetNamed("RawRice");
                ThingDef riceSheaf = DefDatabase<ThingDef>.GetNamed("AMJC_RiceSheaf");
                ThingDef riceHull = DefDatabase<ThingDef>.GetNamed("AMJC_RiceInHull");
                ctx.Require(rice.plant != null && rice.plant.harvestedThingDef == riceSheaf,
                    "Upland rice must harvest AMJC_RiceSheaf; RawRice remains the existing edible item.");
                ctx.Assert(riceSheaf.ingestible.preferability == FoodPreferability.NeverForNutrition
                    && riceHull.ingestible.preferability == FoodPreferability.NeverForNutrition,
                    "Rice intermediates must be inedible.");
                foreach (string part in new[] { "Thresh", "Hull" })
                foreach (bool bulk in new[] { false, true })
                {
                    string name = "AMJC_" + part + "Rice" + (bulk ? "Bulk" : "");
                    RecipeDef rec = DefDatabase<RecipeDef>.GetNamed(name);
                    int n = bulk ? 10 : 1;
                    ThingDef input = part == "Thresh" ? riceSheaf : riceHull;
                    ThingDef output = part == "Thresh" ? riceHull : rawRice;
                    ctx.Assert(rec.ingredients.Count == 1 && rec.ingredients[0].filter.Allows(input)
                        && rec.ingredients[0].GetBaseCount() == n, "Rice processing input differs: " + name);
                    ctx.Assert(rec.products.Any(p => p.thingDef == output && p.count == n)
                        && rec.products.Count == ((Active("dankpyon.medieval.overhaul") && part == "Thresh") ? 2 : 1),
                        "Rice processing output or optional straw differs: " + name);
                }
                ctx.Assert(rice.plant.growDays == 5f && rice.plant.harvestYield == 11f
                    && rice.plant.fertilityMin == 0.7f && rice.plant.fertilitySensitivity == 0.8f,
                    "Rice growth, yield or fertility differs from design.");
                ctx.Assert(rice.plant.minGrowthTemperature == 10f && rice.plant.maxGrowthTemperature == 42f
                    && rice.plant.minOptimalGrowthTemperature == 18f && rice.plant.maxOptimalGrowthTemperature == 32f,
                    "Rice temperatures differ from design.");
                ctx.Assert(rice.plant.sowTags.Count == 1 && rice.plant.sowTags[0] == "Ground",
                    "Rice must sow on ground and not in hydroponics.");
                RecipeDef meal = DefDatabase<RecipeDef>.GetNamed("CookMealSimple");
                ctx.Assert(meal.fixedIngredientFilter != null && meal.fixedIngredientFilter.Allows(rawRice),
                    "RawRice must still be a simple-meal ingredient.");
                var ext = rice.modExtensions == null
                    ? new System.Collections.Generic.List<DefModExtension>()
                    : rice.modExtensions.Where(e => e != null &&
                        e.GetType().FullName == "CropColdToleranceOverhaul.ColdToleranceExtension").ToList();
                bool ccto = Active("sucro.cropcoldtoleranceoverhaul");
                ctx.Assert(ext.Count == (ccto ? 1 : 0), "Rice CCTO extension count differs.");
                if (ccto)
                {
                    var field = ext[0].GetType().GetField("coldDeathTemperature");
                    ctx.Require(field != null && Convert.ToSingle(field.GetValue(ext[0])) == -1f,
                        "Rice must retain the CCTO -1 C cold-death threshold.");
                }
                new StageASteps().AssertSimpleMealAcceptsMillet(ctx);
            });
        }

        [Then("the Grains wheat flour and minimum food chains resolve")]
        public Task FlourChain(PickleContext ctx)
        {
            return RuntimeThread.Run(delegate
            {
                bool mo = Active("dankpyon.medieval.overhaul");
                foreach (string fallback in new[] { "AMJC_Plant_Wheat", "AMJC_RawWheat", "AMJC_WheatFlour", "AMJC_ManualMillstone" })
                    ctx.Assert((DefDatabase<ThingDef>.GetNamedSilentFail(fallback) != null) == !mo,
                        "Fallback presence must match MO absence: " + fallback);
                ctx.Assert((DefDatabase<RecipeDef>.GetNamedSilentFail("AMJC_MillWheat") != null) == !mo,
                    "Only Base must expose the fallback wheat milling recipe.");
                ThingDef wheat = DefDatabase<ThingDef>.GetNamed(mo ? "DankPyon_Plant_Wheat" : "AMJC_Plant_Wheat");
                string sheaf = mo ? "DankPyon_RawWheat" : "AMJC_RawWheat";
                ctx.Assert(wheat.plant.harvestedThingDef.defName == sheaf && wheat.plant.growDays == 12f
                    && wheat.plant.harvestYield == 28f && wheat.plant.fertilityMin == 0.7f
                    && wheat.plant.fertilitySensitivity == 0.9f, "Wheat provider must retain the six-grain balance.");
                if (!mo)
                {
                    ctx.Assert(wheat.plant.sowResearchPrerequisites == null || wheat.plant.sowResearchPrerequisites.Count == 0,
                        "Base wheat must be research-free.");
                    bool ccto = Active("sucro.cropcoldtoleranceoverhaul");
                    var extensions = wheat.modExtensions == null ? new System.Collections.Generic.List<DefModExtension>()
                        : wheat.modExtensions.Where(e => e != null && e.GetType().FullName == "CropColdToleranceOverhaul.ColdToleranceExtension").ToList();
                    ctx.Assert(extensions.Count == (ccto ? 1 : 0), "Fallback CCTO extension must match the provider.");
                    if (ccto)
                        ctx.Assert(Convert.ToSingle(extensions[0].GetType().GetField("coldDeathTemperature").GetValue(extensions[0])) == -6f,
                            "Fallback wheat must retain the -6 C cold-death value.");
                }
                ThingDef inputSheaf = DefDatabase<ThingDef>.GetNamed(sheaf);
                ctx.Assert(inputSheaf.ingestible.preferability == FoodPreferability.NeverForNutrition,
                    "Wheat sheaves must not bypass threshing.");
                foreach (string name in new[] { "AMJC_ThreshWheat", "AMJC_ThreshWheatBulk" })
                {
                    RecipeDef rec = DefDatabase<RecipeDef>.GetNamed(name);
                    int count = name.EndsWith("Bulk") ? 10 : 1;
                    ctx.Assert(rec.ingredients.Count == 1 && rec.ingredients[0].filter.Allows(inputSheaf)
                        && rec.ingredients[0].GetBaseCount() == count, "Wheat thresh input differs: " + name);
                    ctx.Assert(rec.products.Count == (mo ? 2 : 1)
                        && rec.products.Single(p => p.thingDef.defName == "AMJC_Wheat").count == count,
                        "Wheat thresh convergence differs: " + name);
                }
                if (mo)
                {
                    // All three upstream MO grinding recipes include Hay, but
                    // AMJ's conditional XML patch must remove that byproduct.
                    foreach (string sourceName in new[] { "DankPyon_CraftFlour_Manual",
                        "DankPyon_CraftFlour", "DankPyon_CraftFlourBulk" })
                    {
                        RecipeDef loaded = DefDatabase<RecipeDef>.GetNamed(sourceName);
                        ctx.Assert(loaded.products != null && loaded.products.Count == 1
                            && loaded.products[0].thingDef.defName == "DankPyon_Flour",
                            "Grains must remove upstream MO milling Hay: " + sourceName);
                    }
                }
                ThingDef mill = DefDatabase<ThingDef>.GetNamed(mo ? "DankPyon_Millstone" : "AMJC_ManualMillstone");
                ctx.Assert(mill.researchPrerequisites == null || mill.researchPrerequisites.Count == 0,
                    "The standard Grains mill must be research-free.");
                string[] grains = { "AMJC_Buckwheat", "AMJC_Millet", "AMJC_Wheat" };
                string[] powders = { "AMJC_BuckwheatFlour", "AMJC_MilletFlour", mo ? "DankPyon_Flour" : "AMJC_WheatFlour" };
                string[] recipes = { "AMJC_MillBuckwheat", "AMJC_MillMillet", mo ? "DankPyon_CraftFlour" : "AMJC_MillWheat" };
                for (int index = 0; index < grains.Length; index++)
                {
                    RecipeDef rec = DefDatabase<RecipeDef>.GetNamed(recipes[index]);
                    ThingDef grain = DefDatabase<ThingDef>.GetNamed(grains[index]);
                    ThingDef powder = DefDatabase<ThingDef>.GetNamed(powders[index]);
                    ctx.Assert(rec.ingredients.Any(i => i.filter.Allows(grain)) && rec.recipeUsers.Contains(mill),
                        "Grain must connect to the standard mill: " + grains[index]);
                    ctx.Assert(rec.products.Count == 1 && rec.products[0].thingDef == powder,
                        "Milling must yield only the designated powder: " + recipes[index]);
                    ctx.Assert(Math.Abs(rec.ingredients[0].GetBaseCount() * grain.GetStatValueAbstract(StatDefOf.Nutrition)
                        - rec.products[0].count * powder.GetStatValueAbstract(StatDefOf.Nutrition)) < 0.001f,
                        "Milling must conserve nutrition: " + recipes[index]);
                    ctx.Assert(powder.ingestible.preferability == FoodPreferability.NeverForNutrition,
                        "Powders must be used by cooking rather than eaten directly.");
                }
                string[] foods = { "Sobagaki", "MilletDumplings", "Houtou" };
                for (int index = 0; index < foods.Length; index++)
                {
                    RecipeDef rec = DefDatabase<RecipeDef>.GetNamed("AMJC_Cook" + foods[index]);
                    ThingDef food = DefDatabase<ThingDef>.GetNamed("AMJC_" + foods[index]);
                    ThingDef powder = DefDatabase<ThingDef>.GetNamed(powders[index]);
                    ctx.Assert(rec.ingredients.Count == 1 && rec.ingredients[0].filter.Allows(powder)
                        && rec.ingredients[0].GetBaseCount() == 0.5f, "Powder meal must require 0.5 nutrition.");
                    ctx.Assert(rec.products.Count == 1 && rec.products[0].thingDef == food && rec.products[0].count == 1,
                        "Cooking must yield one designed flour meal.");
                    ctx.Assert(rec.recipeUsers.Any(u => u.defName == "Campfire") && rec.researchPrerequisite == null
                        && (rec.researchPrerequisites == null || rec.researchPrerequisites.Count == 0),
                        "Minimum powder food must be research-free and available at a campfire.");
                    ctx.Assert(Math.Abs(food.GetStatValueAbstract(StatDefOf.Nutrition) - 0.9f) < 0.001f
                        && food.ingestible.tasteThought.defName == "AMJC_AteFlourFood", "Food nutrition/thought differs.");
                    ctx.Assert(food.comps.OfType<CompProperties_Rottable>().Single().daysToRotStart == 2.5f,
                        "Minimum powder foods must not become long-storage bread.");
                }
                ctx.Assert(DefDatabase<ThoughtDef>.GetNamed("AMJC_AteFlourFood").stages[0].baseMoodEffect == 2f,
                    "The extra flour processing reward must remain +2 mood.");
            });
        }

        [Then("Grains cold tolerance extensions are present")]
        public void ColdPresent(PickleContext ctx) { new StageASteps().AssertLoadedCropCctoCompatibility(ctx); }

        [Then("Grains cold tolerance extensions are absent")]
        public void ColdAbsent(PickleContext ctx)
        {
            foreach (ThingDef crop in DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.defName.StartsWith("AMJC_") && d.plant != null))
                ctx.Assert(crop.modExtensions == null || !crop.modExtensions.Any(e => e != null &&
                    e.GetType().FullName == "CropColdToleranceOverhaul.ColdToleranceExtension"),
                    crop.defName + " must not load a CCTO extension without CCTO.");
        }
    }
}
