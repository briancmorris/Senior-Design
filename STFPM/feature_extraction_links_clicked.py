import pandas as pd
from sklearn.base import TransformerMixin
from magnum_datagen import Action

LINK_CLICKED_ID = 2


class TotalLinksClicked(TransformerMixin):
    def transform(self, X):
        assert(isinstance(X, pd.DataFrame))

        per_contact_group_by = X.groupby('contactID')
        df = per_contact_group_by.apply(lambda cdf:
                                        cdf['actionID']
                                        .filter(Action.VIEW_LINK.value)
                                        .count())
        return df

    def fit(self):
        return self
