import itertools

from models.CompareSignatures import CompareSignatures


class Lsh:
    """
    Represents a Locality Sensitive Hashing (LSH) of  minHash signatures.
    """

    @staticmethod
    def ret_candidates(signatures, band_width, threshold, hash_function=hash):
        """
        Returns an array of tuples (candidate_i,candidate_j,similarity) for signatures which are candidates based on
        given threshold

        :param signatures: MinHash signatures to be compared
        :param band_width: Width of bands (number of rows) the signatures are separated into.
        Must divide signature length.
        :param threshold: The level of similarity two signatures must achieve to be considered as candidates.
        :param hash_function: Function to be used for hashing bands.
        :return: An array of tuples with indices of candidate pair and corresponding similarity: (i,j,similarity)
        """

        number_of_bands = len(signatures[0]) // band_width

        signature_bands_matrix = []  # number_of_signatures x number_of_bands
        for s in signatures:
            signature_bands = []
            for band_id in range(number_of_bands):
                band = tuple(s[band_id * band_width: band_id * band_width + band_width])
                signature_bands.append(hash_function(band))
            signature_bands_matrix.append(signature_bands)

        potential_candidates = set()
        for band_id in range(number_of_bands):
            buckets = {}
            for signature_id in range(len(signatures)):
                b = signature_bands_matrix[signature_id][band_id]
                if b not in buckets:
                    buckets[b] = []
                buckets[b].append(signature_id)
            for _, bucket_value in buckets.items():
                potential_candidates.update(itertools.combinations(bucket_value, 2))

        candidates = []
        for pci, pcj in potential_candidates:
            similarity = CompareSignatures(signatures[pci], signatures[pcj]).ret_sim()
            if similarity > threshold:
                candidates.append((pci, pcj, similarity))

        return candidates
