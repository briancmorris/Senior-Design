import pandas as pd
from action_types import ActionEnum
from feature_extraction import total_fwd

class TestEmailsForwarded(object):
    def test_emails_forwarded(self):
        test_df = pd.read_csv('./test_files/test_fwd.csv', dtype={'actionID': 'str'}, parse_dates=['timestamp'])
        fe_emails_fwd = total_fwd.FETotalForwarded()
        trans_df = fe_emails_fwd.transform(test_df)

        print(test_df)
        # print(test_df['contactId' == 'c_00001']['actionID'].filter(like=str(ActionEnum.FORWARD_FRIEND.value)))
        print(trans_df)

        exp_fwd = {'c_00001': '4', 'c_00002': '2', 'c_00003': '0'}
        i = 0
        for key in exp_fwd:
            assert exp_fwd[key] == str(trans_df.iloc[i])
            i = i + 1
