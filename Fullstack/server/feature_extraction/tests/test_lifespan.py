import pandas as pd
from pathlib import Path
from feature_extraction import lifespan

class TestLifespan(object):
    def test_lifespan(self):
        # Path generates an os agnostic path for the tests to be reached
        test_folder = Path('./Fullstack/server/feature_extraction/tests/test_files')
        test_file = test_folder / 'test_lifespan.csv'

        test_df = pd.read_csv(test_file, parse_dates=['timestamp'])
        fe_lifespan = lifespan.LifespanTransformer()
        trans_df = fe_lifespan.transform(test_df)

        exp_life = {'c_00001': '0 days 00:01:00', 'c_00002': '7 days 00:05:00', 'c_00003': '14 days 00:06:00'}
        i = 0
        for key in exp_life:
            assert exp_life[key] == str(trans_df.iloc[i, 0])
            i = i + 1
