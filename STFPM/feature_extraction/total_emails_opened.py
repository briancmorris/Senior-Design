import pandas as pd
from sklearn.base import TransformerMixin
from action_types import ActionEnum


class EmailsOpenedTransformer(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """
        Transforms the web log data into contacts and the number of emails they have opened
        :param X: the raw web log data of all contact actions
        :return: the contacts and their associated number of emails opened
        """
        # make X consist only of link clicks and forwards aka opens
        X = X[(X.actionID == float(ActionEnum.VIEW_LINK.value)) | (X.actionID == float(ActionEnum.FORWARD_FRIEND.value))]

        # make a DataFrame to contain the contacts, then counts the unique emails the interacted with,
        # specified by the masking above with clicks and forwards
        Xo = pd.DataFrame()
        Xo['emails_opened'] = X.groupby('contactID').apply(lambda c: c['emailID'].unique().size)
        return Xo


if __name__ == "__main__":
    # Pandas read_csv attempts to parse columns as string, int, or float.
    # In this case, all columns are by default parsed as string.
    # actionID must be parsed as float because of NaN values.
    # timestamp converted to datetime64. Must specify 'timestamp' column so read_csv knows which columns to concatenate.
    raw_df = pd.read_csv('medium_dataset_raw.csv', dtype={'actionID': 'float'}, parse_dates=['timestamp'])
    fe_opened = EmailsOpenedTransformer()
    output = fe_opened.transform(raw_df)