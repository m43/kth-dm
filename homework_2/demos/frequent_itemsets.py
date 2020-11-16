import pprint
import sys

from models.AssociationRules import AssociationRules
from models.FrequentItemsets import FrequentItemsets

if __name__ == '__main__':
    if (len(sys.argv)) != 4:
        raise Exception(f"Invalid number of arguments. Got {len(sys.argv)} arguments, expected 4 (1. irrelevant script "
                        f"name, 2. dataset path, 3. support threshold, 4. confidence threshold).")
    songs_dataset_path = sys.argv[1]

    dataset_path = sys.argv[1]
    support_th = float(sys.argv[2])
    confidence_th = float(sys.argv[3])

    frequent_itemsets_s = FrequentItemsets(fname=dataset_path, s=support_th)
    print(f"Determined itemsets with support s={support_th}")
    print(f'The following itemsets have support higher or equal to {support_th * 100}%:')
    for k, support in enumerate(frequent_itemsets_s.support, 1):
        print(f'For k = {k}:')
        for itemset in support.keys():
            print(f'({itemset}, {support[itemset]})')
    print()

    pretty_print = pprint.PrettyPrinter()
    frequent_itemsets_cs = FrequentItemsets(fname=dataset_path, s=support_th * confidence_th)
    print(f"Determined additional itemsets with support c*s={support_th * confidence_th}")
    association_rules = AssociationRules.get_association_rules(frequent_itemsets_cs, confidence_th, support_th)
    print(f"Association rules for c={confidence_th} and s={support_th}")
    pretty_print.pprint({f"{set(r[0][0])} --> {set(r[0][1])} conf:{r[1]} interest: {r[2]}" for r in association_rules})
