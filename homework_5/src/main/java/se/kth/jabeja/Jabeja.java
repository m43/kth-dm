package se.kth.jabeja;

import org.apache.log4j.Logger;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.NodeSelectionPolicy;
import se.kth.jabeja.io.FileIO;
import se.kth.jabeja.rand.RandNoGenerator;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Jabeja {
    final static Logger logger = Logger.getLogger(Jabeja.class);
    final Config config;
    private final HashMap<Integer/*id*/, Node/*neighbors*/> entireGraph;
    private final List<Integer> nodeIds;
    int numberOfSwaps;
    int round;
    double T;
    private boolean resultFileCreated = false;
    int saBottomCounter = 0;
    int saBottomResetAfter;
    Integer bestCut;

    //-------------------------------------------------------------------
    public Jabeja(HashMap<Integer, Node> graph, Config config) {
        this.entireGraph = graph;
        this.nodeIds = new ArrayList(entireGraph.keySet());
        this.round = 0;
        this.numberOfSwaps = 0;
        this.config = config;
        this.T = config.getTemperature();
        saBottomResetAfter = 50;
    }

    //-------------------------------------------------------------------
    public void startJabeja() throws IOException {
        for (round = 0; round < config.getRounds(); round++) {
            for (int id : entireGraph.keySet()) {
                sampleAndSwap(id);
            }

            //one cycle for all nodes have completed.
            //reduce the temperature
            saCoolDown();
            report();
        }
    }

    /**
     * Simulated analealing cooling function
     */
    void saCoolDown() {
        if (T > 1) {
            T -= config.getDelta();
            if (T < 1) {
                T = 1;
            }
        }

        if (T == 1 && saBottomCounter++ > saBottomResetAfter) {
            if ((config.getRounds() - round) > (50 + T / config.getDelta())) {
                saBottomCounter = 0;
                T = config.getTemperature();
            }
        }
    }

    /**
     * Sample and swap algorith at node p
     *
     * @param nodeId
     */
    private void sampleAndSwap(int nodeId) {
        Node partner = null;
        Node nodep = entireGraph.get(nodeId);

        if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID || config.getNodeSelectionPolicy() == NodeSelectionPolicy.LOCAL) {
            partner = findPartner(nodeId, getNeighbors(nodep));
        }

        if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID
                || config.getNodeSelectionPolicy() == NodeSelectionPolicy.RANDOM) {
            if (partner == null) {
                partner = findPartner(nodeId, getSample(nodeId));
            }
        }

        if (partner != null) {
            int pColor = nodep.getColor();
            nodep.setColor(partner.getColor());
            partner.setColor(pColor);
            numberOfSwaps++;
        }
    }

    /**
     * Method goes through all given nodes looking for the best partner. A partner is a node with which the
     * given nodeId would change color. All given nodes are partner candidates. The best partner is returned,
     * if there is one that satisfies conditions for a partner.
     *
     * @param nodeId
     * @param nodes  the candidate partners
     * @return the best partner among given nodes, if any exist
     */
    public Node findPartner(int nodeId, Integer[] nodes) {

        Node nodep = entireGraph.get(nodeId);

        Node bestPartner = null;
        double highestBenefit = 0;

        for (int nodeqIdx : nodes) {
            Node nodeq = entireGraph.get(nodeqIdx);
            int degree_pp = getDegree(nodep, nodep.getColor());
            int degree_qq = getDegree(nodeq, nodeq.getColor());
            double oldBenefit = benefitOfSolution(degree_pp, degree_qq);

            int degree_pq = getDegree(nodep, nodeq.getColor());
            int degree_qp = getDegree(nodeq, nodep.getColor());
            double newBenefit = benefitOfSolution(degree_pq, degree_qp);

            if ((newBenefit > highestBenefit) && shouldAcceptNewSolution(newBenefit, oldBenefit)) {
                bestPartner = nodeq;
                highestBenefit = newBenefit;
            }
        }

        return bestPartner;
    }

    double benefitOfSolution(int degree1, int degree2) {
        return Math.pow(degree1, config.getAlpha()) + Math.pow(degree2, config.getAlpha());
    }

    boolean shouldAcceptNewSolution(double newBenefit, double oldBenefit) {
        return newBenefit * T > oldBenefit;
    }

    /**
     * The the degreee on the node based on color
     *
     * @param node
     * @param colorId
     * @return how many neighbors of the node have color == colorId
     */
    private int getDegree(Node node, int colorId) {
        int degree = 0;
        for (int neighborId : node.getNeighbours()) {
            Node neighbor = entireGraph.get(neighborId);
            if (neighbor.getColor() == colorId) {
                degree++;
            }
        }
        return degree;
    }

    /**
     * Returns a uniformly random sample of the graph
     *
     * @param currentNodeId
     * @return Returns a uniformly random sample of the graph
     */
    private Integer[] getSample(int currentNodeId) {
        int count = config.getUniformRandomSampleSize();
        int rndId;
        int size = entireGraph.size();
        ArrayList<Integer> rndIds = new ArrayList<Integer>();

        while (true) {
            rndId = nodeIds.get(RandNoGenerator.nextInt(size));
            if (rndId != currentNodeId && !rndIds.contains(rndId)) {
                rndIds.add(rndId);
                count--;
            }

            if (count == 0)
                break;
        }

        Integer[] ids = new Integer[rndIds.size()];
        return rndIds.toArray(ids);
    }

    /**
     * Get random neighbors. The number of random neighbors is controlled using
     * -closeByNeighbors command line argument which can be obtained from the config
     * using {@link Config#getRandomNeighborSampleSize()}
     *
     * @param node
     * @return
     */
    private Integer[] getNeighbors(Node node) {
        ArrayList<Integer> list = node.getNeighbours();
        int count = config.getRandomNeighborSampleSize();
        int rndId;
        int index;
        int size = list.size();
        ArrayList<Integer> rndIds = new ArrayList<Integer>();

        if (size <= count)
            rndIds.addAll(list);
        else {
            while (true) {
                index = RandNoGenerator.nextInt(size);
                rndId = list.get(index);
                if (!rndIds.contains(rndId)) {
                    rndIds.add(rndId);
                    count--;
                }

                if (count == 0)
                    break;
            }
        }

        Integer[] arr = new Integer[rndIds.size()];
        return rndIds.toArray(arr);
    }

    /**
     * Generate a report which is stored in a file in the output dir.
     *
     * @throws IOException
     */
    private void report() throws IOException {
        int grayLinks = 0;
        int migrations = 0; // number of nodes that have changed the initial color
        int size = entireGraph.size();

        for (int i : entireGraph.keySet()) {
            Node node = entireGraph.get(i);
            int nodeColor = node.getColor();
            ArrayList<Integer> nodeNeighbours = node.getNeighbours();

            if (nodeColor != node.getInitColor()) {
                migrations++;
            }

            if (nodeNeighbours != null) {
                for (int n : nodeNeighbours) {
                    Node p = entireGraph.get(n);
                    int pColor = p.getColor();

                    if (nodeColor != pColor)
                        grayLinks++;
                }
            }
        }

        int edgeCut = grayLinks / 2;
        if (bestCut == null || edgeCut < bestCut) {
            bestCut = edgeCut;
        }
        if (round == config.getRounds() - 1) {
            edgeCut = bestCut; // in order to save the best at last line
        }

        logger.info(
                "round: " + (round + 1) + ", edge cut:" + edgeCut + ", swaps: " + numberOfSwaps + ", migrations: " + migrations + ", temp"
                        + T);

        saveToFile(edgeCut, migrations);
    }

    private void saveToFile(int edgeCuts, int migrations) throws IOException {
        String delimiter = "\t\t";
        String outputFilePath;

        //output file name
        File inputFile = new File(config.getGraphFilePath());
        outputFilePath =
                config.getOutputDir() + File.separator + inputFile.getName() + "_" + "NS" + "_" + config.getNodeSelectionPolicy() + "_"
                        + "GICP" + "_" + config.getGraphInitialColorPolicy() + "_" + "T" + "_" + config.getTemperature() + "_" + "D" + "_"
                        + config.getDelta() + "_" + "RNSS" + "_" + config.getRandomNeighborSampleSize() + "_" + "URSS" + "_" + config
                        .getUniformRandomSampleSize() + "_" + "A" + "_" + config.getAlpha() + "_V_" + config.getVersion() + "_" + "R" + "_"
                        + config.getRounds() + ".txt";

        if (!resultFileCreated) {
            File outputDir = new File(config.getOutputDir());
            if (!outputDir.exists()) {
                if (!outputDir.mkdir()) {
                    throw new IOException("Unable to create the output directory");
                }
            }
            // create folder and result file with header
            String header = "# Migration is number of nodes that have changed color.";
            header += "\n\nRound" + delimiter + "Edge-Cut" + delimiter + "Swaps" + delimiter + "Migrations" + delimiter + "Skipped" + "\n";
            FileIO.write(header, outputFilePath);
            resultFileCreated = true;
        }

        FileIO.append((round + 1) + delimiter + (edgeCuts) + delimiter + numberOfSwaps + delimiter + migrations + "\n", outputFilePath);
    }
}
