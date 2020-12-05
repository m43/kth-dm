#!/usr/bin/env python3
import os
import sys

# output_folder = "output"
if (len(sys.argv)) != 2:
        raise Exception(f"Invalid number of arguments. Got {len(sys.argv)} arguments, "
                        f"expected 2: 1. script name (irrelevant) "
                        f"2. output folder location")
output_folder = sys.argv[1]

results = []
for filename in os.listdir(output_folder):
    if not filename.endswith(".txt"):
        continue
    with open(os.path.join(output_folder, filename), "r") as f:
        last_line = f.readlines()[-1:][0]
        results.append((filename[:filename.find("_")], last_line.split()))

for graph, result in results:
    print(f"{graph},{','.join(result)}")
