package se.kth.jabeja;

import se.kth.jabeja.config.Config;
import se.kth.jabeja.rand.RandNoGenerator;

import java.util.HashMap;

public class JabejaExponentialSA2 extends Jabeja {

    public JabejaExponentialSA2(HashMap<Integer, Node> graph, Config config) {
        super(graph, config);
        saBottomResetAfter = 150;
    }

    @Override protected void saCoolDown() {
        double minT = 1e-7;

        if (T > minT) {
            T = T * config.getTemperatureAlpha();
        }

        if (T <= minT && saBottomCounter++ > saBottomResetAfter) {
            if ((config.getRounds() - round) > 200) {
                saBottomCounter = 0;
                T = config.getTemperature();
            }
        }
    }

    @Override protected boolean shouldAcceptNewSolution(double newBenefit, double oldBenefit) {
        double acceptanceProbability = 1 / (1 + Math.exp(-(newBenefit - oldBenefit) / T));
        return acceptanceProbability > RandNoGenerator.nextDouble();
    }
}
