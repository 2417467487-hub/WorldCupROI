public class SponsorRiskRules {
    public static String recommend(double roiLift, double negativeRoiProbability) {
        if (roiLift > 0.18 && negativeRoiProbability < 0.25) {
            return "Scale premium activation";
        }
        if (roiLift > 0.05 && negativeRoiProbability < 0.45) {
            return "Proceed with monitored investment";
        }
        if (negativeRoiProbability > 0.60) {
            return "Shift budget to flexible activation";
        }
        return "Maintain baseline exposure";
    }
}
