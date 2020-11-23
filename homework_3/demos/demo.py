import random
from timeit import default_timer as timer

from models.Triest import Triest

DATASET = '../datasets/com-youtube.ungraph.txt'
M = 1e5

if __name__ == '__main__':
    random.seed(720)

    start = timer()
    trieste = Triest(fname=DATASET, m=M)
    print(f"Improved: {trieste.improved()}")
    print(f"%%% timing: {timer() - start}s %%%\n")

    start = timer()
    print(f"Base: {trieste.base()}")
    print(f"%%% timing: {timer() - start}s %%%\n")
