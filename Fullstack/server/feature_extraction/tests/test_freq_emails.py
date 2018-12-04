import pandas as pd
import math
from feature_extraction import freq_emails

class TestFreqEmails(object):
    def test_freq_emails(self):
        test_df = pd.read_csv('./test_files/test_freq_emails.csv', parse_dates=['timestamp'])
        fe_freq_emails = freq_emails.EmailFrequencyFeatureTransformer()
        trans_df = fe_freq_emails.transform(test_df)

        exp_freq = {'c_00001': '0.01666667', 'c_00002': '0', 'c_00003': '0.0000008264757'}
        i = 0
        for key in exp_freq:
            assert math.isclose(float(exp_freq[key]), float(trans_df.iloc[i, 0]), rel_tol=1e-3, abs_tol=0)
            i = i + 1
