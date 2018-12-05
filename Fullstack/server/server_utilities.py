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

framework = littlefoot
