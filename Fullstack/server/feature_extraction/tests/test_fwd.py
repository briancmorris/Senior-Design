import pandas as pd
from action_types import ActionEnum
from pathlib import Path
from feature_extraction import total_fwd

class TestEmailsForwarded(object):
    def test_emails_forwarded(self):
        # Path generates an os agnostic path for the tests to be reached
        test_folder = Path('./Fullstack/server/feature_extraction/tests/test_files')
        test_file = test_folder / 'test_fwd.csv'

        test_df = pd.read_csv(test_file, dtype={'actionID': 'str'}, parse_dates=['timestamp'])
        fe_emails_fwd = total_fwd.FETotalForwarded()
        trans_df = fe_emails_fwd.transform(test_df)

        exp_fwd = {'c_00001': '4', 'c_00002': '2', 'c_00003': '0'}
        i = 0
        for key in exp_fwd:
            assert exp_fwd[key] == str(trans_df.iloc[i])
            i = i + 1
