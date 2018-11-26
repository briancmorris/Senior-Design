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

###### DATA GENERATOR STARTS HERE

class Action(Enum):
    EMAIL_VIEW_LINK = 0
    EMAIL_WEBFORM_UNSUB = 1
    EMAIL_WEBFORM_FTAF = 2
    EMAIL_WEBFORM_VIEW = 3


random.seed(42)
#
contactIDs = [str(i) for i in range(0, 11)]
deliveryIDs = [str(i) for i in range(20, 31)]

allActions = []

# for each contact
for contact in contactIDs:
    for j in range(0, 11):
        allActions.append([
            contact,
            random.randint(0,4),
            deliveryIDs[random.randint(0, len(deliveryIDs)-1)],
            random.randint(0, 300),
            str(random.randint(9999, 99999999))
        ])

columns = ['contactID', 'actionID', 'deliveryID', 'timestamp', 'linkID']

raw_df = pd.DataFrame(columns=columns, data=allActions)

###### DATA GENERATOR ENDS HERE

###### FEATURE EXTRACTION STARTS HERE!!!

feature_df = pd.DataFrame(columns=['contactID'])

# Add a column for the new feature.
# When you call groupby, you are forking the execution of how the data is processed. In this case, we are grouping
# by contactID, selecting the 'timestamp' column, and running some function for each series of timestamps.
feature_df['lifespan'] = raw_df.groupby('contactID')['timestamp'].apply(lambda x: x.max() - x.min())
feature_df['avg_num_actions_per_email'] = raw_df.groupby('contactID').apply(lambda cdf: cdf.groupby('deliveryID'))

# anova_filter = SelectKBest(f_regression, k=5)
# clf = svm.SVC(kernel='linear')
#
# svm_pipeline = Pipeline([
#     ('features', extract_feature_avg_contact_time),
#     ('feature_selection_anova', anova_filter),
#     ('svc', clf)
# ])
# svm_pipeline.set_params(anova__k=10, svc__C=.1).fit(X, y)
#
# svm_pipeline.fit(X_training, y_train_labels)
#
# svm_pipeline.fit_predict(X_testing, y_test_labels)
#
#
# FeatureUnion()