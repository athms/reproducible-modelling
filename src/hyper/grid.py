#!/usr/bin/env python3

import numpy as np


def sample_hyper_params(
    n: int=10,
    param_bounds: dict={
        'alpha': (0.000001, 0.001),
        'eta0': (0.001, 1),
        'steps': (1, 200)
        }
    ) -> dict:
    """Sample 'n' equally-spaced values for 
    {alpha, eta0, steps} between specified
    parameter bounds, in addition to 
    'n' random seed values.

    Args:
        n (int, optional): How many paramater values to sample
            for each hyper-parameter? Defaults to 10.
        param_bounds (dict, optional): Parameter bounds.
            Defaults to { 'alpha': (0.000001, 0.001),
                          'eta0': (0.001, 1),
                          'steps': (1, 100) }.

    Returns:
        dict: Hyper-parameter values.
    """
    return {
        "alpha": np.linspace(*param_bounds["alpha"], num=n),
        "eta0": np.linspace(*param_bounds["eta0"], num=n),
        'steps': np.linspace(*param_bounds["steps"], num=n).astype(int),
        "random_state": np.random.uniform(100000, 999999, size=n).astype(int)
    }




