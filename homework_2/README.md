# Instructions on how to run the solution

There is exactly one demo that can be run and that accepts three command line arguments:

1. dataset path
2. support threshold
3. condidence threshold

Python 3 should be installed. To run the demo, enter one of the commands below in terminal/cmd that is positioned in this directory (in which this README is). Commands are given for two different datasets.

## Dataset 1

This dataset has 100K baskets. It is the dataset given in the homework instructions.

`python -m demos.frequent_itemsets datasets/baskets/T10I4D100K.dat 0.01 0.75`

With given parameters, the resulting association rules should be:

```js
Association rules for c=0.75 and s=0.01
{'{227, 390} --> {722} conf:0.8646329837940897 interest: 0.8061829837940897',
 '{704, 39} --> {825} conf:0.9349593495934959 interest: 0.9041093495934959',
 '{704, 825} --> {39} conf:0.9392014519056261 interest: 0.8966214519056261',
 '{722, 390} --> {227} conf:0.8704414587332053 interest: 0.8522614587332054',
 '{825, 39} --> {704} conf:0.8719460825610783 interest: 0.8540060825610784'}
```

## Dataset 2

This dataset has 1M baskets and a lower support threshold value should be used to find some association rules. It is also slower.

`python -m demos.frequent_itemsets datasets/baskets/chainstoreFIM.txt 0.005 0.5`

With the given parameters, the resulting association rule should be just the following one:
```{'{11780} --> {11783} conf:0.5204726573234405 interest: 0.5126016767124691'}```
