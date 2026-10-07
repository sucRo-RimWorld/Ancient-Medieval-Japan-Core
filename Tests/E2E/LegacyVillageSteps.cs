// Legacy-provider regression only. Independent start tests belong to AMJ Scenarios.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;
using RimWorks.Pickle;
using RimWorld;
using Verse;

namespace AncientMedievalJapanCore.E2E
{
    [PickleSteps]
    public sealed class LegacyVillageSteps
    {
        private static bool UseMO { get { return LoadedModManager.RunningModsListForReading.Any(m =>
            string.Equals(m.PackageIdPlayerFacing, "dankpyon.medieval.overhaul", StringComparison.OrdinalIgnoreCase)
            || string.Equals(m.PackageIdPlayerFacing, "sucro.ancientmedievaljapan.core.mofixture", StringComparison.OrdinalIgnoreCase)); } }

        private static string[] StartingResearch { get { return UseMO ? new[] {
            "DankPyon_Lumber", "DankPyon_RusticFurniture", "DankPyon_BasicCooking"
        } : new string[0]; } }

        private static Dictionary<string, int> Supplies { get { return UseMO ? new Dictionary<string, int> {
            { "DankPyon_MealRations", 60 }, { "AMJC_Millet", 200 }, { "AMJC_RawMillet", 100 },
            { "MedicineHerbal", 20 }, { "WoodLog", 200 }, { "DankPyon_RawWood", 200 },
            { "DankPyon_IronIngot", 30 }, { "Cloth", 80 }, { "Silver", 150 },
            { "Bow_Short", 2 }, { "MeleeWeapon_Knife", 2 }, { "MeleeWeapon_Club", 1 }
        } : new Dictionary<string, int> {
            { "Pemmican", 1080 }, { "AMJC_Millet", 200 }, { "AMJC_RawMillet", 100 },
            { "MedicineHerbal", 20 }, { "WoodLog", 400 }, { "Steel", 30 },
            { "Cloth", 80 }, { "Silver", 150 }, { "Bow_Short", 2 },
            { "MeleeWeapon_Knife", 2 }, { "MeleeWeapon_Club", 1 }
        }; } }
        private static string KnifeStuff { get { return UseMO ? "DankPyon_IronIngot" : "Steel"; } }

        [Then("loaded legacy New Village scenario matches the start design")]
        public void AssertLoadedScenario(PickleContext ctx)
        {
            ScenarioDef definition = DefDatabase<ScenarioDef>.GetNamed("AMJC_NewVillage");
            List<ScenPart> parts = definition.scenario.AllParts.ToList();
            ScenPart playerFaction = parts.Single(p => p is ScenPart_PlayerFaction);
            FactionDef faction = (FactionDef)ReadMember(playerFaction, "factionDef");
            ctx.Assert(faction.defName == "AMJC_PlayerVillage", "New Village must select its own player faction.");
            ctx.Assert(faction.isPlayer && faction.techLevel == TechLevel.Medieval, "Village must be a Medieval player faction.");
            ctx.Assert(faction.basicMemberKind.defName == "AMJC_Villager", "Village must use the ordinary villager kind.");
            ctx.Assert(Empty(ReadMember(faction, "startingResearchTags")), "Faction must not grant research via start tags.");
            ctx.Assert(Empty(ReadMember(faction, "startingTechprintsResearchTags")), "Faction must not grant techprints via tags.");

            PawnKindDef kind = faction.basicMemberKind;
            ctx.Assert(kind.race == ThingDefOf.Human, "The standard village start must use Human.");
            ctx.Assert(Convert.ToSingle(ReadMember(kind, "techHediffsChance")) == 0f, "Villager generation must not add technology implants.");
            ctx.Assert(kind.apparelTags.Contains("Neolithic") && kind.apparelTags.Contains("DankPyon_Peasant") == UseMO, "Villager clothing must match the active profile.");

            ScenPart pawns = parts.Single(p => p is ScenPart_ConfigPage_ConfigureStartingPawns);
            ctx.Assert(Convert.ToInt32(ReadMember(pawns, "pawnCount")) == 5, "Start must select five villagers.");
            ctx.Assert(Convert.ToInt32(ReadMember(pawns, "pawnChoiceCount")) == 8, "Start must offer eight candidates.");
            ScenPart arrive = parts.Single(p => p is ScenPart_PlayerPawnsArriveMethod);
            ctx.Assert(ReadMember(arrive, "method").ToString() == "Standing", "Village must use a Standing arrival.");

            string[] projects = parts.OfType<ScenPart_StartingResearch>()
                .Select(p => ((ResearchProjectDef)ReadMember(p, "project")).defName).OrderBy(x => x).ToArray();
            ctx.Assert(projects.SequenceEqual(StartingResearch.OrderBy(x => x)), "Starting research must match the active profile.");

            List<ScenPart_StartingThing_Defined> items = parts.OfType<ScenPart_StartingThing_Defined>().ToList();
            ctx.Assert(items.Count == Supplies.Count, "Start must contain exactly the designed supply parts.");
            foreach (KeyValuePair<string, int> supply in Supplies)
            {
                ScenPart item = items.Single(p => ((ThingDef)ReadMember(p, "thingDef")).defName == supply.Key);
                ctx.Assert(Convert.ToInt32(ReadMember(item, "count")) == supply.Value, "Starting quantity differs: " + supply.Key);
                ThingDef stuff = (ThingDef)ReadMember(item, "stuff");
                string expectedStuff = supply.Key == "MeleeWeapon_Knife" ? KnifeStuff
                    : supply.Key == "MeleeWeapon_Club" ? "WoodLog" : null;
                ctx.Assert((stuff == null ? null : stuff.defName) == expectedStuff, "Starting material differs: " + supply.Key);
                if (stuff != null)
                {
                    ThingDef weapon = (ThingDef)ReadMember(item, "thingDef");
                    ctx.Assert(stuff.stuffProps != null && weapon.stuffCategories.Any(c => stuff.stuffProps.categories.Contains(c)),
                        "The selected weapon material must be supported: " + supply.Key);
                }
            }
            ctx.Assert(!parts.Any(p => p is ScenPart_StartingAnimal || p is ScenPart_ScatterThingsAnywhere
                || p is ScenPart_ScatterThingsNearPlayerStart), "Village must not add animals or scattered supplies.");
            if (!UseMO)
                ctx.Assert(Math.Abs(DefDatabase<ThingDef>.GetNamed("Pemmican").GetStatValueAbstract(StatDefOf.Nutrition) * 1080f - 54f) < 0.001f,
                    "Base starting provisions must provide 54 nutrition.");
            AssertEarlyProcessing(ctx);
        }

        [Then("legacy New Village starts with five villagers and the designed supplies")]
        public Task AssertStartedVillage(PickleContext ctx)
        {
            return RuntimeThread.Run(delegate { AssertStartedVillageOnMainThread(ctx); });
        }

        private void AssertStartedVillageOnMainThread(PickleContext ctx)
        {
            AssertLoadedScenario(ctx);
            Map map = Find.CurrentMap;
            ctx.Assert(map != null && map.IsPlayerHome, "Quickstart must generate a player home map.");
            ctx.Assert(Faction.OfPlayer.def.defName == "AMJC_PlayerVillage", "Actual player faction must be the village faction.");
            List<Pawn> pawns = map.mapPawns.FreeColonistsSpawned.ToList();
            ctx.Assert(pawns.Count == 5, "The production Scenario must spawn exactly five villagers.");
            ctx.Assert(pawns.All(p => p.kindDef.defName == "AMJC_Villager" && p.Faction == Faction.OfPlayer),
                "All starting villagers must be generated using the village kind and faction.");

            string[] finished = DefDatabase<ResearchProjectDef>.AllDefsListForReading
                .Where(p => p.IsFinished).Select(p => p.defName).OrderBy(x => x).ToArray();
            ctx.Assert(finished.SequenceEqual(StartingResearch.OrderBy(x => x)),
                "The actual research manager must finish only the designed profile start projects.");

            List<Thing> available = map.listerThings.AllThings.ToList();
            foreach (Pawn pawn in pawns)
                if (pawn.inventory != null) available.AddRange(pawn.inventory.innerContainer);
            foreach (KeyValuePair<string, int> supply in Supplies)
            {
                // Map generation may independently scatter items. Loaded-part checks above are
                // exact; here verify all promised supplies actually made it into the live start.
                int count = available.Where(t => t.def.defName == supply.Key).Sum(t => t.stackCount);
                ctx.Assert(count >= supply.Value, "Actual start is missing supplies: " + supply.Key + " (" + count + ")");
            }
            ctx.Assert(available.Count(t => t.def.defName == "MeleeWeapon_Knife"
                && t.Stuff != null && t.Stuff.defName == KnifeStuff) >= 2, "Both knives must spawn in the designed material.");
            ctx.Assert(available.Any(t => t.def.defName == "MeleeWeapon_Club" && t.Stuff == ThingDefOf.WoodLog),
                "The club must actually spawn in wood.");

            ThingDef spot = DefDatabase<ThingDef>.GetNamed("AMJC_GrainProcessingSpot");
            ctx.Assert(spot.costStuffCount == 10 && spot.stuffCategories.Contains(ThingDefOf.WoodLog.stuffProps.categories[0]),
                "Starting wood must support the ten-wood simple grain processing spot.");
            foreach (string crop in new[] { "AMJC_Plant_FoxtailMillet_Awa", "AMJC_Plant_BarnyardMillet_Hie",
                "AMJC_Plant_ProsoMillet_Kibi", "AMJC_Plant_Buckwheat_Soba" })
            {
                ThingDef plant = DefDatabase<ThingDef>.GetNamed(crop);
                ctx.Assert(plant.plant.sowResearchPrerequisites == null || plant.plant.sowResearchPrerequisites.Count == 0,
                    "Initial field crop must not be blocked by unfinished research: " + crop);
            }
        }

        private static void AssertEarlyProcessing(PickleContext ctx)
        {
            ThingDef spot = DefDatabase<ThingDef>.GetNamed("AMJC_GrainProcessingSpot");
            ctx.Assert(spot.researchPrerequisites == null || spot.researchPrerequisites.Count == 0,
                "The simple processing spot must be available without research.");
            foreach (string name in new[] { "AMJC_ThreshMillet", "AMJC_HullMillet" })
            {
                RecipeDef recipe = DefDatabase<RecipeDef>.GetNamed(name);
                ctx.Assert(recipe.recipeUsers != null && recipe.recipeUsers.Contains(spot),
                    "Simple spot must offer the initial millet processing recipe: " + name);
                ctx.Assert(recipe.researchPrerequisite == null
                    && (recipe.researchPrerequisites == null || recipe.researchPrerequisites.Count == 0),
                    "Initial millet processing must not require research: " + name);
            }
        }

        private static bool Empty(object value)
        {
            return value == null || !((IEnumerable)value).Cast<object>().Any();
        }

        // Scenario parts keep some XML fields private. Missing fields fail with a useful
        // name, instead of accidentally treating a reflection miss as a zero/default.
        private static object ReadMember(object value, string name)
        {
            for (Type type = value.GetType(); type != null; type = type.BaseType)
            {
                FieldInfo field = type.GetField(name, BindingFlags.Public | BindingFlags.NonPublic
                    | BindingFlags.Instance | BindingFlags.DeclaredOnly);
                if (field != null) return field.GetValue(value);
                PropertyInfo property = type.GetProperty(name, BindingFlags.Public | BindingFlags.NonPublic
                    | BindingFlags.Instance | BindingFlags.DeclaredOnly);
                if (property != null) return property.GetValue(value, null);
            }
            throw new InvalidOperationException("Required XML member " + value.GetType().FullName + "." + name + " was not found.");
        }
    }
}

