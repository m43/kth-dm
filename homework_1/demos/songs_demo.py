import csv
import io
import sys

from tqdm import tqdm

from demos.util import demo
from models.Shingling import Shingling

# SONGS_DATASET_PATH = "../datasets/scraped_songs.csv"
# SONGS_DATASET_PATH = "../datasets/scraped_songs_2.csv"
K = 5
N = 100
BAND_WIDTH = 5
THRESHOLD = 0.5
SEED = 72
MINHASH_HASH = hash
LSH_BAND_HASH = hash
# MAX_SONGS = -1
MAX_SONGS = 5000
TEST_BARE = True
TEST_MINHASH = True
TEST_LSH = True


def load_songs(songs_dataset_path, max_songs=-1):
    names = []
    hash_brownies = []
    universe = set()
    with open(songs_dataset_path, newline='') as songs:
        reader = csv.reader(songs)
        rows = iter(reader)
        next(rows)  # skip header
        for row in tqdm(rows):
            if 0 <= max_songs == len(names):
                break
            names.append(row[0] + " -- " + row[1] + " -- url:" + row[4])
            hash_brownies.append(Shingling(io.StringIO(row[2]), K, MINHASH_HASH, universe).return_hashed_shingles())

    return universe, names, hash_brownies


if __name__ == '__main__':
    if (len(sys.argv)) != 2:
        raise Exception(f"Invalid number of arguments. Got {len(sys.argv)} arguments, expected 2 (irrelevant script "
                        f"name and dataset path).")
    songs_dataset_path = sys.argv[1]
    demo(lambda: load_songs(songs_dataset_path, MAX_SONGS), K, N, BAND_WIDTH, THRESHOLD, SEED, MINHASH_HASH,
         LSH_BAND_HASH, TEST_BARE, TEST_MINHASH, TEST_LSH)
