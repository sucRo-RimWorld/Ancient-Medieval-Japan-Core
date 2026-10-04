using Verse;

namespace CropColdToleranceOverhaul
{
    // Developer-only XML API shape used by AMJC integration tests.
    // Runtime CCTO behavior remains tested in the CCTO repository.
    public sealed class ColdToleranceExtension : DefModExtension
    {
        public float coldDeathTemperature = float.NaN;
        public bool coldDormancy;
    }
}
