from models.CompareSets import CompareSets
from models.CompareSignatures import CompareSignatures
from models.Lsh import Lsh
from models.MinHashing import MinHashing
from models.Shingling import Shingling

K = 10  # defines shingle size
N = 99  # defines the length of minHash signatures
BAND_WIDTH = 3  # width of bands in LSH, N (length of minHash signatures) should be divisible by this number
LSH_THRESHOLD = 0.7  # threshold used for to calculate candidates in LSH
SEED = 1998  # seed used for minHash permutations
HASH = hash

if __name__ == '__main__':
    print('\nShingling comparisons'
          '\n---------------------------------------------------')

    universe = set()

    my_shingles_1 = Shingling(open('../../datasets/text/test_1.txt', "r", encoding='UTF-8'), K, HASH, universe)
    my_shingles_2 = Shingling(open('../../datasets/text/test_1.txt', "r", encoding='UTF-8'), K, HASH, universe)
    my_shingles_3 = Shingling(open('../../datasets/text/test_2.txt', "r", encoding='UTF-8'), K, HASH, universe)

    my_hash_1 = my_shingles_1.return_hashed_shingles()
    my_hash_2 = my_shingles_2.return_hashed_shingles()
    my_hash_3 = my_shingles_3.return_hashed_shingles()

    my_comparison_1 = CompareSets(my_hash_1, my_hash_2)
    my_comparison_2 = CompareSets(my_hash_1, my_hash_3)

    print('Jaccard similarity between the same text: ', my_comparison_1.ret_jaccard_sim())
    print('Jaccard distance between the same text: ', my_comparison_1.ret_jaccard_dist())

    print('Jaccard similarity between two texts: ', my_comparison_2.ret_jaccard_sim())
    print('Jaccard distance between two texts: ', my_comparison_2.ret_jaccard_dist())

    print('\n###################################################\n\n'
          'MinHash signature comparisons'
          '\n---------------------------------------------------')

    ordered_universe = list(universe)

    my_min_hash_1 = MinHashing(N, my_hash_1, ordered_universe, SEED)
    my_min_hash_2 = MinHashing(N, my_hash_2, ordered_universe, SEED)
    my_min_hash_3 = MinHashing(N, my_hash_3, ordered_universe, SEED)

    my_signature_1 = my_min_hash_1.return_signature()
    my_signature_2 = my_min_hash_2.return_signature()
    my_signature_3 = my_min_hash_3.return_signature()

    my_comparison_3 = CompareSignatures(my_signature_1, my_signature_2)
    my_comparison_4 = CompareSignatures(my_signature_1, my_signature_3)

    print('Signature similarity between the same text: ', my_comparison_3.ret_sim())
    print('Signature distance between the same text: ', my_comparison_3.ret_dist())

    print('Signature similarity between two texts: ', my_comparison_4.ret_sim())
    print('Signature distance between two texts: ', my_comparison_4.ret_dist())

    print('\n###################################################\n\n'
          'LSH candidates'
          '\n---------------------------------------------------')

    signatures = [my_signature_1, my_signature_2, my_signature_3]

    threshold_1 = 0.1
    threshold_2 = 0.3

    my_lsh_1 = Lsh(signatures, BAND_WIDTH, threshold_1, HASH)
    my_lsh_2 = Lsh(signatures, BAND_WIDTH, threshold_2, HASH)

    print(f'With threshold {threshold_1} LSH returned the following pairs of signatures as candidates:',
          my_lsh_1.ret_candidates())
    print(f'With threshold {threshold_2} LSH returned the following pairs of signatures as candidates:',
          my_lsh_2.ret_candidates())
    print('(index 0 and index 1 are the same text, while index 2 is a similar, but different text)')

    print('\n###################################################\n\n')
