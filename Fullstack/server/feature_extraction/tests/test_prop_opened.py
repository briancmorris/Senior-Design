import pandas as pd
import math
from feature_extraction import prop_opened

class TestPropOpened(object):
    def test_prop_opened(self):
        test_df = pd.read_csv('./test_files/test_prop_opened.csv', parse_dates=['timestamp'])
        fe_prop_opened = prop_opened.PropOpenedTransformer()
        trans_df = fe_prop_opened.transform(test_df)

        print(trans_df)

        exp_prop = {'c_00001': '0.6666666667', 'c_00002': '1', 'c_00003': '0'}
        i = 0
        for key in exp_prop:
            assert math.isclose(float(exp_prop[key]), float(trans_df.iloc[i, 0]), rel_tol=1e-3, abs_tol=0)
            i = i + 1
