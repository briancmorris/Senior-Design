import pandas as pd
from feature_extraction import total_emails_opened

class TestEmailsOpened(object):
    def test_emails_opened(self):
        test_df = pd.read_csv('./test_files/test_emails_opened.csv', dtype={'actionID': 'float'}, parse_dates=['timestamp'])
        fe_emails_opened = total_emails_opened.EmailsOpenedTransformer()
        trans_df = fe_emails_opened.transform(test_df)

        exp_opened = {'c_00001': '1', 'c_00002': '2', 'c_00003': '0'}
        i = 0
        for key in exp_opened:
            assert exp_opened[key] == str(trans_df.iloc[i]['emails_opened'])
            i = i + 1
