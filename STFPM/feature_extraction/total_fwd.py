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
        Xz = per_contact_groupby.apply(lambda contact:
                                       contact['actionID']
                                       .filter(like=str(ActionEnum.FORWARD_FRIEND.value))
                                       .count())
        return Xz


if __name__ == "__main__":
    # Pandas read_csv attempts to parse columns as string, int, or float.
    # In this case, all columns are by default parsed as string.
    # actionID must be parsed as float because of NaN values.
    # timestamp converted to datetime64. Must specify 'timestamp' column so read_csv knows which columns to concatenate.
    raw_df = pd.read_csv('medium_dataset_raw.csv', dtype={'actionID': 'float'}, parse_dates=['timestamp'])
    fe_total_forward = FETotalForwarded()
    output = fe_total_forward.fit_transform(raw_df)
