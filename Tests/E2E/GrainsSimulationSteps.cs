using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.ExceptionServices;
using System.Threading.Tasks;
using RimWorks.Pickle;
using RimWorld;
using Verse;
using Verse.AI;

namespace AncientMedievalJapanCore.E2E
{
    [PickleSteps]
    public sealed class GrainsSimulationSteps
    {
        internal static string[] Crops(bool mo)
        {
            return new[] { "AMJC_Plant_FoxtailMillet_Awa", "AMJC_Plant_BarnyardMillet_Hie",
                "AMJC_Plant_ProsoMillet_Kibi", "AMJC_Plant_Buckwheat_Soba", "AMJC_Plant_Barley",
                mo ? "DankPyon_Plant_Wheat" : "AMJC_Plant_Wheat", "Plant_Rice" };
        }

        private static bool HasMO()
        {
            return LoadedModManager.RunningModsListForReading.Any(m => string.Equals(
                m.PackageIdPlayerFacing, "dankpyon.medieval.overhaul", StringComparison.OrdinalIgnoreCase));
        }

        [Then("seven Grains retain environmental harvest niches")]
        public Task Environment(PickleContext ctx)
        {
            return RuntimeThread.Run(delegate
            {
                ThingDef[] crops = Crops(HasMO()).Select(n => DefDatabase<ThingDef>.GetNamed(n)).ToArray();
                int[] wins = new int[crops.Length];
                int viable = 0;
                foreach (float fertility in new[] { 0.5f, 1f, 1.4f })
                foreach (float temperature in new[] { 10f, 20f, 30f })
                foreach (float season in new[] { 5f, 10f, 20f })
                {
                    // Effective growing days: full light, no resting, weather,
                    // sow/harvest delays or frost death. Use the game's utility,
                    // including any installed provider patches, rather than our formula.
                    float[] yields = crops.Select(c => fertility < c.plant.fertilityMin ? 0f :
                        (float)Math.Floor(season * PlantUtility.GrowthRateFactorFor_Fertility(c, fertility)
                            * PlantUtility.GrowthRateFactorFor_Temperature(c, temperature)
                            / c.plant.growDays + 0.000001f) * c.plant.harvestYield).ToArray();
                    float best = yields.Max();
                    if (best <= 0f) continue;
                    viable++;
                    for (int i = 0; i < crops.Length; i++)
                        if (Math.Abs(yields[i] - best) < 0.0001f) wins[i]++;
                }
                ctx.Require(viable > 0, "Environment matrix must contain mature harvests.");
                for (int i = 0; i < crops.Length; i++)
                {
                    ctx.Assert(wins[i] > 0, crops[i].defName + " lost its representative harvest niche.");
                    ctx.Assert(wins[i] * 3 < viable * 2, crops[i].defName + " wins >=2/3 of viable cells.");
                }
            });
        }

        [Then("Grains harvest and flour food Bills complete through real jobs")]
        public async Task ProductionJobs(PickleContext ctx)
        {
            ProductionScope scope = null;
            ExceptionDispatchInfo failure = null;
            try
            {
                await RuntimeThread.Run(delegate { scope = new ProductionScope(ctx); });
                await RuntimeThread.Run(scope.AssertUplandSowability);
                foreach (string crop in Crops(scope.MO)) await scope.Harvest(crop);
                // All inputs below are outputs of the preceding real jobs.
                await scope.Bill("AMJC_ThreshMilletBulk", scope.Processing, "AMJC_RawMillet", 10);
                await scope.Bill("AMJC_HullMilletBulk", scope.Processing, "AMJC_MilletInHull", 10);
                await scope.Bill("AMJC_MillMillet", scope.Mill, "AMJC_Millet", 10);
                await scope.Bill("AMJC_CookMilletDumplings", scope.Campfire, "AMJC_MilletFlour", 10);
                await scope.Bill("AMJC_ThreshBuckwheatBulk", scope.Processing, "AMJC_RawBuckwheat", 10);
                await scope.Bill("AMJC_HullBuckwheatBulk", scope.Processing, "AMJC_BuckwheatInHull", 10);
                await scope.Bill("AMJC_MillBuckwheat", scope.Mill, "AMJC_Buckwheat", 10);
                await scope.Bill("AMJC_CookSobagaki", scope.Campfire, "AMJC_BuckwheatFlour", 10);
                await scope.Bill("AMJC_ThreshWheatBulk", scope.Processing,
                    scope.MO ? "DankPyon_RawWheat" : "AMJC_RawWheat", 10);
                await scope.Bill(scope.MO ? "DankPyon_CraftFlourBulk" : "AMJC_MillWheat", scope.Mill, "AMJC_Wheat", 10);
                await scope.Bill("AMJC_CookHoutou", scope.Campfire, scope.MO ? "DankPyon_Flour" : "AMJC_WheatFlour", 10);
            }
            catch (Exception error) { failure = ExceptionDispatchInfo.Capture(error); }
            // The repository builds with the Framework C# 5 compiler, which
            // does not permit await inside catch/finally. Preserve the original
            // failure while awaiting main-thread cleanup outside those blocks.
            try { if (scope != null) await RuntimeThread.Run(scope.Dispose); }
            catch (Exception cleanup)
            {
                if (failure != null) throw new AggregateException(failure.SourceException, cleanup);
                throw;
            }
            if (failure != null) failure.Throw();
        }

        // This scope is only valid on a fresh AmjStageAQuickstart test map.
        // Setup creates mature plants, a worker, benches and fuel. It never
        // manufactures harvested ingredients or recipe products.
        private sealed class ProductionScope
        {
            private readonly PickleContext ctx;
            private readonly Map map;
            private readonly TimeSpeed speed;
            private readonly Stopwatch deadline = Stopwatch.StartNew();
            private readonly List<Thing> created = new List<Thing>();
            private readonly Dictionary<Pawn, IntVec3> parked = new Dictionary<Pawn, IntVec3>();
            private readonly Dictionary<IntVec3, TerrainDef> terrain = new Dictionary<IntVec3, TerrainDef>();
            private Pawn worker;
            private IntVec3 center;
            public bool MO;
            public Building_WorkTable Processing, Mill, Campfire;

            public ProductionScope(PickleContext context)
            {
                ctx = context;
                map = Find.CurrentMap;
                ctx.Require(map != null && map.Size.x == 50 && map.Size.z == 50,
                    "Production jobs require the isolated 50-cell Stage A Quickstart map.");
                speed = Find.TickManager.CurTimeSpeed;
                MO = HasMO();
                try
                {
                    Find.TickManager.CurTimeSpeed = TimeSpeed.Paused;
                    ctx.Require(Find.TickManager.CurTimeSpeed == TimeSpeed.Paused, "Controlled tick advancement requires pause.");
                    bool found = false;
                    foreach (IntVec3 cell in map.AllCells.OrderBy(c => c.DistanceToSquared(map.Center)))
                    {
                        CellRect area = CellRect.CenteredOn(cell, 7);
                        if (!area.Cells.All(c => c.InBounds(map) && c.Standable(map) && c.GetEdifice(map) == null)) continue;
                        center = cell; found = true; break;
                    }
                    ctx.Require(found, "Quickstart map needs a clear 15x15 test area.");
                    foreach (Pawn pawn in map.mapPawns.AllPawnsSpawned.ToList())
                    {
                        parked.Add(pawn, pawn.Position);
                        pawn.DeSpawn();
                    }
                    foreach (IntVec3 cell in CellRect.CenteredOn(center, 7).Cells)
                    {
                        terrain.Add(cell, map.terrainGrid.TerrainAt(cell));
                        foreach (Thing thing in cell.GetThingList(map).ToList()) thing.Destroy(DestroyMode.Vanish);
                        map.terrainGrid.SetTerrain(cell, TerrainDefOf.Soil);
                    }
                    for (int attempt = 0; attempt < 30; attempt++)
                    {
                        Pawn candidate = PawnGenerator.GeneratePawn(PawnKindDefOf.Colonist, Faction.OfPlayer);
                        if (!candidate.Downed && candidate.skills != null && !candidate.WorkTypeIsDisabled(WorkTypeDefOf.Growing)
                            && !candidate.WorkTypeIsDisabled(WorkTypeDefOf.Crafting)
                            && !candidate.WorkTypeIsDisabled(DefDatabase<WorkTypeDef>.GetNamed("Cooking")))
                        { worker = candidate; break; }
                        candidate.Destroy(DestroyMode.Vanish);
                    }
                    ctx.Require(worker != null, "Cannot create a capable production worker.");
                    created.Add(worker);
                    GenSpawn.Spawn(worker, center, map);
                    worker.workSettings.EnableAndInitializeIfNotAlreadyInitialized();
                    foreach (SkillDef skill in new[] { SkillDefOf.Plants, SkillDefOf.Crafting, SkillDefOf.Cooking })
                        worker.skills.GetSkill(skill).Level = 20;
                    ctx.Require(worker.GetStatValue(StatDefOf.PlantHarvestYield) >= 1f, "Harvest failure must be excluded by worker skill.");
                    Processing = Bench("AMJC_GrainProcessingTable", center + new IntVec3(-3,0,0));
                    Mill = Bench(MO ? "DankPyon_Millstone" : "AMJC_ManualMillstone", center + new IntVec3(3,0,0));
                    Campfire = Bench("Campfire", center + new IntVec3(0,0,-4));
                    CompRefuelable fuel = Campfire.TryGetComp<CompRefuelable>();
                    ctx.Require(fuel != null, "Campfire needs a fuel component.");
                    fuel.Refuel(fuel.Props.fuelCapacity);
                }
                catch { Dispose(); throw; }
            }

            private Building_WorkTable Bench(string name, IntVec3 cell)
            {
                ThingDef def = DefDatabase<ThingDef>.GetNamed(name);
                Thing thing = ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
                thing.SetFaction(Faction.OfPlayer);
                created.Add(thing);
                GenSpawn.Spawn(thing, cell, map, Rot4.North);
                Building_WorkTable bench = thing as Building_WorkTable;
                ctx.Require(bench != null, name + " must be a real worktable.");
                return bench;
            }

            private int Count(string name)
            {
                int total = map.listerThings.AllThings.Where(t => t.def.defName == name).Sum(t => t.stackCount);
                Thing carried = worker.carryTracker.CarriedThing;
                return total + (carried != null && carried.def.defName == name ? carried.stackCount : 0);
            }

            private void Start(Job job, string label)
            {
                ctx.Require(job != null, "No real job was offered for " + label);
                if (worker.needs.food != null) worker.needs.food.CurLevelPercentage = 1f;
                if (worker.needs.rest != null) worker.needs.rest.CurLevelPercentage = 1f;
                job.playerForced = true;
                worker.jobs.StartJob(job, JobCondition.InterruptForced);
                ctx.Require(worker.CurJob == job, "Job failed to start: " + label);
            }

            private async Task Complete(Job job, Func<bool> done, string label)
            {
                bool complete = false;
                for (int ticks = 0; ticks < 20000 && !complete; ticks += 64)
                {
                    await RuntimeThread.Run(delegate
                    {
                        ctx.Require(deadline.Elapsed.TotalSeconds < 150, "Production suite exceeded 150 seconds: " + label);
                        for (int tick = 0; tick < 64; tick++)
                        {
                            if (done()) { complete = true; break; }
                            ctx.Require(worker.CurJob == job, "Job ended without its expected outputs: " + label);
                            Find.TickManager.DoSingleTick();
                        }
                        if (done()) complete = true;
                    });
                    // Yield between bounded tick batches so driver/rendering can update.
                    await Task.Delay(1);
                }
                await RuntimeThread.Run(delegate
                {
                    ctx.Require(complete, "Job exceeded 20000 game ticks: " + label);
                    worker.jobs.EndCurrentJob(JobCondition.InterruptForced, false);
                    if (worker.carryTracker.CarriedThing != null)
                    {
                        Thing dropped;
                        ctx.Require(worker.carryTracker.TryDropCarriedThing(worker.Position, ThingPlaceMode.Near, out dropped),
                            "Cannot place carried job product: " + label);
                    }
                });
            }

            public void AssertUplandSowability()
            {
                // Real engine eligibility on soil; calendar-dependent native Sow remains pending.
                ThingDef rice = DefDatabase<ThingDef>.GetNamed("Plant_Rice");
                IntVec3 cell = center + new IntVec3(0, 0, 2);
                Zone_Growing zone = new Zone_Growing(map.zoneManager);
                map.zoneManager.RegisterZone(zone);
                try
                {
                    zone.AddCell(cell);
                    zone.SetPlantDefToGrow(rice);
                    ctx.Require(zone.CellCount == 1 && zone.GetPlantDefToGrow() == rice,
                        "Rice must be selectable on a standard growing zone.");
                    ctx.Assert(PlantUtility.CanSowOnGrower(rice, zone),
                        "Native sow eligibility must accept upland rice.");
                    ctx.Assert(rice.CanNowPlantAt(cell, map),
                        "Upland rice must be plantable in normal soil.");
                }
                finally { zone.Delete(false); }
            }

            public async Task Harvest(string name, bool extra = false)
            {
                Plant plant = null; Job job = null;
                string raw = null; int before = 0, straw = 0, hay = 0, minimum = 0, maximum = 0;
                await RuntimeThread.Run(delegate
                {
                    ThingDef crop = DefDatabase<ThingDef>.GetNamed(name);
                    raw = crop.plant.harvestedThingDef.defName;
                    if (name == "Plant_Rice") ctx.Require(raw == "RawRice", "Upland rice must harvest Vanilla RawRice.");
                    before = Count(raw); straw = Count("DankPyon_Straw"); hay = Count("Hay");
                    // Two Soba plants ensure >=10 actual sheaves for the x10 Bills.
                    plant = (Plant)ThingMaker.MakeThing(crop);
                    plant.Growth = 1f;
                    created.Add(plant);
                    GenSpawn.Spawn(plant, center + new IntVec3(0,0,4), map);
                    float baseYield = crop.plant.harvestYield * (crop.plant.harvestYieldAffectedByDifficulty
                        ? Find.Storyteller.difficulty.cropYieldFactor : 1f);
                    float skill = worker.GetStatValue(StatDefOf.PlantHarvestYield);
                    // Native harvest rounds plant yield, then rounds excess skill.
                    minimum = (int)Math.Floor(Math.Floor(baseYield) * skill);
                    maximum = (int)Math.Ceiling(Math.Ceiling(baseYield) * skill);
                    map.designationManager.AddDesignation(new Designation(plant, DesignationDefOf.HarvestPlant));
                    job = new WorkGiver_PlantsCut().JobOnThing(worker, plant, true);
                    ctx.Require(job != null && job.def == JobDefOf.HarvestDesignated, "Must use designated harvest job: " + name);
                    Start(job, name);
                });
                await Complete(job, () => plant.Destroyed && Count(raw) > before, name);
                await RuntimeThread.Run(delegate
                {
                    ctx.Assert(Count("DankPyon_Straw") == straw && Count("Hay") == hay,
                        "Harvest must not bypass threshing with a straw/hay drop: " + name);
                    int harvested = Count(raw) - before;
                    ctx.Assert(harvested >= minimum && harvested <= maximum,
                        name + " harvest quantity disagrees with difficulty/skill-adjusted yield.");
                });
                if (name == "AMJC_Plant_Buckwheat_Soba" && !extra)
                    await Harvest(name, true);
            }

            public async Task Bill(string recipeName, Building_WorkTable bench, string ingredient, int consumed)
            {
                Job job = null; Bill_Production bill = null; RecipeDef recipe = null;
                int before = 0, straw = 0, hay = 0;
                Dictionary<string,int> products = null;
                await RuntimeThread.Run(delegate
                {
                    recipe = DefDatabase<RecipeDef>.GetNamed(recipeName);
                    ctx.Require(bench.def.AllRecipes.Contains(recipe), recipeName + " must be offered by " + bench.def.defName);
                    before = Count(ingredient); ctx.Require(before >= consumed, "Harvest chain lacks " + ingredient);
                    straw = Count("DankPyon_Straw"); hay = Count("Hay");
                    products = recipe.products.ToDictionary(p => p.thingDef.defName, p => Count(p.thingDef.defName));
                    bill = (Bill_Production)recipe.MakeNewBill();
                    bill.repeatMode = BillRepeatModeDefOf.RepeatCount; bill.repeatCount = 1;
                    bill.SetStoreMode(BillStoreModeDefOf.DropOnFloor);
                    bill.ingredientSearchRadius = 10f;
                    bench.BillStack.AddBill(bill);
                    foreach (WorkGiverDef def in DefDatabase<WorkGiverDef>.AllDefsListForReading)
                    {
                        if (def.giverClass == null || !typeof(WorkGiver_DoBill).IsAssignableFrom(def.giverClass)) continue;
                        WorkGiver_DoBill giver = def.Worker as WorkGiver_DoBill;
                        if (giver == null || !giver.ThingIsUsableBillGiver(bench)) continue;
                        Job offered = giver.JobOnThing(worker, bench, true);
                        if (offered != null && offered.def == JobDefOf.DoBill && offered.bill == bill)
                        { job = offered; break; }
                    }
                    Start(job, recipeName);
                });
                await Complete(job, () => bill.repeatCount == 0 && recipe.products.All(p =>
                    Count(p.thingDef.defName) == products[p.thingDef.defName] + p.count), recipeName);
                await RuntimeThread.Run(delegate
                {
                    ctx.Assert(Count(ingredient) == before - consumed, recipeName + " consumed the wrong ingredient quantity.");
                    ctx.Assert(bill.repeatCount == 0, recipeName + " must finish exactly one Bill iteration.");
                    foreach (ThingDefCountClass product in recipe.products)
                        ctx.Assert(Count(product.thingDef.defName) == products[product.thingDef.defName] + product.count,
                            recipeName + " produced the wrong quantity: " + product.thingDef.defName);
                    if (!recipe.products.Any(p => p.thingDef.defName == "DankPyon_Straw"))
                        ctx.Assert(Count("DankPyon_Straw") == straw, recipeName + " must not create straw.");
                    ctx.Assert(Count("Hay") == hay, recipeName + " must not create hay.");
                    bench.BillStack.Delete(bill);
                });
            }

            public void Dispose()
            {
                if (worker != null && worker.Spawned) worker.jobs.EndCurrentJob(JobCondition.InterruptForced, false);
                foreach (Thing thing in created.AsEnumerable().Reverse())
                    if (!thing.Destroyed) thing.Destroy(DestroyMode.Vanish);
                foreach (KeyValuePair<IntVec3,TerrainDef> cell in terrain) map.terrainGrid.SetTerrain(cell.Key, cell.Value);
                foreach (KeyValuePair<Pawn,IntVec3> pawn in parked)
                    if (!pawn.Key.Destroyed && !pawn.Key.Spawned) GenSpawn.Spawn(pawn.Key, pawn.Value, map);
                Find.TickManager.CurTimeSpeed = speed;
            }
        }
    }
}
