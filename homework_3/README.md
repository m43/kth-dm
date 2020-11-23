# Instructions on how to run the solution

There is exactly one demo that can be run and that accepts two command line arguments:

1. dataset path
2. value of parameter M (number of buckets to be used)

Python 3 should be installed. To run the demo, enter one of the commands below in terminal/cmd that is positioned in this directory (in which this README is). Feel free to change the two parameters.

`python -m demos.triest_demo datasets/com-amazon.ungraph.txt 100000`
`python -m demos.triest_demo datasets/com-dblp.ungraph.txt 100000`
`python -m demos.triest_demo datasets/com-youtube.ungraph.txt 100000`
`python -m demos.triest_demo datasets/facebook_combined.txt 100000`
