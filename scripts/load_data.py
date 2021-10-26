#!/usr/bin/env python3

"""
This script downloads the handwritten digits dataset
provided by sklearn to the specified 'data-path'.

Author: Armin W. Thomas; athms@stanford.edu
"""

import os
import argparse
import numpy as np
from sklearn.datasets import load_digits


def main():

    # parsing the script's input arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--data-path",
        required=False,
        default='../data/',
        type=str,
        help="path where data file is stored (default: ../data/)")
    args = ap.parse_args()

    # 1. define local target path for dataset
    filepath = '{}hand_written_digits_data.npy'.format(args.data_path)

    # 2. download and store handwritten digits data
    # to 'filepath', if it does not exist yet
    if not os.path.isfile(filepath):
        os.makedirs('../data/', exist_ok=True)
        data = load_digits()
        np.save(filepath, data)


if __name__ == '__main__':

    main()