import numpy as np


class MinHashing:
    """
    Represents a minHash signature of a set of hash values.
    """

    def __init__(self, length, hash_values, universe, seed=0):
        """
        Constructs a MinHashing object using given set/vector of hash values for a given universe of items, a seed
        for creating random permutations and a hash function.

        :param length: The length of the signature (number of permutations)
        :param hash_values: The hash values for which the signature is made
        :param seed: Seed used for to generate permutations
        :param universe: An array of all possible hashed k-shingles.
        """

        # calculate minHash signature
        characteristic_column = [1 if item in hash_values else 0 for item in universe]
        np.random.seed(seed)  # set seed for numpy
        permutations = [np.random.permutation(characteristic_column) for _ in range(length)]
        # signature is an array of the row indexes where a 1 first appeared for each permutation
        self.signature = [np.where(permutation == 1)[0][0] for permutation in permutations]

    def return_signature(self):
        """
        Returns the minHash signature.

        :return: The minHash signature.
        """

        return self.signature
