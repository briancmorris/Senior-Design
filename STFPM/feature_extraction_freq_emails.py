import pandas as pd
from sklearn.base import TransformerMixin

def calculateEmailFrequency(contact):
    lifespan = contact['timestamp'].max() - contact['timestamp'].max()
    total_emails = contact['emailID'].unique().size
    return total_emails/lifespan

class EmailFrequencyFeatureTransformer(TransformerMixin):
    # FunctionTransformer but for pandas DataFrames

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        Xt = pd.DataFrame()
        Xt['email frequency'] = X.groupby('contactID').apply(calculateEmailFrequency)
        return Xt
