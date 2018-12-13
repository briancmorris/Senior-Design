from littlefoot import frameworkRunner
from feature_extraction.links_clicked import TotalLinksClicked
from sklearn.ensemble import AdaBoostClassifier
class TestFreqEmails(object):
  def test_framework(self):
    filename = 'medium_dataset_raw.csv'
    features = [('Total Links Clicked', TotalLinksClicked())]
    output = frameworkRunner(features, AdaBoostClassifier, filename, './Fullstack/server/Data/')
    '''
      To test the framework, we check the correct keys exists, because testing the values 
      will not work because they will be different at each run
    '''
    assert output[0][0] == 'fit_time'
    assert output[1][0] == 'score_time'
    assert output[2][0] == 'test_accuracy'
    assert output[3][0] == 'train_accuracy'
    assert output[4][0] == 'test_precision'
  