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

    cmap_name = 'twilight'
    my_cm = cm.cmaps_listed[cmap_name]
    legend_colors = my_cm(colors)

    df["Color"] = df[catcol].apply(lambda x: colordict[x])
    ax.scatter(df[xcol].tolist(), df[ycol].tolist(), cmap=cmap_name, c=df.Color, marker='|')
    ax.yaxis.set_ticklabels([])
    ax.xaxis.set_ticklabels([])
    ax.set_ylabel("Contacts")
    legend_elements = [Line2D([0], [0], marker='o', color=my_cm(colordict[c]),
                              label=Action(c).name) for c in categories]
    fig.legend(loc='right', bbox_to_anchor=(1.3, 0.5), handles=legend_elements)
    # fig.autofmt_xdate()
    # ax.set_xlim([date(2014, 11, 17), date(2014, 11, 18)])
    ax.set_title('Contact Action Timeline')
    # ax.yaxis.grid(True)
    return fig


raw_df = pd.read_csv('medium_dataset_raw.csv')

fig = dfScatter(raw_df, xcol='timestamp', ycol='contactID', catcol='actionID')
fig.savefig('medium_fig.png', bbox_inches='tight', dpi=300)
