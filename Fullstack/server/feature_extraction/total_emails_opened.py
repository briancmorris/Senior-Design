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
        original_contacts = set(X.contactID.unique())
        original_contacts = {c for c in original_contacts if pd.notna(c)}

        # make X consist only of link clicks and forwards aka opens
        X = X[(X.actionID == float(ActionEnum.VIEW_LINK.value)) | (X.actionID == float(ActionEnum.FORWARD_FRIEND.value))]

        # make a DataFrame to contain the contacts, then counts the unique emails the interacted with,
        # specified by the masking above with clicks and forwards
        Xo = pd.DataFrame()
        Xo['emails_opened'] = X.groupby('contactID').apply(lambda c: c['emailID'].unique().size)

        contacts_with_actions = set(Xo.index.unique())
        if len(contacts_with_actions) < len(original_contacts):
            for contact in original_contacts - contacts_with_actions:
                # assign 0 emails opened to contacts who have not interacted with emails
                idx = pd.Index(name='contactID', data=[contact])
                c = pd.DataFrame({'emails_opened':pd.Series([0], dtype='int', index=idx)})
                Xo = Xo.append(c)

        return Xo
