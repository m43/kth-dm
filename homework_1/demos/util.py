from timeit import default_timer as timer

from tqdm import tqdm

from models.CompareSets import CompareSets
from models.CompareSignatures import CompareSignatures
from models.Lsh import Lsh
from models.MinHashing import MinHashing


def candidate_pairs(names, hash_brownies, threshold):
    candidate_names = []
    for c1 in tqdm(range(len(hash_brownies) - 1)):
        for c2 in range(c1 + 1, len(hash_brownies)):
            sim = CompareSets(hash_brownies[c1], hash_brownies[c2]).ret_jaccard_sim()
            if sim > threshold:
                candidate_names.append((names[c1], names[c2], sim))
    return candidate_names


def minhash_candidates(universe, names, hash_brownies, threshold, n, seed):
    universe_list = list(universe)
    signatures = MinHashing(n, hash_brownies, universe_list, seed).return_signatures()

    candidate_names = []
    for c1 in tqdm(range(len(signatures) - 1)):
        for c2 in range(c1 + 1, len(signatures)):
            sim = CompareSignatures(signatures[c1], signatures[c2]).ret_sim()
            if sim > threshold:
                candidate_names.append((names[c1], names[c2], sim))
    return candidate_names


def lsh_candidates(universe, names, hash_brownies, threshold, n, seed, band_width, lsh_band_hash):
    universe_list = list(universe)
    signatures = MinHashing(n, hash_brownies, universe_list, seed).return_signatures()

    candidates = Lsh.ret_candidates(signatures, band_width, threshold, lsh_band_hash)
    candidate_names = [(names[candidate[0]], names[candidate[1]], candidate[2]) for candidate in candidates]
    return candidate_names


def demo(dataset_loader, k, n, band_width, threshold, seed, minhash_hash, lsh_band_hash,
         test_bare=True, test_minhash=True, test_lsh=True):
    print(
        f"K:{k} N:{n} Band_width:{band_width} Seed:{seed} MinHash_hash:{minhash_hash} LSH_band_hash:{lsh_band_hash}\n")

    start = timer()
    universe, names, hash_brownies = dataset_loader()
    print(f"Got {len(universe)} brownies in total for {len(names)} documents.")
    print(f"%%% load dataset: {timer() - start}s %%%\n")

    if test_bare:
        start = timer()
        candidate_names = candidate_pairs(names, hash_brownies, threshold)
        print(f"Bare candidate_pairs for threshold {threshold}:\n{candidate_names}")
        print(f"%%% candidate_pairs: {timer() - start}s %%%\n")

    if test_minhash:
        start = timer()
        candidate_names = minhash_candidates(universe, names, hash_brownies, threshold, n, seed)
        print(f"minhash_candidates for threshold {threshold}:\n{candidate_names}")
        print(f"%%% minhash_candidates: {timer() - start}s %%%\n")

    if test_lsh:
        start = timer()
        candidate_names = lsh_candidates(universe, names, hash_brownies, threshold, n, seed, band_width, lsh_band_hash)
        print(f"lsh_candidates for threshold {threshold}:\n{candidate_names}")
        print(f"%%% lsh_candidates: {timer() - start}s %%%\n")
