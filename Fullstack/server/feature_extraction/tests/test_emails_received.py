import pandas as pd
from feature_extraction import recv

class TestEmailsReceived(object):
    def test_received(self):
        test_df = pd.read_csv('./test_files/test_emails_received.csv',
                              dtype={'actionID': 'float'}, parse_dates=['timestamp'])
        fe_emails_received = recv.EmailsReceivedTransformer()
        trans_df = fe_emails_received.transform(test_df)

        exp_received = {'c_00001': '1', 'c_00002': '0', 'c_00003': '1'}
        i = 0
        for key in exp_received:
            assert exp_received[key] == str(trans_df.iloc[i, 0])
            i += 1
