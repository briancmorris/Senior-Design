import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin
from datetime import datetime
import pandas as pd

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


def calculateEmailFrequency(contact, emails):
    """
    Calculates the frequency at which each contact received emails
    :param contact: the data frame grouped by contact
    :param emails: the log of emails sent to each contact
    :return: the frequency in emails/sec that the contact received emails
    """
    lifespan = contact['timestamp'].max() - contact['timestamp'].min()
    total_emails_recv = countEmailsReceived(contact, emails)
    try:
        # frequency is currently emails/sec
        return total_emails_recv / lifespan.total_seconds()
    except ZeroDivisionError:
        return np.nan


class EmailFrequencyFeatureTransformer(TransformerMixin):
    # FunctionTransformer but for pandas DataFrames

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """
        Transforms the web log data into contact-wise data with their associated email frequency
        :param X: the web log data
        :return: each contact and the frequency at which they received emails
        """
        Xt = pd.DataFrame()
        emails = X[X.contactID.isna()]
        Xt['email frequency'] = X.groupby('contactID').apply(lambda c: calculateEmailFrequency(c, emails))
        return Xt


if __name__ == "__main__":
    # Pandas read_csv attempts to parse columns as string, int, or float.
    # In this case, all columns are by default parsed as string.
    # actionID must be parsed as float because of NaN values.
    # timestamp converted to datetime64. Must specify 'timestamp' column so read_csv knows which columns to concatenate.
    raw_df = pd.read_csv('medium_dataset_raw.csv', dtype={'actionID': 'float'}, parse_dates=['timestamp'])
    fe_freq = EmailFrequencyFeatureTransformer()
    output = fe_freq.transform(raw_df)
