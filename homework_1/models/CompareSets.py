class CompareSets:
    """
    Represents a comparison between two sets containing hash values in terms of Jaccard similarity.
    """

    def __init__(self, first_set, second_set):
        """
        Constructs CompareSets object given two sets of hash values.

        :param first_set: First set of hash values.
        :param second_set: Second set of hash values.
        """

        # calculate Jaccard similarity and save it
        self.jaccard_similarity = len(first_set.intersection(second_set)) / len(first_set.union(second_set))

    def ret_jaccard_sim(self):
        """
        Returns the calculated Jaccard similarity between two sets of hash values the object was constructed with.

        :return: Jaccard similarity
        """

        return self.jaccard_similarity

    def ret_jaccard_dist(self):
        """
        Returns the calculated Jaccard similarity between two sets of hash values the object was constructed with.

        :return: Jaccard similarity
        """

        return 1 - self.jaccard_similarity
