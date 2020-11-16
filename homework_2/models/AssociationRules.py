from itertools import combinations

from models.FrequentItemsets import FrequentItemsets


class AssociationRules:

    @staticmethod
    def get_association_rules(frequent_itemsets_object: FrequentItemsets, confidence_th: float, support_th: float):
        """
        Static function that generates association rules with at least the given support threshold for left side of the
        rule and with at least the given confidence level.

        :param frequent_itemsets_object: FrequentItemsets object of the dataset. Has all itemsets that have support at
            least confidence_th*support_th
        :param confidence_th: Confidence threshold for generating association rules. Percentage.
        :param support_th: Support threshold for itemsets. Percentage.
        :return list of ((rule_left_set, rule_right_set), confidence, interest)
        """

        universe = {}
        for k_sets in frequent_itemsets_object.support:
            universe.update(k_sets)
        universe = {frozenset(k): v for k, v in universe.items()}

        result = []
        for frequent_set in universe:
            result.extend(
                AssociationRules._generate_rules_bruteforce(universe, frequent_set, confidence_th, support_th))

        return result

    @staticmethod
    def _generate_rules_bruteforce(universe, frequent_set, confidence_th, support_th) -> list:
        father_support = universe[frequent_set]

        rules = []
        for k in range(1, len(frequent_set)):
            for left in combinations(frequent_set, k):
                left = frozenset(left)
                if universe[left] < support_th:
                    continue

                right = frequent_set.difference(left)

                confidence = father_support / universe[left]
                interest = confidence - universe[right]

                if confidence >= confidence_th:
                    rules.append(((frozenset(left), frozenset(right)), confidence, interest))

        return rules
