#!/usr/bin/env python3

import pandas as pd
import numpy as np
from typing import Generator
from sklearn.linear_model import SGDClassifier


def _create_train_test_idx(
    n: int,
    frac_training: float=2./3.,
    shuffle: bool=False,
    seed: int=1234
    ) -> tuple[float]:
    """Create training and test indeces for a dataset 
    with 'n' samples.

    The indeces indicate which of the 'n' data samples 
    should be dedicated as trainig and test data.

    Args:
        n (int): How many samples are in the dataset?
        frac_training (float, optional): Fraction of 
            samples used for training. Defaults to 2./3..
        shuffle (bool, optional): Whether to shuffle
            index before creating the training / test split.
            Defaults to False.
        seed (int, optional): Random seed for shuffling.
            Defaults to 1234.

    Returns:
        tuple of training and test indeces
    """
    idx = np.arange(n)
    if shuffle:
        np.random.seed(seed)
        np.random.shuffle(idx)
    split = int(frac_training * idx.size)
    return (idx[:split], idx[split:])


def _yield_cv_train_val_idx(
    n: int,
    folds: int=3,
    shuffle: bool=False,
    seed: int=1234
    ) -> Generator[int, tuple[float], None]:
    """Yield cross-validation indeces for training and validation 
    datasets for each cross-validation fold, given a dataset 
    with 'n' samples.

    Args:
        n (int): How many samples are in the dataset?
        folds (int, optional): Number of cross-validation folds.
            Defaults to 3.
        shuffle (bool, optional): Whether to shuffle
            index before creating the training / test split.
            Otherwise data are separated into chunks in sequential order.
            Defaults to False.
        seed (int, optional): Random seed for shuffling.
            Defaults to 1234.

    Raises:
        ValueError: 'n' needs to larger than 'folds'

    Yields:
        Generator[int, tuple[float], None]: training and validation
            index for each fold
    """
    idx = np.arange(n)
    if idx.size < folds:
        raise ValueError(
            'n needs to be larger than folds.'
        )
    if shuffle:
        np.random.seed(seed)
        np.random.shuffle(idx)
    n_val = int(n / folds)
    for fold in range(folds):
        idx_val = idx[n_val*fold:n_val*(fold+1)]
        idx_train = np.array([i for i in idx if i not in idx_val])
        yield (idx_train, idx_val)


def cross_validate(
    X: np.ndarray,
    y: np.array,
    clf: SGDClassifier,
    steps: int,
    folds: int=3,
    ) -> pd.DataFrame:
    """Cross-validate classifier performance.

    Args:
        X (np.ndarray): Input data with shape (samples x features)
        y (np.array): Data labels with shape (samples)
        clf (sklearn classifier): Classifier to use. Classifier needs 
            to be  compatible with sklearn'S classifier specification 
            and implement {.score, .partial_fit} methods.
            Defaults to sklearns 'SGDClassifier'.
        steps (int): How many training steps?
            Each step represents one call to .partial_fit
        folds (int, optional): Number of cross-validation
            folds. Defaults to 3.

    Returns:
        pd.DataFrame: Cross-validation results
    """
    
    cv_results = []
    cv_iterator = _yield_cv_train_val_idx(
        n=y.size,
        folds=folds
    )
    for i, (idx_cv_train, idx_cv_val) in enumerate(cv_iterator):

        for _ in range(steps):
            clf.partial_fit(
                X=X[idx_cv_train],
                y=y[idx_cv_train],
                classes=np.unique(y)
            )

        score = clf.score(
            X=X[idx_cv_val],
            y=y[idx_cv_val],
        )

        res = {
            'CV-Fold': i,
            'Regularisation (Alpha)': clf.get_params()['alpha'],
            'Learning Rate': clf.get_params()['eta0'],
            'Steps': steps,
            'Random State': clf.get_params()['random_state'],
            'Accuracy' : score
        }

        cv_results.append(
            pd.DataFrame(res, index=[i])
        )

    cv_results = pd.concat(cv_results)
    cv_results['Mean Accuracy'] = cv_results['Accuracy'].mean()
    
    return cv_results


def evaluate_hyper_params_effects(
    X: np.ndarray,
    y: np.array,
    classifier: SGDClassifier,
    hyper_params: dict,
    folds: int=3,
    n_jobs=2,
    default_classifier_args: dict={
        'alpha': 0.0001,
        'eta0': 0.1,
        'steps': 50,
        'random_state': 999        
        }
    ) -> pd.DataFrame:
    """Evaluate effect of idividually varying {alpha, eta0, steps} 
    (while holding everything else constant ) on classifier 
    performance in {X, y}.

    Classifier performance is estimated by the use of cross-validation.

    Args:
        X (np.ndarray): Input data with shape (samples x features)
        y (np.array): Data labels with shape (samples)
        classifier (sklearn classifier): Classifier to use. Classifier needs to be 
            compatible with sklearn's classifier specification and 
            implement {.score, .partial_fit} methods. 
            Defaults to sklearns 'SGDClassifier'.
        hyper_params (dict): Hyper-parameter values to 
            evaluate; can be created by calling 
            hyper.sample_hyper_params()
        folds (int, optional): Number of cross-validation folds.
            Defaults to 3.
        n_jobs (int, optional): How many parallel jobs for fitting?
            Defaults to 2.
        default_classifier_args (dict, optional): Default classifier arguments
            that are used while individual factors are varied.
            Defaults to { 'alpha': 0.0001,
                          'eta0': 0.1,
                          'steps': 50,
                          'random_state': 999 }.

    Returns:
        pd.DataFrame: Cross-validation results
    """

    i, results = 0, []
    for par, values in hyper_params.items():
        
        for val in values:
            
            clf_args = dict(default_classifier_args)
            clf_args[par] = val
            
            clf = classifier(
                **{k: clf_args[k] for k in ["alpha", "eta0", "random_state"]},
                shuffle=True,
                learning_rate='constant',
                max_iter=clf_args["steps"],
                n_jobs=n_jobs
            )
            
            cv_results = cross_validate(
                X=X,
                y=y,
                clf=clf,
                steps=clf_args["steps"],
                folds=folds
            )

            cv_results = cv_results.set_index(np.arange(i,i+folds))
            i += 1

            cv_results["Varied"] = ' '.join(par.capitalize().split('_')) if '_' in par else par.capitalize()
            if par == 'eta0':
                cv_results["Varied"] = "Learning rate"
            elif par == 'alpha':
                cv_results["Varied"] = "Regularisation"
            
            results.append(cv_results)

    return pd.concat(results)