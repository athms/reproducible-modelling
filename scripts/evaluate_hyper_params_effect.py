#!/usr/bin/env python3

"""
This script evaluates the effect of varying different factors of the 
training of a classification model on its predictive performance in
sklearn's handwritten digit dataset. 

Each factor is varied separately while all other factors are held 
constant during training. Performance evaluation is performed by the 
use of 3-fold cross-validation.

This script requires that sklearn's handwritten digit dataset is stored
in 'data-path'. This can be achieved by first running 'load_data.py'
or 'make load'.

The script outputs a dataframe to 'results-path', which contains the 
classifier's predictive performance in each cross-validation fold.

Author: Armin W. Thomas; athms@stanford.edu
"""

import os
import argparse
import numpy as np
import sklearn
import hyper


def main():

    # parsing the script's input arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--n",
        required=False,
        default=100,
        type=int,
        help="How many values to evaluate for each hyper-parameter (default: 100)?")
    ap.add_argument(
        "--data-path",
        required=False,
        default='../data/',
        type=str,
        help="path where data file is stored (default: ../data/)")
    ap.add_argument(
        "--results-path",
        required=False,
        default='../results/',
        type=str,
        help="path where results are stored (default: ../results/)")
    args = ap.parse_args()

    # 0. fix the initial random seed
    np.random.seed(1111)

    # 1. load handwritten digits dataset
    # from ../data/
    data = np.load(
        '{}hand_written_digits_data.npy'.format(args.data_path),
        allow_pickle=True
    )[()]

    # 2. define our classification model
    # (we choose sklearn's SGDClassifier)
    classifier = sklearn.linear_model.SGDClassifier

    # 3. sample a set of hyper-parameters 
    # with 'hyper'
    hyper_params = hyper.sample_hyper_params(
        n=args.n
    )

    # 4. evaluate classifier performance for 
    # the specified hyper-parameter values
    # with 'hyper'
    results = hyper.evaluate_hyper_params_effects(
        X=data["data"],
        y=data["target"],
        classifier=classifier,
        hyper_params=hyper_params
    )

    # 5. save the results to ../results/data/
    os.makedirs('{}estimates/'.format(args.results_path), exist_ok=True)
    results.to_csv(
        '{}estimates/hyper_params_performance.csv'.format(args.results_path),
        index=False
    )


if __name__ == '__main__':

    main()