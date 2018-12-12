from feature_extraction.freq_emails import EmailFrequencyFeatureTransformer
from feature_extraction.lifespan import LifespanTransformer
from feature_extraction.links_clicked import TotalLinksClicked
from feature_extraction.prop_opened import PropOpenedTransformer
from feature_extraction.recv import EmailsReceivedTransformer
from feature_extraction.total_emails_opened import EmailsOpenedTransformer
from feature_extraction.total_fwd import FETotalForwarded
import littlefoot


features = {
  'Email Frequency': EmailFrequencyFeatureTransformer, 
  'Lifespan': LifespanTransformer,
  'Total Links Clicked': TotalLinksClicked,
  'Props Opened': PropOpenedTransformer,
  'Emails Recieved': EmailsReceivedTransformer,
  'Emails Opened': EmailsOpenedTransformer,
  'Total Emails Forwarded': FETotalForwarded
  }

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

models = {
  'adaboost': AdaBoostClassifier,
  'svc': SVC,
  'knn': KNeighborsClassifier,
  'mlp': MLPClassifier,
  'decision_tree': DecisionTreeClassifier,
  'random_forest': RandomForestClassifier,
  'gaussian_naive_bayes': GaussianNB,
  'quad_disc_analysis': QuadraticDiscriminantAnalysis,
}

framework = littlefoot
