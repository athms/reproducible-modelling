# An examplary reproducible computational modelling project


## What are we doing?

This example was created for the lecture series of Stanford's Center for Open and REproducible Science (CORES).

The goal of this analysis is to study the effect of varying different hyper-parameters of the training of a simple classification model on its performance in sklearn's handwritten digit dataset. 

Specifically, we will study the effect of varying the learning rate, regularisation strength, number of gradient descent iterations, and random shuffling of the data on the cross-validated performance of [sklearn's default linear one-vs-rest SVM classifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html).

Each hyper-parameter is varied individually, while all other hyper-parameters are set to default values (see [scripts/evaluate_hyper_params_effect.py](scripts/evaluate_hyper_params_effect.py))


## Project organization

```bash
├── LICENSE            <- MIT License
├── Makefile           <- Makefile with targets to 'load', 'evaluate', and 'plot' ('make all' runs all three analysis steps)
├── poetry.lock        <- Details of used package versions
├── poetry.toml        <- Lists all dependencies
├── README.md          <- This README file.
├── data/
|    └──               <- A copy of the handwritten digit dataset provided by sklearn
|
├── results/
|    ├── estimates/
|    │    └──          <- Generated estimates of classifier performance
|    ├── figures/
|         └──          <- Generated figures
|
├── scrips/
|    ├── load_data.py                       <- Downloads the dataset to specified 'data-path'
|    ├── evaluate_hyper_params_effect.py    <- Runs hyper-parameter evaluation
|    ├── plot_hyper_params_effect.py        <- Summarizes results of evaluation in a figure
|    └── run_analysis.sh                    <- Sequentially runs all analysis scripts
|
├── src/
|    ├── __init__.py    <- Makes src a Python module
|    └──hyper/
|        ├──  __init__.py                   <- Makes hyper a Python module
|        ├── grid.py                        <- Functionality to sample hyper-parameter values
|        ├── evaluation.py                  <- Functionality to fit & cross-validate 
|        └── plotting.py                    <- Functionality to create results figure
|
└── setup.py           <- makes project pip-installable (pip install -e .) so that 'src' can be imported
```


## Installation

This project is written for Python 3.9.5 (we generally recommend [pyenv](https://github.com/pyenv/pyenv) for Python version management). 

This project manages dependencies with [Python Poetry](https://python-poetry.org/) and provides details of the used package versions  in [pyproject.toml](pyproject.toml).

To install all dependencies, run:
```bash
poetry install
```

This project further uses a custom Python module ([src/hyper](src/hyper)), which can be installed with:
```bash
pip install -e .
```

## Reproducing our analysis

Our analysis can be reproduced either by running [scripts/run_analysis.sh](scripts/run_analysis.sh):

```bash
cd scripts
poetry run bash run_analysis.sh
```

Or by the use of `make`:
```bash
make <ANALYSIS TARGET>
```

Our Makefile provides the following analysis targets:

| Analysis target | Description |
| --- | ----------- |
| all | Runs the entire analysis pipeline |
| load | Downloads sklearn's handwritten digit dataset |
| evaluate | Runs our cross-validated hyper-parameter evaluation |
| plot | Summarizes results of evaluation in a figure |


*This README file is strongly inspired by the [Cookiecutter Data Science Structure](https://drivendata.github.io/cookiecutter-data-science/)*