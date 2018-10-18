# Peter Girouard
# 17 October 2018

import pandas as pd
from datetime import *
from sklearn.base import TransformerMixin


def datetime_to_float(dt):
    return (dt - datetime(1970, 1, 1)).total_seconds()


class LifespanTransformer(TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        # stateless transformer
        return self

    def transform(self, X):
        assert isinstance(X, pd.DataFrame)
        feature_df = pd.DataFrame()
        feature_df['lifespan'] = X.groupby('contactID')['timestamp'].apply(lambda x: x.max() - x.min())
        return feature_df

if __name__ == "__main__":
    # Pandas read_csv attempts to parse columns as string, int, or float.
    # In this case, all columns are by default parsed as string.
    # actionID must be parsed as float because of NaN values.
    # timestamp converted to datetime64. Must specify 'timestamp' column so read_csv knows which columns to concatenate.
    raw_df = pd.read_csv('medium_dataset_raw.csv', dtype={'actionID': 'float'}, parse_dates=['timestamp'])
    fe_lifespan = LifespanTransformer()
    output = fe_lifespan.transform(raw_df)
