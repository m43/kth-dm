from timeit import default_timer as timer

import os

from models.CompareSets import CompareSets
from models.CompareSignatures import CompareSignatures
from models.Lsh import Lsh
from models.MinHashing import MinHashing
from models.Shingling import Shingling

RESEARCH_DATASET_PATH = os.path.abspath("../../datasets/literature-text")
K = 6
N = 50
BAND_WIDTH = 5
# LSH_THRESHOLDS = [0.1, 0.3, 0.7, 0.05, 0.01]
threshold = 0.3
SEED = 36
HASH = hash


def load_papers():
    names = []
    hash_brownies = []
    universe = set()
    for filename in os.listdir(RESEARCH_DATASET_PATH):
        file = open(os.path.join(RESEARCH_DATASET_PATH, filename), "r", encoding='UTF-8')
        names.append(filename)
        hash_brownies.append(Shingling(file, K, HASH, universe).return_hashed_shingles())

    return universe, names, hash_brownies


def candidate_pairs(names, hash_brownies, threshold):
    candidate_names = []
    for c1 in range(len(hash_brownies) - 1):
        for c2 in range(c1 + 1, len(hash_brownies)):
            sim = CompareSets(hash_brownies[c1], hash_brownies[c2]).ret_jaccard_sim()
            if sim > threshold:
                candidate_names.append((names[c1], names[c2], sim))
    return candidate_names


def minhash_candidates(universe, names, hash_brownies, threshold):
    universe_list = list(universe)
    signatures = MinHashing(N, hash_brownies, universe_list, SEED).return_signatures()

    candidate_names = []
    for c1 in range(len(signatures) - 1):
        for c2 in range(c1 + 1, len(signatures)):
            sim = CompareSignatures(signatures[c1], signatures[c2]).ret_sim()
            if sim > threshold:
                candidate_names.append((names[c1], names[c2], sim))
    return candidate_names


def lsh_candidates(universe, names, hash_brownies, threshold):
    universe_list = list(universe)
    signatures = MinHashing(N, hash_brownies, universe_list, SEED).return_signatures()

    candidates = Lsh(signatures, BAND_WIDTH, threshold, HASH).ret_candidates()
    candidate_names = [(names[candidate[0]], names[candidate[1]], candidate[2]) for candidate in candidates]
    return candidate_names


if __name__ == '__main__':
    print(f"K:{K} N:{N} Band_width:{BAND_WIDTH} Seed:{SEED} Hash:{HASH}\n")

    start = timer()
    universe, names, _ = load_papers()
    print(f"Got {len(universe)} brownies in total for {len(names)} documents.")
    print(f"%%% Load papers: {timer()-start}s %%%\n")

    start = timer()
    _, names, hash_brownies = load_papers()
    candidate_names = candidate_pairs(names, hash_brownies, threshold)
    print(f"Bare candidate_pairs for threshold {threshold}:\n{candidate_names}")
    print(f"%%% Load papers + candidate_pairs: {timer()-start}s %%%\n")

    start = timer()
    universe, names, hash_brownies = load_papers()
    candidate_names = minhash_candidates(universe, names, hash_brownies, threshold)
    print(f"minhash_candidates for threshold {threshold}:\n{candidate_names}")
    print(f"%%% Load papers + minhash_candidates: {timer()-start}s %%%\n")


    start = timer()
    universe, names, hash_brownies = load_papers()
    candidate_names = lsh_candidates(universe, names, hash_brownies, threshold)
    print(f"lsh_candidates for threshold {threshold}:\n{candidate_names}")
    print(f"%%% Load papers + lsh_candidates: {timer()-start}s %%%\n")
