#!/usr/bin/env bash

CMD1="python load_data.py --data-path ../data/"
echo "Now running: $CMD1"
$CMD1
echo "..done."

CMD2="python evaluate_hyper_params_effect.py --n 100 --data-path ../data/ --results-path ../results/"
echo "Now running: $CMD2"
$CMD2
echo "..done."

CMD3="python plot_hyper_params_effect.py --results-path ../results/"
echo "Now running: $CMD3"
$CMD3
echo "..done."