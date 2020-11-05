class CompareSignatures:
    """
    Represents a comparison between two signatures.
    """

    def __init__(self, first_signature, second_signature):
        """
        Construct a CompareSignatures object and calculate the similarity of two signature.

        :param first_signature: The first signature of the two to be compared.
        :param second_signature: The second signature of the two to be compared.
        """

        # remember originals
        self.first_signature = first_signature
        self.second_signature = second_signature

        # calculate similarity between the two signatures
        self.similarity = 0
        for i in range(len(first_signature)):
            if first_signature[i] == second_signature[i]:
                self.similarity += 1
        self.similarity /= len(first_signature)

    def ret_sim(self):
        """
        Returns similarity between the two signatures the object was constructed with.

        :return: Similarity between the two signatures the object was constructed with
        """

        return self.similarity

    def ret_dist(self):
        """
        Returns distance between the two signatures the object was constructed with.

        :return: Distance between the two signatures the object was constructed with
        """

        return 1 - self.similarity
