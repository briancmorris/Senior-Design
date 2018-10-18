# Peter Girouard
# 17 October 2018

import pandas as pd
import datetime
from sklearn.base import TransformerMixin


def datetime_to_float(dt):
    return (dt - datetime(1970, 1, 1)).total_seconds()


class EmailReceivedTransformer(TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        # stateless transformer
        return self

    def transform(self, X):
        assert(isinstance(X, pd.DateFrame))
        # sort by timestamp
        df = X.sort_values(by='timestamp', ascending=True)
        df['timestamp'] = df['timestamp'].apply(lambda t: datetime_to_float(pd.to_datetime(t)))
        recv_df = pd.DataFrame()
        recv_df['contact_start'] = df.groupby('contactID')['timestamp'].apply(lambda x: x.min())
        recv_df['contact_end'] = df.groupby('contactID')['timestamp'].apply(lambda x: x.max())

        # make a DataFrame only containing the emails sent
        email_df = df[df.contactID.isna()]
        recv_df['emails_recv'] = -1 #need to run through recv_df and count the number of emails in
                                    # email_df between contacts start and end dates
        return -1
