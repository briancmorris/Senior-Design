# Peter Girouard
# 17 October 2018

import pandas as pd
import datetime
from sklearn.base import TransformerMixin

def countEmailsReceived(contact, emails):
    """
    Counts the total number of emails received by a contact in their lifespan
    :param contact: the data frame grouped by contact
    :param emails: the log emails sent to each contact
    :return: the number of unique emailIDs over the lifetime of a contact
    """
    contact_start = contact['timestamp'].min()
    contact_end = contact['timestamp'].max()
    emails = emails[emails.timestamp.between(str(contact_start), str(contact_end))]
    return emails['emailID'].unique().size

class EmailsReceivedTransformer(TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        # stateless transformer
        return self

    def transform(self, X):
        """
        Transforms the web log data into contacts and the number of emails they have received
        :param X: the incoming raw web log data
        :return: the contacts and their associated number of emails received
        """
        assert(isinstance(X, pd.DataFrame))
        # sort by timestamp
        df = X.sort_values(by='timestamp', ascending=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # make a DataFrame only containing the emails sent
        email_df = df[df.contactID.isna()]
        recv_df = pd.DataFrame()
        recv_df['emails_recv'] = df.groupby('contactID').apply(lambda c: countEmailsReceived(c, email_df))

        return recv_df

if __name__ == "__main__":
    # Pandas read_csv attempts to parse columns as string, int, or float.
    # In this case, all columns are by default parsed as string.
    # actionID must be parsed as float because of NaN values.
    # timestamp converted to datetime64. Must specify 'timestamp' column so read_csv knows which columns to concatenate.
    raw_df = pd.read_csv('medium_dataset_raw.csv', dtype={'actionID': 'float'}, parse_dates=['timestamp'])
    fe_received = EmailsReceivedTransformer()
    output = fe_received.transform(raw_df)