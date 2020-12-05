package se.kth.jabeja;

import se.kth.jabeja.config.Config;
import se.kth.jabeja.rand.RandNoGenerator;

import java.util.HashMap;

public class JabejaExponentialSA extends Jabeja {

    public JabejaExponentialSA(HashMap<Integer, Node> graph, Config config) {
        super(graph, config);
    }

    @Override protected void saCoolDown() {
        double minT = 1e-5;

        if (T > minT) {
            T = T * config.getTemperatureAlpha();
        }

        if (T <= minT && saBottomCounter++ > 40) {
            if ((config.getRounds() - round) > 200) {
                saBottomCounter = 0;
                T = config.getTemperature();
            }
        }
    }

    @Override protected boolean shouldAcceptNewSolution(double newBenefit, double oldBenefit) {
        if (newBenefit > oldBenefit) {
            return true;
        }

        double acceptanceProbability = Math.exp(0.3 * (newBenefit - oldBenefit) / T);
        if (newBenefit == oldBenefit) {
            return false;
        }
        return acceptanceProbability > RandNoGenerator.nextDouble();

    }
}
