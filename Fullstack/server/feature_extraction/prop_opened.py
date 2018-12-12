import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin
from action_types import ActionEnum


def countEmailsReceived(contact, emails):
    """
    Counts the number of emails received by a contact
    :param contact: the grouped contact data frame
    :param emails: the emails data frame
    :return: the number of emails received
    """
    contact_start = contact['timestamp'].min()
    contact_end = contact['timestamp'].max()
    emails = emails[emails.timestamp.between(str(contact_start), str(contact_end))]
    return emails['emailID'].unique().size


def countEmailsOpened(contact):
    """
    Counts the number of emails opened by a contact, by seeing if they have any action associated with it
    :param contact: the grouped contact data frame
    :return: the number of unique emails that the contact interacted with
    """
    return contact.emailID.unique().size

class PropOpenedTransformer(TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        # stateless transformer
        return self

    def transform(self, X):
        """
        Transforms the data frame passed to one with contacts and their proportion of emails opened
        :param X: The web log data frame
        :return: a data frame with contacts and their proportion of emails opened
        """
        assert(isinstance(X, pd.DataFrame))
        # sort by timestamp
        X = X.sort_values(by='timestamp', ascending=True)
        X['timestamp'] = pd.to_datetime(X['timestamp'])

        # make DataFrame for emails only
        email_df = X[X.contactID.isna()]
        # count emails received
        Xp = pd.DataFrame()
        Xp['emails_recv'] = X.groupby('contactID').apply(lambda c: countEmailsReceived(c, email_df))

        # make X consist only of link clicks and forwards aka opens
        X = X[(X.actionID == float(ActionEnum.VIEW_LINK.value)) | (X.actionID == float(ActionEnum.FORWARD_FRIEND.value))]
        Xp['emails_open'] = X.groupby('contactID').apply(lambda c: countEmailsOpened(c))
        Xp['prop_opened'] = Xp['emails_open'] / Xp['emails_recv']

        Xp = Xp.drop(['emails_recv', 'emails_open'], axis=1)
        Xp.fillna(0, inplace=True)

        return Xp
