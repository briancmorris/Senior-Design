from datetime import timedelta, datetime

import pandas as pd
import numpy as np

from typing import List

from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split, cross_validate
from sklearn import ensemble

from action_types import ActionEnum
from feature_extraction.links_clicked import TotalLinksClicked
from feature_extraction.total_fwd import FETotalForwarded

class LabelledPoint:
    def __init__(self, label, features: List):
        self.label = label
        self.features = features


def getContactsForExperiment(df: pd.DataFrame, numContacts: int, percentChurnedOut: float) -> List[pd.DataFrame]:
    result = []

    # only keep rows for contact actions
    df = df[df.contactID.notna()]

    # calculate goal numbers for churned and still subscribed contacts
    goalChurn = int(numContacts * percentChurnedOut)
    goalSub = int(numContacts - goalChurn)

    # make a data frame out of all unsubscribe actions
    churned_df = df[df['actionID'] == float(ActionEnum.UNSUBSCRIBE.value)]
    if len(churned_df) < goalChurn:
        raise Exception('Not enough churned contacts in data set to meet goal')

    # take the first of as many churned contacts as is desired
    churn_contacts = churned_df.head(goalChurn).contactID

    # get list of contact IDs who did not unsubscribe in window
    sub_contacts = list(set(df.contactID.unique()) - set(churned_df.contactID.unique()))
    if len(sub_contacts) < goalSub:
        raise Exception('Not enough subscribed contacts in data set to meet goal, will censor churned contacts')
        # could do censoring here
    else:
        # select first as many still subscribed contacts as is desired
        sub_contacts = sub_contacts[:goalSub]

    # if a contact has EVER unsubscribed, they are considered churn
    for contact in churn_contacts:
        result.append(df.loc[df['contactID'] == contact].drop(columns=['Unnamed: 0']))

    for contact in sub_contacts:
        result.append(df.loc[df['contactID'] == contact].drop(columns=['Unnamed: 0']))

    # return list of data frames, each is for a contact
    return result


def getLabelledPointsFromContacts(input: List[pd.DataFrame], percentChurnedOut: float, featuresSelected) -> List[LabelledPoint]:
    # input dataframe is a list of data frames
    # each dataframe represents a list of user actions (each with a timestamp)

    # transformation requires sampling "dates" in each contact time line
    #   for each date sampled, it represents a labelled point
    #   this takes in arguments for checking

    # output is a list of extracted labelled points
    #   a single contact may provide multiple labelled points
    result = []

    # tlc = TotalLinksClicked()
    # tf = FETotalForwarded()
    # features_to_be_extracted = [('links_clicked', tlc)]
    # print(features_to_be_extracted)

    # print(featuresSelected)

    for df in input:
        # mask each df to only last month of activity
        df = df[(df['timestamp'] > df['timestamp'].max() - pd.DateOffset(months=1))]

        # check if current data frame contains an unsubscribe action
        label_churn = (1, 0)[float(ActionEnum.UNSUBSCRIBE.value) in df.actionID.values]
        features = [] # {} to make a dictionary
        for f in featuresSelected:
            # print(f[1].transform(df).iloc[0])
            # builds a features DICTIONARY
            # features[f[0]] = f[1].transform(df).iloc[0]

            # make a list of features
            features.append(f[1].transform(df).iloc[0])
        result.append(LabelledPoint(label_churn, features))

    # return list of labelled points
    # should retain correct ratio of churn/non-churn points
    return result


def transformLabelledPointsToDataFrame(points: List[LabelledPoint]) -> pd.DataFrame:
    """
        Transforms a list of N labelled points into an NxN pandas data frame. The first column has the label of the point.
        Col_1 to Col_n holds extracted feature data. An example data frame has been illustrated below.

        df:
        Label    Feat_1   Feat_2  ...    Feat_n
        Label_1  Feat_11  Feat_12 ...    Feat_1n
        ...      ...      ...     ...    ...
        Label_n  Feat_n1 Feat_n2  ...    Feat_nn

        NOTE: This function does not error check the data contained within the labelled points, this should be done
        wherever the list is built.

        :param points: the list of labelled data points
        :return: a pandas data frame representing the provided list of labelled points
        """
    # Get the length of the feature vector.
    len_features = len(points[0].features)

    # 2D array containing individual labelled point data in an array representation.
    # i.e. [[Label_1, Feat_11, ..., Feat_1n], [Label_2, Feat_21, ..., Feat2n], ...]
    array = []

    # For every labelled point, represent it as a 1D array.
    for point in points:
        # Start with the label.
        point_as_array = [point.label]
        # Then add all of the feature data.
        for i in range(len_features):
            point_as_array.append(point.features[i])
        # Append the 1D array to the 2D array.
        array.append(point_as_array)

    # Convert 2D array to a numpy array, used to construct pandas data frame.
    array = np.array(array)

    # Column names for pandas data frame: ['Label', 'Feature_1', ..., 'Feature_n'].
    columns = ['Label']
    for n in range(len_features):
        columns.append('Feat_' + str(n + 1))

    # Convert 2D array and column names to pandas data frame. NOTE: don't forget the 'columns=' portion.
    df = pd.DataFrame(array, columns=columns)

    # Return the data frame.
    return df

def frameworkRunner(featuresSelected, filename) :
    input_dataframe = pd.read_csv("./Data/" + filename, dtype={'actionID': 'float'}, parse_dates=['timestamp'])
    # doing .head(200) causes us to lose valuable info such as unsubscribe actions
    # input_dataframe = input_dataframe.head(200)

    percentChurnOut = 0.5

    listContactTimelines = getContactsForExperiment(input_dataframe, 16, percentChurnOut)
    listLabelledPoints = getLabelledPointsFromContacts(listContactTimelines, percentChurnOut, featuresSelected)
    feature_df = transformLabelledPointsToDataFrame(listLabelledPoints)

    num_features = feature_df.shape[1]

    # TODO: need to figure out how to do this masking without using column headers
    # int indices were not working at first might require indexing into columns name list to generate mask
    X = feature_df.loc[:, 'Feat_1':]
    y = feature_df.loc[:, :'Label']

    # changes shape of y from column vector to 1d array
    y = y.values.ravel()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    abc = ensemble.AdaBoostClassifier()
    # abc.fit(X_train, y_train)
    # abc.score(X_train, y_train)
    # by default performs StratifiedKFold CV
    metrics = ["accuracy", "precision", "recall", "f1"]
    results = cross_validate(abc, X, y, cv=5, scoring=metrics)

    modified_results = [(k,np.mean(v)) for k,v in results.items()]
    return modified_results
    # print(cross_val_score(abc, X, y, cv=5))


# if __name__ == "__main__":

#     input_dataframe = pd.read_csv("./Data/medium_dataset_raw.csv", dtype={'actionID': 'float'}, parse_dates=['timestamp'])
#     # doing .head(200) causes us to lose valuable info such as unsubscribe actions
#     # input_dataframe = input_dataframe.head(200)

#     percentChurnOut = 0.5

#     listContactTimelines = getContactsForExperiment(input_dataframe, 16, percentChurnOut)
#     listLabelledPoints = getLabelledPointsFromContacts(listContactTimelines, percentChurnOut)
#     feature_df = transformLabelledPointsToDataFrame(listLabelledPoints)

#     num_features = feature_df.shape[1]

#     # TODO: need to figure out how to do this masking without using column headers
#     # int indices were not working at first might require indexing into columns name list to generate mask
#     X = feature_df.loc[:, 'Feat_1':]
#     y = feature_df.loc[:, :'Label']

#     # changes shape of y from column vector to 1d array
#     y = y.values.ravel()

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#     abc = ensemble.AdaBoostClassifier()
#     # abc.fit(X_train, y_train)
#     # abc.score(X_train, y_train)
#     # by default performs StratifiedKFold CV
#     metrics = ["accuracy", "precision", "recall", "f1"]
#     results = cross_validate(abc, X, y, cv=5, scoring=metrics)
#     # print(cross_val_score(abc, X, y, cv=5))
