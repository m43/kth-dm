import random
import statistics

from models.Triest import Triest

if __name__ == '__main__':
    random.seed(720)

    datasets = [
        # name, path, nodes, edges, triangles
        # ("Youtube", "../datasets/com-youtube.ungraph.txt", 1134890, 2987624, 3056386),
        ("Amazon", "../datasets/com-amazon.ungraph.txt", 334863, 925872, 667129),
        # ("DBLP", "../datasets/com-dblp.ungraph.txt", 317080, 1049866, 2224385),
        # ("Facebook", "../datasets/facebook_combined.txt", 4039, 88234, 1612010)
    ]
    # ms = [10000, 50000, 100000]
    # loops = 10
    ms = [100000]
    loops = 2

    print(f"loops={loops}")

    results = {}
    for dataset_name, dataset_path, _, _, _ in datasets:
        results[dataset_name] = {}
        for m in ms:
            results[dataset_name][m] = {}
            trieste = Triest(fname=dataset_path, m=m, log=True)
            for alg_name, alg in [("Improved", trieste.improved), ("Base", trieste.base)]:
                triangles_array = []
                best_time = -1
                for i in range(loops):
                    result = alg()
                    print(result)
                    triangles_array.append(result["global_triangles"])
                    if best_time == -1 or best_time < result["time"]:
                        best_time = result["time"]
                mean, stddev = statistics.mean(triangles_array), statistics.stdev(triangles_array)
                results[dataset_name][m][alg_name] = mean, stddev, best_time

    print(f'Dataset name,Nodes,Edges,Triangles (ground truth)')
    for dataset_name, _, nodes, edges, triangles in datasets:
        print(f"{dataset_name},{nodes},{edges},{triangles}")

    print(f'Dataset name,Improved,m,Triangles(stddev),Best time')
    for dataset_name, _, _, _, _ in datasets:
        for yes_no, alg_name in ("N", "Base"), ("Y", "Improved"):
            for m in ms:
                print(f"{dataset_name},{yes_no},{m},"
                      f"{results[dataset_name][m][alg_name][0]:.2f}"
                      f"({results[dataset_name][m][alg_name][1]:.2f}),"
                      f"{results[dataset_name][m][alg_name][2]:.4f}")

"""
Friendster results:
Improved: {'m': 10000, 'epsilon': 1, 'global_counter': 814269856.1821496, 'global_triangles': 814269856.1821496}
Base: {'m': 10000, 'epsilon': 5892939304365283.0, 'global_counter': 0, 'global_triangles': 0.0}
Improved: {'m': 100000, 'epsilon': 1, 'global_counter': 4444248139.442466, 'global_triangles': 4444248139.442466}
Base: {'m': 100000, 'epsilon': 5891348279702.881, 'global_counter': 0, 'global_triangles': 0.0}
Improved: {'t': 1806067135, 'm': 1000000, 'epsilon': 1, 'global_counter': 4092690331.181979, 'global_triangles': 4092690331.181979, 'samples_length': 1000000}
Base: {'t': 1806067135, 'm': 1000000, 'epsilon': 5891189213.988619, 'global_counter': 0, 'global_triangles': 0.0, 'samples_length': 1000000}
"""
