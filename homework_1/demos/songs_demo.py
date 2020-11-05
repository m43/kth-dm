import csv
import io

from models.Lsh import Lsh
from models.MinHashing import MinHashing
from models.Shingling import Shingling

SONGS_DATASET_PATH = "../../datasets/scraped_songs.csv"
# SONGS_DATASET_PATH = "../../datasets/scraped_songs_2.csv"
PICKLE_PATH = "../../datasets/dump"
K = 9
N = 99
BAND_WIDTH = 3
LSH_THRESHOLDS = [0.1, 0.3, 0.7, 0.05, 0.01]
SEED = 72
HASH = hash

if __name__ == '__main__':
    names = []
    hash_brownies = []
    universe = set()
    with open(SONGS_DATASET_PATH, newline='') as songs:
        reader = csv.reader(songs)
        rows = iter(reader)
        next(rows)  # skip header
        for row in rows:
            names.append(row[0] + " -- " + row[1] + " -- url:" + row[4])
            hash_brownies.append(Shingling(io.StringIO(row[2]), K, HASH, universe).return_hashed_shingles())

    print(f"got {len(hash_brownies)} brownies")
    print("now signatures")
    universe_list = list(universe)
    signatures = [MinHashing(N, brownie, universe_list, SEED).return_signature() for brownie in hash_brownies]

    print("lsh")
    for threshold in LSH_THRESHOLDS:
        candidates = Lsh(signatures, BAND_WIDTH, threshold, HASH).ret_candidates()
        candidate_names = [(names[candidate[0]], names[candidate[1]]) for candidate in candidates]
        print(f"Candidates for threshold {threshold}:\n{candidate_names}\n")
