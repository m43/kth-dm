import random

import numpy as np

from models.Triest import Triest

# DATASET = '../datasets/web-Google.txt'
DATASET = '../datasets/com-youtube.ungraph.txt'
M = 20000

if __name__ == '__main__':
    np.random.seed(72)
    random.seed(72)

    trieste = Triest(fname=DATASET, m=M)
    print(f"Base: {trieste.base()}")
    print(f"Improved: {trieste.improved()}")

