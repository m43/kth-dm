#!/usr/bin/env python3
import os
import sys

# output_folder = "output"
if (len(sys.argv)) != 2:
        raise Exception(f"Invalid number of arguments. Got {len(sys.argv)} arguments, "
                        f"expected 2: 1. script name (irrelevant) "
                        f"2. output folder location")
output_folder = sys.argv[1]

header = "graph,rounds,edge_cut,swaps,migrations,temp,alpha,jabeja_version"
results = []
for filename in os.listdir(output_folder):
    t = filename[filename.find("_T_")+3:filename.find("_D_")]
    a = filename[filename.find("_A_")+3:filename.find("_V_")]
    v = filename[filename.find("_V_")+3:filename.find("_R_")]
    if not filename.endswith(".txt"):
        continue
    with open(os.path.join(output_folder, filename), "r") as f:
        last_line_parts = f.readlines()[-1:][0].split()
        result = []
        result += last_line_parts[:4]
        result.append(t)
        result.append(a)
        result.append(v)
        results.append((filename[:filename.find("_")], result))

print(header)
for graph, result in results:
    print(f"{graph},{','.join(result)}")
