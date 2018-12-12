import pandas as pd
from pathlib import Path
from feature_extraction import links_clicked


class TestLinksClicked(object):
    def test_links_clicked(self):
        """
        Tests the feature extractor "links_clicked.py" for completeness and correctness.
        """
        # Path generates an os agnostic path for the tests to be reached
        test_folder = Path('./Fullstack/server/feature_extraction/tests/test_files')
        test_file = test_folder / 'test_links_clicked.csv'

        test_df = pd.read_csv(test_file, dtype={'actionID': 'float'}, parse_dates=['timestamp'])
        fe_links_clicked = links_clicked.TotalLinksClicked()
        trans_df = fe_links_clicked.transform(test_df)

        exp_clicked = {'c_00001': '1', 'c_00002': '2', 'c_00003': '3'}
        i = 0
        for key in exp_clicked:
            assert exp_clicked[key] == str(trans_df.iloc[i])
            i = i + 1
