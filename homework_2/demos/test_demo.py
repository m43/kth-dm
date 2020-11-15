from models.FrequentItemsets import FrequentItemsets

FILE_PATH = '../../datasets/baskets/T10I4D100K.dat'
SUPPORT = 0.01  # 1% is said to be a good support threshold for brick-and-mortar stores

my_fis = FrequentItemsets(fname=FILE_PATH, s=SUPPORT)
print(f'The following itemsets have support higher or equal to {SUPPORT*100}%:')
for k, support in enumerate(my_fis.support, 1):
    print(f'For k = {k}:')
    for itemset in support.keys():
        print(f'({itemset}, {support[itemset]})', end=' ')
    print('\n')
