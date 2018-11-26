# Daniel Karamitrov
# 10/13/2018

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm  # color maps
from matplotlib.lines import Line2D  # for custom legend elements
from datetime import *

from enum import Enum


class Action(Enum):
    """
    Enumeration of possible contact actions. Primary use is
    for visualization and displaying action string description
    given an actionID.
    """
    SUBSCRIBE = 0
    UNSUBSCRIBE = 1
    VIEW_LINK = 2
    FORWARD_FRIEND = 3


def dfScatter(df, xcol='timestamp', ycol='contactID', catcol='actionID'):
    df = df.dropna(axis=0, subset=[catcol]).copy()  # drop any rows with a NaN actionID
    fig, ax = plt.subplots()
    categories = np.unique(df[catcol].unique())
    colors = np.linspace(0, 1, len(categories))
    colordict = dict(zip(categories, colors))
    cmap_name = 'plasma'
    my_cm = cm.cmaps_listed[cmap_name]

    df["Color"] = df[catcol].apply(lambda x: colordict[x])
    ax.scatter(df[xcol].tolist(), df[ycol].tolist(), cmap=cmap_name, c=df.Color, marker='.', s=(72./fig.dpi)**2)
    ax.yaxis.set_ticklabels([])
    ax.set_ylabel("Contacts")
    legend_elements = [Line2D([0], [0], marker='o', color=my_cm(colordict[c]),
                              label=Action(c).name) for c in categories]
    ax.legend(loc='upper left', handles=legend_elements,)  # bbox_to_anchor=(0.9, 0.9))
    ax.xaxis.set_ticklabels([])
    # fig.autofmt_xdate()
    # ax.set_xlim(date(2012, 1, 1), date(2014, 1, 1))
    ax.set_title('Contact Action Timeline')
    # ax.yaxis.grid(True)
    return fig


raw_df = pd.read_csv('medium_dataset_raw.csv')

fig = dfScatter(raw_df, xcol='timestamp', ycol='contactID', catcol='actionID')
fig.savefig('medium_fig.png', bbox_inches='tight', figsize=(20, 20), dpi=600)
