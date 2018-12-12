from feature_extraction.freq_emails import EmailFrequencyFeatureTransformer
from feature_extraction.links_clicked import TotalLinksClicked
from feature_extraction.prop_opened import PropOpenedTransformer
from feature_extraction.recv import EmailsReceivedTransformer
from feature_extraction.total_emails_opened import EmailsOpenedTransformer
from feature_extraction.total_fwd import FETotalForwarded
import littlefoot


features = {
  'Email Frequency': EmailFrequencyFeatureTransformer,
  'Total Links Clicked': TotalLinksClicked,
  'Proportion Opened': PropOpenedTransformer,
  'Emails Received': EmailsReceivedTransformer,
  'Emails Opened': EmailsOpenedTransformer,
  'Total Emails Forwarded': FETotalForwarded
  }

framework = littlefoot
