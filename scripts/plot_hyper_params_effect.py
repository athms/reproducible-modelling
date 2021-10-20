#!/usr/bin/env python3

"""
This script summarizes the results of running 
'evaluate_hyper_params_effect.py' in a figure.

The script requires that the 'evaluate_hyper_params_effect.py' 
script has been run and that its results are stored in 'results-path'.
This can also be achieved by running 'make evaluate'.

The resulting figure is saved to 'results-path'.

Author: Armin W. Thomas; athms@stanford.edu
"""

import os
import argparse
import pandas as pd
import hyper
from seaborn import set_theme
set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})


def main():

    # parsing the script's input arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--results-path",
        required=False,
        default='../results/',
        type=str,
        help="path where results are stored (default: ../results/)")
    args = ap.parse_args()

    # 1. load the results of 'evaluate_hyper_params_effect.py'
    # from specified 'results-path'
    results = pd.read_csv(
        "{}estimates/hyper_params_performance.csv".format(args.results_path)
    )

    # 2. create the figure with 'hyper.plot_hyper_params_performance'
    #  and save it to 'results-path' 
    g = hyper.plot_hyper_params_performance(results)
    os.makedirs('{}figures/'.format(args.results_path), exist_ok=True)
    g.savefig(
        '{}figures/fig_hyper_params_effects.png'.format(args.results_path),
        dpi=330
    )


if __name__ == '__main__':

    main()