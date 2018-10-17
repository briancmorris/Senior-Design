import pandas as pd
from sklearn.base import TransformerMixin
from magnum_datagen import Action

def calculateEmailsOpened(contact):
    return contact['actionID'].filter(Action.OPEN.value).unique().count()

class EmailsOpenedFeatureTransformer(TransformerMixin):
    # FunctionTransformer but for pandas DataFrames

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        Xt = pd.DataFrame()
        Xt['emails opened'] = X.groupby('contactID').apply(calculateEmailsOpened)
        return Xt
