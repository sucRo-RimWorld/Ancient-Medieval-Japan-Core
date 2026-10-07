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
                new StageASteps().AssertSimpleMealAcceptsMillet(ctx);
                ctx.Require(DefDatabase<ScenarioDef>.GetNamedSilentFail("AMJC_NewVillage") != null,
                    "New Village must remain present during migration.");
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
