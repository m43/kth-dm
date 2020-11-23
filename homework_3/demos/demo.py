from models.Triest import Triest

DATASET = '../datasets/web-Google.txt'
M = 10000

trieste = Triest(fname=DATASET, m=M)
trieste.base()
trieste.improved()
