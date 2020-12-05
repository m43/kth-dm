N=8
declare -a graphs=(
    "3elt.graph" "4elt.graph"
    "add20.graph"
    # "add20.graph.part.4"
    "data.graph"
    "facebook.graph"
    # "facebook.graph.part.4"
    # "google.graph"
    # "google.graph.part.4"
    "scale-1000.graph"
    "synth-0.25-1000.graph" "synth-0.75-1000.graph" "synth-0.95-10000.graph" "synth-0.95-1000.graph"
    "synth-0.95-25000.graph" "synth-0.95-250.graph" "synth-0.95-5000.graph"
    "twitter.graph"
    # "TwitterGraph.net"
    "vibrobox.graph"
    "ws-10000.graph" "ws-1000.graph" "ws-25000.graph" "ws-250.graph" "ws-5000.graph"
)


# initialize a semaphore with a given number of tokens
open_sem(){
    mkfifo pipe-$$
    exec 3<>pipe-$$
    rm pipe-$$
    local i=$1
    for((;i>0;i--)); do
        printf %s 000 >&3
    done
}

# run the given command asynchronously and pop/push tokens
run_with_lock(){
    local x
    # this read waits until there is something to read
    read -u 3 -n 3 x && ((0==x)) || exit $x
    (
     ( "$@"; )
    # push the return code of the command to the semaphore
    printf '%.3d' $? >&3
    )&
}

task(){
    ./run.sh -graph graphs/"$1"
    ./plot.sh output/"$1"_*.txt
}

open_sem $N
for thing in "${graphs[@]}"; do
    run_with_lock task $thing
done 

wait
python extract_results.py output > output/results.csv