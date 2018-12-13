import pandas as pd
from sklearn.base import TransformerMixin
from action_types import ActionEnum


class TotalLinksClicked(TransformerMixin):
    def transform(self, X):
        """
        Transforms the raw web log data to contacts and the total number of links they have clicked
        :param X: the raw web log data of contact actions
        :return: the contacts and their associated number of links clicked
        """
        assert(isinstance(X, pd.DataFrame))
        # make X consist only of link clicks and forwards aka opens
        X = X[X.actionID == float(ActionEnum.VIEW_LINK.value)]


        return X.groupby('contactID').apply(lambda cdf: cdf['actionID'].count())

    def fit(self):
        return self
