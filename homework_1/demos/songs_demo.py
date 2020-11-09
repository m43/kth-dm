import csv
import io
import numpy as np
import os
import sys
from tqdm import tqdm

from models.CompareSignatures import CompareSignatures
from models.Shingling import Shingling

# SONGS_DATASET_PATH = "../datasets/scraped_songs.csv"
# SONGS_DATASET_PATH = "../datasets/scraped_songs_2.csv"
PICKLE_PATH = "../../datasets/dump"
K = 5
N = 99
BAND_WIDTH = 20
LSH_THRESHOLDS = [0.1, 0.3, 0.7, 0.05, 0.01]
SEED = 72
HASH = hash


def load_songs(songs_dataset_path):
    names = []
    hash_brownies = []
    universe = set()
    with open(songs_dataset_path, newline='') as songs:
        reader = csv.reader(songs)
        rows = iter(reader)
        next(rows)  # skip header
        for row in rows:
            names.append(row[0] + " -- " + row[1] + " -- url:" + row[4])
            hash_brownies.append(Shingling(io.StringIO(row[2]), K, HASH, universe).return_hashed_shingles())

    return universe, names, hash_brownies


if __name__ == '__main__':
    if (len(sys.argv)) != 2:
        raise Exception(f"Invalid number of arguments. Got {len(sys.argv)} arguments, expected 2.")
    songs_dataset_path = sys.argv[1]

    print(f"loading songs from {os.path.abspath(songs_dataset_path)}...")
    universe, names, hash_brownies = load_songs(songs_dataset_path)
    print("songs loaded")

    print(f"got {len(universe)} brownies in universe")
    print("now signatures")
    universe_list = list(universe)
    signatures = []
    np.random.seed(SEED)
    permutations = [np.random.permutation(np.arange(len(universe_list))) for _ in range(N)]
    for brownie in tqdm(hash_brownies):
        signature = []
        for perm in permutations:
            for i in range(len(perm)):
                if universe_list[perm[i]] in brownie:
                    signature.append(i)
                    break
        signatures.append(signature)

    print("now lsh")
    number_of_bands = len(signatures[0]) // BAND_WIDTH
    lsh_matrix = []
    for signature in signatures:
        lsh_signature = []
        for band_id in range(number_of_bands):
            band = tuple(signature[band_id * BAND_WIDTH: band_id * BAND_WIDTH + BAND_WIDTH])
            lsh_signature.append(HASH(band))
        lsh_matrix.append(lsh_signature)
    threshold_to_pairs = {th: list() for th in LSH_THRESHOLDS}
    for i in range(len(lsh_matrix)):
        for j in range(i + 1, len(lsh_matrix)):
            comparison = CompareSignatures(lsh_matrix[i], lsh_matrix[j])
            for threshold in LSH_THRESHOLDS:
                if comparison.similarity > threshold:
                    threshold_to_pairs[threshold].append((names[i], names[j], comparison.similarity))
    print(f"Threshold to pairs map: {threshold_to_pairs}\n")
