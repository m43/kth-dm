import numpy as np
from tqdm import tqdm


class MinHashing:
    """
    Represents a minHash signature of a set of hash values.
    """

    def __init__(self, length, hash_brownies, universe, seed=0):
        """
        Constructs a MinHashing object using given set/vector of hash values for a given universe of items, a seed
        for creating random permutations and a hash function.

        :param length: The length of the signature (number of permutations)
        :param hash_brownies: The hash values for which the signatures are made.
        :param seed: Seed used for to generate permutations
        :param universe: An array of all possible hashed k-shingles.
        """

        self.signatures = []
        np.random.seed(seed)
        permutations = [np.random.permutation(np.arange(len(universe))) for _ in range(length)]
        for brownie in tqdm(hash_brownies):
            signature = []
            for perm in permutations:
                for i in range(len(perm)):
                    if universe[perm[i]] in brownie:
                        signature.append(i)
                        break
            self.signatures.append(signature)

    def return_signatures(self):
        """
        Returns the minHash signatures.

        :return: The minHash signatures.
        """

        return self.signatures
