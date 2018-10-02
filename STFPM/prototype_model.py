# 9/22/2018
# Daniel Karamitrov

# PEP8 style standard
# PEP484 type hinting standard

# import type hinting for PEP484
from typing import List, Dict

# pandas to load dataset
import pandas as pd

# numpy for transpose
import numpy as np

# sklearn for train/test data split
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import r2_score

# global variables, for the demo.
raw_df: pd.DataFrame = None
clean_df: pd.DataFrame = None
features_df: pd.DataFrame = None
blind_df: pd.DataFrame = None
true_features_df: pd.DataFrame = None
blind_features_df: pd.DataFrame = None
contacts = None


def run_model_validate():
    """
    Main function for validating a model.

    Prediction Goal: monspent by lifespan
    Model type: linear regression
    Feature extraction: lifespan, total money spent
    """

    # global variables, for the purpose of demonstration in an interactive environment
    global raw_df, clean_df, features_df, blind_df, true_features_df, blind_features_df, contacts

    # load the raw dataset into a pandas DataFrame
    raw_df = pd.read_csv('small_dataset_raw.csv')

    # clean the dataset. remove log entries with missing information
    clean_df = clean_dataset(raw_df)

    # create a blinded version of the dataset. remove the final action each user took.
    blind_df = blind_dataset(clean_df)

    # transform the dataset via feature extraction
    true_features_df = extract_features(clean_df)
    blind_features_df = extract_features(blind_df)
    contacts = clean_df['contactID'].unique()

    # skip model validation. we are only performing 1 sample for demonstration.
    # sample the contacts
    # X_train, X_test, y_train, y_test = train_test_split(true_features_df['contactID'],
    #                                                     true_features_df['moneySpent'],
    #                                                     test_size=0.33, random_state=0)
    # print("Training on contacts (X):", list(X_train))
    # print("Training on data (Y):", list(y_train))
    #
    # print("Testing on contacts (X):", list(X_test))
    # print("Testing on data (Y):", list(y_test))

    # helper function to reshape a pandas Series to numpy vector
    def series_to_vector(df: pd.DataFrame, column: str):
        return np.reshape(np.array(df[column]), (df[column].size, 1))

    regr = linear_model.LinearRegression()

    # train the model on the blinded data
    # X represents the array of features where each column is a feature.
    X_train = series_to_vector(blind_features_df, 'lifespan')
    # y represents the vector of dependent variables. moneySpent in this demo.
    y_train = series_to_vector(blind_features_df, 'moneySpent')
    regr.fit(X_train, y_train)

    # test the model on the true set (testing contacts)
    X_test = series_to_vector(true_features_df, 'lifespan')
    y_predict = regr.predict(X_test)

    # report the R-squared score
    y_true = series_to_vector(true_features_df, 'moneySpent')
    accuracy = r2_score(y_true, y_predict)

    print("R2 Accuracy = ", accuracy)

    # Done.


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract features (contact lifespan, contact total money spent) and return features
    as columns in a new DataFrame.
    """
    contacts: List[str] = df['contactID'].unique()
    temp: List[Dict] = []

    for c in contacts:
        # get all rows associated with the contact
        contact_df = df[df['contactID'] == c]
        lifespan = contact_df['timestamp'].max() - contact_df['timestamp'].min()
        money_spent = contact_df['moneySpent'].sum()
        temp.append({'contactID': c, 'lifespan': lifespan, 'moneySpent': money_spent})

    return pd.DataFrame(data=temp, columns=['contactID', 'lifespan', 'moneySpent'])


def blind_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Blind the dataset. Remove the last action a user had performed.
    """
    print("Blinding dataset!")

    result = pd.DataFrame(columns=df.columns)

    # blind the dataset on a per-contact basis
    contacts: List[str] = df['contactID'].unique()

    # for each contact, drop the log entry with maximum timestamp value
    # and concatenate it to the returned dataframe
    # TODO: pandas has a more expressive way to drop rows. concatenating here is inefficient.
    for c in contacts:
        a = df[df['contactID'] == c]
        b = a.drop(a['timestamp'].idxmax())
        result = pd.concat([result, b])

    return result


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset by removing illegal observations.
    For this demo, remove rows which have empty contactID, actionID, or timestamp fields.

    Later on, cleaning will involve removing rows where to actionID requires a special attribute to be not null.
    """

    print("Cleaning dataset!")
    # drop row if any of the following attributes are NaN
    attributes = ['contactID', 'actionID', 'timestamp']
    return df.dropna(subset=attributes, how='any')


if __name__ == '__main__':
    run_model_validate()
