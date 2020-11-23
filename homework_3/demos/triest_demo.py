import pprint
import random
import sys
from timeit import default_timer as timer

from models.Triest import Triest

# DATASET = '../datasets/com-youtube.ungraph.txt'
# M = 1e5

if __name__ == '__main__':
    if (len(sys.argv)) != 3:
        raise Exception(f"Invalid number of arguments. Got {len(sys.argv)} arguments, expected 3 (1. irrelevant script "
                        f"name, 2. dataset path, 3. parameter M value (number of buckets to be used).")
    dataset_path = sys.argv[1]
    m = float(sys.argv[2])

    random.seed(720)
    pretty_print = pprint.PrettyPrinter()

    trieste = Triest(fname=dataset_path, m=m)

    print("Improved:", end="")
    pretty_print.pprint(trieste.improved())

    print("Base:", end="")
    pretty_print.pprint(trieste.base())
