using RimWorks.Quickstarts;
using RimWorld;
using Verse;

namespace AncientMedievalJapanCore.E2E
{
    public sealed class AmjStageAQuickstart : AbstractQuickstart
    {
        public override TaggedString description
        {
            get { return "Deterministic small colony used only by AMJ Core Stage A Pickle tests."; }
        }

        public override int mapSize
        {
            get { return 50; }
        }

        public override string seed
        {
            get { return "AMJ-Stage-A-E2E"; }
        }
    }

    // Select the retained legacy Scenario; do not replace its pawn/items/research parts.
    public sealed class AmjLegacyVillageQuickstart : AbstractQuickstart
    {
        public override TaggedString description
        {
            get { return "Starts the production AMJC New Village scenario for Pickle verification."; }
        }

        public override ScenarioDef scenario
        {
            get { return DefDatabase<ScenarioDef>.GetNamed("AMJC_NewVillage"); }
        }

        public override int mapSize
        {
            get { return 75; }
        }

        public override string seed
        {
            get { return "AMJ-New-Village-E2E"; }
        }
    }
}
