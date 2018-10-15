# Peter Girouard
# 15 October 2018

# Create a pipeline that standardizes the data then creates a model
import pandas as pd
from pandas import read_csv
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from datetime import *

def datetime_to_float(dt):
    return (dt - datetime(1970, 1, 1)).total_seconds()

# load data
df = read_csv("medium_dataset_raw.csv")
df['timestamp'] = df['timestamp'].apply(lambda t: datetime_to_float(pd.to_datetime(t)))
# remove rows where email is sent, no contact associated
df = df[df.contactID.notnull()]

# feature extraction
feature_df = pd.DataFrame()
feature_df['lifespan'] = df.groupby('contactID')['timestamp'].apply(lambda x: x.max() - x.min())
feature_df['actions_per_email'] = df.groupby(['contactID']).apply(lambda cdf: cdf['actionID'].count() / cdf['emailID'].unique().size)

array = feature_df.values
X = array[:,1].reshape(-1, 1)
Y = array[:,0]

# create feature union
#features = []
#features.append(('pca', PCA(n_components=3)))
#features.append(('select_best', SelectKBest(k=6)))
#feature_union = FeatureUnion(features)

# create pipeline
estimators = []
#estimators.append(('feature_union', feature_union))
estimators.append(('logistic', LogisticRegression()))
model = Pipeline(estimators)

# evaluate pipeline
seed = 42
kfold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(model, X, Y, cv=kfold)
print(results.mean())