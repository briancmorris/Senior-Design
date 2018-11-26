import pandas as pd
from feature_extraction import links_clicked

class TestLinksClicked(object):
    def test_links_clicked(self):
        test_df = pd.read_csv('./feature_extraction/tests/test_files/test_links_clicked.csv',dtype={'actionID': 'float'}, parse_dates=['timestamp'])
        fe_links_clicked = links_clicked.TotalLinksClicked()
        trans_df = fe_links_clicked.transform(test_df)

        exp_clicked = {'c_00001': '1', 'c_00002': '2', 'c_00003': '3'}
        i = 0
        for key in exp_clicked:
            print(str(trans_df.iloc[:,0]))
            # assert exp_clicked[key] == str(trans_df.iloc[i,0])
            i = i + 1
