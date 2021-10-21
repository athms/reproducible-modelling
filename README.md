# An example of a reproducible modelling project


## What are we doing?

This example was created for the [2021 fall lecture series](https://datascience.stanford.edu/news/center-open-and-reproducible-science-cores-fall-lecture-series) of [Stanford's Center for Open and REproducible Science (CORES)](https://datascience.stanford.edu/cores).

The goal of this analysis is to study the effect of varying different hyper-parameters of the training of a simple classification model on its performance in [scikit-learn's handwritten digit dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#digits-dataset). 

Specifically, we will study the effect of individually varying the learning rate, regularisation strength, number of gradient descent iterations, and random shuffling of the data on the 3-fold cross-validation performance of [scikit-learn's default linear one-vs-rest SVM classifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html).

Importantly, we vary each hyper-parameter separately while all other hyper-parameters are set to default values (see [scripts/evaluate_hyper_params_effect.py](scripts/evaluate_hyper_params_effect.py)).


## Project organization

```bash
├── LICENSE            <- MIT License
├── Makefile           <- Makefile with targets to 'load', 'evaluate', and 'plot' ('make all' runs all three analysis steps)
├── poetry.lock        <- Details of used package versions
├── pyproject.toml     <- Lists all dependencies
├── README.md          <- This README file.
├── docs/              <- Slides of the practical tutorial
├── data/
|    └──               <- A copy of the handwritten digit dataset provided by scikit-learn
|
├── results/
|    ├── estimates/
|    │    └──          <- Generated estimates of classifier performance
|    └── figures/
|         └──          <- Generated figures
|
├── scrips/
|    ├── load_data.py                       <- Downloads the dataset to specified 'data-path'
|    ├── evaluate_hyper_params_effect.py    <- Runs cross-validated hyper-parameter evaluation
|    ├── plot_hyper_params_effect.py        <- Summarizes results of evaluation in a figure
|    └── run_analysis.sh                    <- Runs all analysis steps
|
└── src/
    ├── hyper/
    │    ├──  __init__.py                   <- Makes 'hyper' a Python module
    │    ├── grid.py                        <- Functionality to sample hyper-parameter grid
    │    ├── evaluation.py                  <- Functionality to evaluate classifier performance, given hyper-parameters
    │    └── plotting.py                    <- Functionality to visualize results
    └── setup.py                            <- Makes 'hyper' pip-installable (pip install -e .)  
```

## Data description

We use the handwritten digits dataset provided by [scikit-learn](https://scikit-learn.org/stable/). For details on this dataset, see scikit-learn's documentation:

https://scikit-learn.org/stable/datasets/toy_dataset.html#digits-dataset


## Installation

This project is written for Python 3.9.5 (we recommend [pyenv](https://github.com/pyenv/pyenv) for Python version management). 

All software dependencies of this project are managed with [Python Poetry](https://python-poetry.org/). All details about the used package versions are provided in  [pyproject.toml](pyproject.toml).

To clone this repository to your local machine, run:
```bash
git clone https://github.com/athms/reproducible-modelling
```

To install all dependencies with `poetry`, run:
```bash
cd reproducible-modelling/
poetry install
```

To reproduce our analyses, you additionally need to install our custom Python module ([src/hyper](src/hyper)) in your `poetry` environment:
```bash
cd src/
poetry run pip install -e .
```

## Reproducing our analysis

Our analysis can be reproduced either by running [scripts/run_analysis.sh](scripts/run_analysis.sh):

```bash
cd scripts
poetry run bash run_analysis.sh
```

..or by the use of `make`:
```bash
poetry run make <ANALYSIS TARGET>
```

We provide the following targets for `make`:

| Analysis target | Description |
| --- | ----------- |
| all | Runs the entire analysis pipeline |
| load | Downloads scikit-learn's handwritten digit dataset |
| evaluate | Runs our cross-validated hyper-parameter evaluation |
| plot | Creates our results figure |



*This README file is strongly inspired by the [Cookiecutter Data Science Structure](https://drivendata.github.io/cookiecutter-data-science/)*
