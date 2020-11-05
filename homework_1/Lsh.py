from CompareSignatures import CompareSignatures


class Lsh:
    """
    Represents a Locality Sensitive Hashing (LSH) of  minHash signatures.
    """

    def __init__(self, signatures, band_width, threshold, hash_function):
        """
        Constructs an LSH object given an array of minHash signatures, band width, and a hash function

        :param signatures: MinHash signatures to be compared
        :param band_width: Width of bands (number of rows) the signatures are separated into.
        Must divide signature length.
        :param threshold: The level of similarity two signatures must achieve to be considered as candidates.
        :param hash_function: Function to be used for hashing bands.
        """

        # create candidates member
        self.candidates = None

        # remember originals
        self.signatures = signatures
        self.band_width = band_width
        self.threshold = threshold
        self.hash_function = hash_function

        # calculates LSH
        number_of_bands = len(signatures[0]) // band_width
        self.lsh_matrix = []
        for signature in signatures:
            lsh_signature = []
            for band_id in range(number_of_bands):
                band = tuple(signature[band_id * band_width: band_id * band_width + band_width])
                lsh_signature.append(hash_function(band))
            self.lsh_matrix.append(lsh_signature)

    def ret_candidates(self):
        """
        Returns an array of pairs of signatures (their respective indices) which are candidates for similarity.

        :return: An array of pairs which are candidates for similarity.
        """

        # if created once return right away
        if self.candidates is not None:
            return self.candidates

        # calculate candidates
        self.candidates = []
        for i in range(len(self.lsh_matrix)):
            for j in range(i + 1, len(self.lsh_matrix)):
                comparison = CompareSignatures(self.lsh_matrix[i], self.lsh_matrix[j])
                if comparison.similarity > self.threshold:
                    self.candidates.append((i, j))

        return self.candidates
