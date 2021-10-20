#!/usr/bin/eny python3

import pandas as pd
import seaborn as sns
from matplotlib.pyplot import gca


def plot_hyper_params_performance(
    df: pd.DataFrame,
    outcome_var='Mean Accuracy',
    ) -> sns.FacetGrid:    
    """Plot distribution of 'outcome_var' as a 
    function of each 'Varied' hyper-parameter in 
    'df'.

    For details on the formatting of 'df', see 
    hyper.evaluate_hyper_params_effects()

    Args:
        df (pd.DataFrame): DataFrame containing one 
            row for each model fitting run with the 
            following columns:
                - outcome_var (see below)
                - 'Varied' indicates the hyper-parameter
                  that was varied in this cross-validation run 
                - one column for each hyper-parameter 
                  containing its respective value in the 
                  cross-validation run.
        outcome_var (str, optional): Name of outcome
            variable that is plotted. Defaults to 
            'Mean Accuracy'.
            
    Returns:
        sns.FacetGrid: figure as seaborn FacetGrid
    """

    df = df.copy()
    
    g = sns.FacetGrid(
        df,
        row="Varied",
        hue="Varied",
        aspect=3,
        height=1.5,
        xlim=(0.7, 1)
    )

    g.map(
        sns.kdeplot,
        outcome_var,
        bw_adjust=.5,
        clip_on=False,
        fill=True, 
        alpha=1,
        linewidth=1.5
    )
    g.map(
        sns.kdeplot,
        outcome_var,
        clip_on=False,
        color="w",
        lw=2,
        bw_adjust=.5
    )

    g.refline(
        y=0,
        linewidth=2,
        linestyle="-",
        color=None,
        clip_on=False
    )

    def label(x, color, label):
        ax = gca()
        ax.text(
            0, .2,
            label,
            fontweight="bold",
            color=color,
            ha="left",
            va="center",
            transform=ax.transAxes
        )

    g.map(label, outcome_var)

    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)

    return g