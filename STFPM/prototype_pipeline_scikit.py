# 10/1/2018
# Daniel Karamitrov

# using scikit-learn pipeline to perform feature extraction
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
import pandas as pd
import numpy as np
from uuid import *
from enum import Enum
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.pipeline import Pipeline
from sklearn import svm
import random
import sklearn_pandas as skpd

from base64 import b64encode
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from datetime import *


###### DATA GENERATOR STARTS HERE
class Action(Enum):
    EMAIL_VIEW_LINK = 0
    EMAIL_WEBFORM_UNSUB = 1
    EMAIL_WEBFORM_FTAF = 2
    EMAIL_WEBFORM_VIEW = 3
    CUSTOM_ACTION_A = 4
    CUSTOM_ACTION_B = 5
    CUSTOM_ACTION_C = 6



random.seed(42)
#
TOTAL_CONTACTS = 30
TOTAL_EMAILS = 20

contactIDs = ["c_{:05d}".format(i) for i in range(0, TOTAL_CONTACTS + 1)]
deliveryIDs = ["d_{:05d}".format(i) for i in range(0, TOTAL_EMAILS + 1)]

allDelivery = {}

for dID in deliveryIDs:
    allDelivery[dID] = []

allActions = []

def gen_rand_str():
    return b64encode(os.urandom(6))

# Generating data

# for each contact
for contact in contactIDs:
    for j in range(0, 21):
        allActions.append([
            contact,
            random.randint(0,4),
            deliveryIDs[random.randint(0, len(deliveryIDs)-1)],
            random.randint(0, 1000),
            str(random.randint(9999, 99999999))
        ])

columns = ['contactID', 'actionID', 'deliveryID', 'timestamp', 'linkID']

raw_df = pd.DataFrame(columns=columns, data=allActions)
raw_df['timestamp'] = raw_df['timestamp'].apply(lambda t: pd.to_datetime(timedelta(minutes=t) + datetime(2014, 11, 17)))

###### PLOT CONTACT ACTION DATA FOR VISUALS
# derivative work of the following
# https://stackoverflow.com/questions/14885895/color-by-column-values-in-matplotlib
def dfScatter(df, xcol='timestamp', ycol='contactID', catcol='actionID'):
    fig, ax = plt.subplots()
    categories = np.unique(df[catcol])
    colors = np.linspace(0, 1, len(categories))
    colordict = dict(zip(categories, colors))

    df["Color"] = df[catcol].apply(lambda x: colordict[x])
    ax.scatter(df[xcol].tolist(), df[ycol].tolist(), c=df.Color,marker='|')
    ax.set_xlim([date(2014, 11, 17), date(2014, 11, 18)])
    ax.yaxis.set_ticklabels([])
    ax.set_ylabel("Contacts")
    # legend_elements = [Line2D([0], [0], color='b', lw=4, label='Line'),
    #                    Line2D([0], [0], marker='o', color='w', label='Scatter',
    #                           markerfacecolor='g', markersize=15)]
    legend_elements = [Line2D([0], [0], marker='o', # color=v[1],
                              label=c) for c in categories]
    ax.legend(handles=legend_elements)
    fig.autofmt_xdate()
    ax.set_title('Contact Action Timeline')
    ax.yaxis.grid(True)
    return fig


fig = dfScatter(raw_df, xcol='timestamp', ycol='contactID', catcol='actionID')
fig.savefig('fig1.png')
fig.show()

###### DATA GENERATOR ENDS HERE

###### FEATURE EXTRACTION STARTS HERE!!!

feature_df = pd.DataFrame()

# Add a column for the new feature.
# When you call groupby, you are forking the execution of how the data is processed. In this case, we are grouping
# by contactID, selecting the 'timestamp' column, and running some function for each series of timestamps.
feature_df['lifespan'] = raw_df.groupby('contactID')['timestamp'].apply(lambda x: x.max() - x.min())

# feature_df['avg_num_actions_per_email'] = raw_df.groupby('contactID').apply(lambda cdf: cdf.groupby('deliveryID'))

#pipeline

# mapper_df = skpd.DataFrameMapper(feature_df)
#
# anova_filter = SelectKBest(f_regression, k=5)
# clf = svm.SVC(kernel='linear')
#
# svm_pipeline = Pipeline([
#     ('feature_input', mapper_df),
#     ('feature_selection_anova', anova_filter),
#     ('svc', clf)
# ])
#
# svm_pipeline.set_params(anova__k=10, svc__C=.1)
#
# svm_pipeline.fit(X_training, y_train_labels)
#
# svm_pipeline.fit_predict(X_testing, y_test_labels)

#
# FeatureUnion()