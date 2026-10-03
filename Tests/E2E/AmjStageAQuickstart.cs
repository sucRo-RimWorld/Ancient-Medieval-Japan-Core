using RimWorks.Quickstarts;
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
}
