# Instructions on how to run the solution

Pick a graph from `graphs` folder (for example `3elt.graph`, `add20.graph` etc.), let its name be GRAPH_NAME, then you can enter the following commands to compile, run and plot:

```sh
./compile.sh
./run.sh -graph graphs/GRAPH_NAME
./plot.sh output/GRAPH_NAME_*.txt
```

You can also try running the python batch script, but we give no promises for non Linux operating systems. The batch script has configurable parameters (which graphs to run and in which configurations) inside itself. Enter the following to run the python batch script:

```sh
./demo.py
```
