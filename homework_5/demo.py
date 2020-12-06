#!/usr/bin/env python3
import os
import subprocess
import tqdm
import itertools
from pathlib import Path
import multiprocessing

def ensure_dir(dirname):
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)

def run(config):
    print(config, "Started")
    outputDir, version, rounds, graph, alpha, temp = config
    os.system(f'./run.sh -version {version} -rounds {rounds} -graph graphs/{graph} -temp {temp} -alpha {alpha} -outputDir "{outputDir}" >> /dev/null') # >> /dev/null
    print(config, "Done")

if __name__ == '__main__':
    compile = False
    outputDir = "output10"
    threads=6 # or processes, not sure
    xdg_open = False
    generate_pngs = True
    graphs = [
        "3elt.graph",
        "4elt.graph",
        "add20.graph",
        "data.graph",
        # "twitter.graph",
        ### "facebook.graph",
        # "google.graph",
        # "scale-1000.graph",
        # "synth-0.25-1000.graph", "synth-0.75-1000.graph", "synth-0.95-10000.graph", "synth-0.95-1000.graph",
        # "synth-0.95-25000.graph", "synth-0.95-250.graph", "synth-0.95-5000.graph",
        "vibrobox.graph",
        # "ws-10000.graph"
        # "ws-1000.graph", "ws-25000.graph", "ws-250.graph", "ws-5000.graph",
    ]

    configs = []

    # V1 config
    version = ["v1"]
    rounds = [10000]
    a_values = [2,2.5,3]
    t_values = [1, 2, 3]
    # a_values = [2]
    # t_values = [2]
    configs.extend(list(itertools.product([outputDir], version, rounds, graphs, a_values, t_values)))


    # V2 config
    version = ["v2"]
    rounds = [10000]
    a_values = [2,3]
    t_values = [2, 1, 0.9, 0.8]
    # t_values = [0.8]
    configs.extend(list(itertools.product([outputDir], version, rounds, graphs, a_values, t_values)))

    # V3 config
    version = ["v3"]
    rounds = [10000]
    a_values = [2,3]
    t_values = [4,1,0.5, 0.25]
    configs.extend(list(itertools.product([outputDir], version, rounds, graphs, a_values, t_values)))


    print(os.getcwd())
    ensure_dir(outputDir)
    print(configs)

    if compile:
        os.system("./compile.sh")

    # with multiprocessing.Pool(threads) as pool:
    #     list(tqdm.tqdm(pool.imap(run, configs), total=len(configs)))
    # os.system(f"python extract_results.py {outputDir} > {outputDir}/results.csv")

    results = {}
    with open(f"{outputDir}/results.csv", "r") as f:
        lines = [line.strip().split(",") for line in f.readlines()]
        name_to_idx = {col:lines[0].index(col) for col in lines[0]}
        for line in lines[1:]:
            graph = line[name_to_idx["graph"]]
            rounds = line[name_to_idx["rounds"]]
            alpha = line[name_to_idx["alpha"]]
            temp = line[name_to_idx["temp"]]
            edge_cut = line[name_to_idx["edge_cut"]]
            version = line[name_to_idx["version"]]

            run_name = f'{graph}-rounds={rounds}-version={version}'
            if run_name not in results:
                results[run_name] = {}
            if alpha not in results[run_name]:
                results[run_name][alpha] = {}

            results[run_name][alpha][temp] = edge_cut

    with open(f"{outputDir}/results_grid.csv", "w") as f:
        for run_name in results:
            run_alphas = sorted(results[run_name].keys(), key=lambda x: float(x))
            run_temps = set([temp for a in run_alphas for temp in results[run_name][a].keys()])
            temps = sorted(run_temps, key=lambda x: float(x))

            f.write(run_name + "\n")
            f.write("alpha/temp," + ",".join(temps) + "\n")
            for a in run_alphas:
                current_temp = [results[run_name][a][t] if t in results[run_name][a] else "" for t in temps]
                f.write(f'{a},{",".join(current_temp)}\n')
            f.write("\n")

    with open(f"{outputDir}/results_grid.csv", "r") as f:
        for line in f.readlines():
            print(line.strip())

    if generate_pngs:
        for filename in os.listdir(outputDir):
            if not filename.endswith(".txt"):
                continue
            os.system(f"./plot.sh {os.path.join(outputDir, filename)}")

    if xdg_open:
        os.system(f"xdg-open {outputDir}/results_grid.csv")
