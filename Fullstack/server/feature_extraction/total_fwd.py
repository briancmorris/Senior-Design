from sklearn.base import TransformerMixin
import pandas as pd
from datetime import datetime
from action_types import ActionEnum
import numpy as np
from datetime import datetime


class FETotalForwarded(TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """
        Transforms the web log data into contacts and their total number of emails forwarded
        :param X: the raw web log data
        :return: the contacts and their associated number of emails forwarded
        """
        assert(isinstance(X, pd.DataFrame))

        per_contact_groupby = X.groupby('contactID')
        # passes unit test but does not work from front-end
        Xz = per_contact_groupby.apply(lambda contact: np.sum(contact['actionID'] == str(float(ActionEnum.FORWARD_FRIEND.value))))

        return Xz
