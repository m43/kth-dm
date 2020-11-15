import itertools


class FrequentItemsets:
    """
    Represents frequent item sets of a given file whose each line represents a basket of items, where items are integer
    numbers.
    """

    def __init__(self, fname, s):
        """
        Creates a FrequentItemSets object where frequent items must have a support larger than given s.

        :param fname: Path to dataset (file) which the frequent itemsets will be calculated for.
        :param s:  Similarity threshold below which itemsets are considered unsupported.
        """

        # read file line by line
        k = 1
        self.support = []  # array containing dictionaries of frequent itemsets (size of itemsets depends on the index)
        self.frequent_itemsets = set()  # set of frequent itemsets
        while True:
            k_count = dict()  # dictionary which counts appearnce of k-sized tuples
            basket_count = 0  # used for calculating support
            ignore_set = set()  # remembers which itemsets have no support from subsets
            with open(fname, 'r') as data:
                # count k sized subsets of baskets
                for line in data:
                    basket_count += 1
                    # sorted so itertools.combinations creates identical tuples for the same items of any basket
                    current_basket = sorted([int(x) for x in line.strip().split()])  # array of items

                    # skip baskets that are too small for current k
                    if len(current_basket) < k:
                        continue

                    # generate all k-sized subsets
                    possible_k_tuples = list(itertools.combinations(current_basket, k))

                    # ignore those k-sized tuples whose subsets have no support if k > 1
                    candidates = set()
                    if k > 1:
                        for k_tuple in possible_k_tuples:
                            if k_tuple in ignore_set:
                                continue
                            add = True
                            for length in range(1, k):
                                subsets = list(itertools.combinations(k_tuple, length))
                                for subset in subsets:
                                    if subset not in self.frequent_itemsets:
                                        add = False
                                        ignore_set.add(k_tuple)
                                        break
                            if add:
                                candidates.add(k_tuple)
                    else:
                        candidates = set(possible_k_tuples)

                    # count all k_tuples
                    for k_tuple in candidates:
                        if k_tuple in k_count:
                            k_count[k_tuple] += 1
                        else:
                            k_count[k_tuple] = 1

            # remove those k-sized tuples which have support < s, otherwise remember their support and them
            keys = list(k_count.keys())
            for key in keys:
                support = k_count[key] / basket_count
                if support < s:
                    del k_count[key]
                else:
                    k_count[key] = support
                    self.frequent_itemsets.add(key)

            # terminate if no k-sized subsets have support
            if len(k_count) == 0:
                break

            # otherwise remember those k-sized tuples which have support
            self.support.append(k_count)

            # increase k and continue
            k += 1
