
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.ensemble import AdaBoostClassifier
import pandas as pd


from feature_extraction_total_fwd import FETotalForwarded
from feature_extraction_freq_emails import EmailFrequencyFeatureTransformer
from feature_extraction_lifespan import LifespanTransformer
from feature_extraction_links_clicked import TotalLinksClicked
from feature_extraction_recv import EmailsReceivedTransformer

from external.PandasWithScikit import PandasFeatureUnion, PandasTransform


class FuegoFramework:
    def __init__(self, input_file, feature_steps, feature_selection_steps, estimator):
        self._input_file = input_file
        self._feature_steps = feature_steps
        self._feature_selection_steps = feature_selection_steps
        self._estimator = estimator

        # TODO: Check feature, selection, estimator steps are compatible objects and have non-empty names

        self._main_pipeline = Pipeline([
            ('feature_extraction', PandasFeatureUnion(self._feature_steps)),
            ('feature_selection', Pipeline(self._feature_selection_steps)),
            ('estimator', estimator),
        ])

    def perform_validation(self):
        input_dataframe = pd.read_csv(self._input_file, dtype={'actionID': 'float'}, parse_dates=['timestamp'])

        # choose a time window (start date and end date)
        # TODO: add time window start an end to constructor arguments
        # i e pick a subset of actions regardless of contact ID that happened in a date range

        # stage 1 validation, on a per-contact basis
        # sklearn KFold
        # cross_validate(cv=KFold(n=5))
        # X = set of all unique contact IDs
        splitter = KFold(n=5)
        for train_indices, test_indices in splitter.split(X_global):

            # estimator type is input for the framework
            estimator = AdaBoostClassifier()
            _pipeline = Pipeline([
                ('feature_extraction', PandasFeatureUnion(self._feature_steps)),
                ('feature_selection', Pipeline(self._feature_selection_steps)),
                ('estimator', estimator),
            ])


            # stage 2, time series (rolling window, walk forward, sklearn.TimeSeriesSplit)
            # For each contact, make a new instance of the prediction model
            # TimeSeriesSplit
            tscv = TimeSeriesSplit(n_splits=5)
            print(tscv)
            # TODO: WINDOW EXPANSION INPUT VARIABLE IN CONSTRUCTOR
            X_timeseries = # contactID VERSUS WINDOWS (W1, W2, W3)
            for train_index, test_index in tscv.split(X_timeseries):
                # TRAIN: [0]TEST: [1]
                # TRAIN: [0 1]TEST: [2]
                # TRAIN: [0 1 2]TEST: [3]
                # TRAIN: [0 1 2 3]TEST: [4]
                # TRAIN: [0 1 2 3 4] TEST: [5]

                #train_index = {set of indices to time windows in X_global}
                #test_index = index to final time window in X_global

                # TODO: make function which extracts the label (ground truth) for the given time window
                # TODO: (CONTINUED) generate Y_timeseries[window index]

                # or use our stuff from feature_extraction
                # feature to be extracted
                ftbe = _pipeline
                X[contactID,windowIndex] -> X[contactID,actionsForThatContactInThoseWindows]
                ftbe.fit(X_timeseries[train_index],Y_timeseries[train_index])
                ftbe.predict(X_timeseries[test_index],Y_timeseries[test_index])

                # self._main_pipeline.fit_transform(input_dataframe)




class ValidationScheme:
    def __init__(self):
        pass

    def get_training_data(self):
        pass

    def get_testing_data(self):
        pass


if __name__ == "__main__":

    feature_steps = [
        ('FE_forwarded', FETotalForwarded()),
        ('FE_lifespan', LifespanTransformer()),
        ('FE_emailfreq', EmailFrequencyFeatureTransformer()),
        ('FE_emailrecv', EmailsReceivedTransformer()),
        # ('FE_totallinksclicked', TotalLinksClicked()),
    ]

    feature_selection_steps = [
        ('ANOVA', SelectKBest(f_regression, k=3))
    ]

    estimator = AdaBoostClassifier()

    fw = FuegoFramework('medium_dataset_raw.csv', feature_steps, feature_selection_steps, estimator)
    # output = fw.perform_validation()