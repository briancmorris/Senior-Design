from datetime import timedelta, datetime

import pandas as pd
import numpy as np

from typing import List

from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split, cross_validate
from sklearn import ensemble

from action_types import ActionEnum

class LabelledPoint:
    def __init__(self, label, features: List):
        self.label = label
        self.features = features


def getContactsForExperiment(df: pd.DataFrame, numContacts: int, percentChurnedOut: float) -> List[pd.DataFrame]:
    """
    Selects the contacts from the dataset that will be used for the experiment

    :param df: the weblog format of all contacts' actions
    :param numContacts: the total number of contacts desired for the experiment
    :param percentChurnedOut: the percentage of contacts selected who should be churned out
    this helps prevent the model from being trained with too many or too few churned contacts
    :return: a list of selected contacts as individual data frames
    """

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
    else:
        # take the first of as many churned contacts as is desired
        churn_contacts = churned_df.head(goalChurn).contactID

    # get list of contact IDs who did not unsubscribe in window
    sub_contacts = list(set(df.contactID.unique()) - set(churned_df.contactID.unique()))
    if len(sub_contacts) < goalSub:
        # could do censoring here
        raise Exception('Not enough subscribed contacts in data set to meet goal, will censor churned contacts')
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


def getLabelledPointsFromContacts(input: List[pd.DataFrame], featuresSelected, email_df) -> List[LabelledPoint]:
    """
    Transforms a list of contact data frames into a list of labelled points for their past month of data
    A labelled point corresponds to a single contact with its features extracted and a label added
    The label is a 1 if the user has unsubscribed or 0 if they are still subscribed

    :param input: the list of contact data frames
    :param featuresSelected: a list of feature extraction objects to be applied to the data
    :return: a list of labelled points of contact actions
    """

    result = []

    for df in input:
        # mask each df to only last 3 months of activity
        df = df[(df['timestamp'] > df['timestamp'].max() - pd.DateOffset(months=3))]
        df = df.append(email_df)

        # check if current data frame contains an unsubscribe action
        label_churn = (1, 0)[float(ActionEnum.UNSUBSCRIBE.value) in df.actionID.values]
        features = []
        for f in featuresSelected:
            # make a list of features
            features.append(f[1].transform(df).iloc[0])

        result.append(LabelledPoint(label_churn, features))

    # return list of labelled points, should retain correct ratio of churn/non-churn points
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


def frameworkRunner(featuresSelected, modelSelected, filename, fileroot="./Data/", percentChurnOut=0.5, numContacts=50) :
    """
        Runs the framework based on the features to be extracted and the file uploaded
        :param featuresSelected: a list of feature extraction objects to be applied to the data
        :param modelSelected: the model selected on the front-end
        :param filename: the file that contains the weblog data of contact actions
        :param fileroot: needed to test the function, but can also point the framework to different file locations
        :param percentChurnOut: desired percentage of contacts who have churned out in the dataset
        :param numContacts: desired number of contacts to be used in the dataset
        :return: the model scoring metrics
    """
    input_dataframe = pd.read_csv(fileroot + filename, dtype={'actionID': 'float'}, parse_dates=['timestamp'])

    email_df = input_dataframe[input_dataframe.contactID.isna()]

    listContactTimelines = getContactsForExperiment(input_dataframe, numContacts, percentChurnOut)
    listLabelledPoints = getLabelledPointsFromContacts(listContactTimelines, featuresSelected, email_df)
    feature_df = transformLabelledPointsToDataFrame(listLabelledPoints)

    X = feature_df.loc[:, 'Feat_1':]
    y = feature_df.loc[:, :'Label']

    # changes shape of y from column vector to 1d array
    y = y.values.ravel()

    # This is one way to do the test train split
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    abc = modelSelected()
    # abc.fit(X_train, y_train)
    # abc.score(X_train, y_train)
    # by default performs StratifiedKFold CV
    metrics = ["accuracy", "precision", "recall", "f1"]
    results = cross_validate(abc, X, y, cv=5, scoring=metrics)

    modified_results = [(k,np.mean(v)) for k,v in results.items()]
    return modified_results
