import os
import sys

from demos.util import demo
from models.Shingling import Shingling

# RESEARCH_DATASET_PATH = os.path.abspath("../datasets/literature-text")
K = 6
N = 50
BAND_WIDTH = 3
THRESHOLD = 0.3
SEED = 36
MINHASH_HASH = hash
LSH_BAND_HASH = hash


def load_papers(research_dataset_path):
    names = []
    hash_brownies = []
    universe = set()
    for filename in os.listdir(research_dataset_path):
        file = open(os.path.join(research_dataset_path, filename), "r", encoding='UTF-8')
        names.append(filename)
        hash_brownies.append(Shingling(file, K, MINHASH_HASH, universe).return_hashed_shingles())

    return universe, names, hash_brownies


if __name__ == '__main__':
    if (len(sys.argv)) != 2:
        raise Exception(f"Invalid number of arguments. Got {len(sys.argv)} arguments, expected 2 (irrelevant script "
                        f"name and dataset path).")
    research_dataset_path = sys.argv[1]
    demo(lambda: load_papers(research_dataset_path), K, N, BAND_WIDTH, THRESHOLD, SEED, MINHASH_HASH, LSH_BAND_HASH)
