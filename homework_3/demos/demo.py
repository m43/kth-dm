from models.Trieste import Trieste

DATASET = '../datasets/web-Google.txt'
M = 10000

trieste = Trieste(fname=DATASET, m=M)
trieste.base()