""" Implement the hello command.

"""
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, cross_val_predict, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

try:
    # for visual mode. `pip install -e .[visual]`
    import matplotlib.pyplot as plt
    import seaborn as sns
except ModuleNotFoundError:
    plt = None
    sns = None

from ..core.logger import logger

TARGET_LABEL = 'Corona'


def to_unix_epoch(dt):
    return dt.astype9


def normalize(df, column):
    scaler = MinMaxScaler(feature_range=(0, 1))
    return scaler.fit_transform(df[column])


def display_df(df:pd.DataFrame, show_missing:bool=True, show_info:bool=False) -> None:
    """Display the DataFrame.
    
    :param df: The data.
    :type df: pd.DataFrame
    :param show_missing: Whether to show missing data counts.
    :type show_missing: bool
    :param show_info: Whether to show info on the data.
    :type show_info: bool
    """
    logger.info(f'DataFrame shape: {df.shape}')
    logger.info(f'First 5 rows:\n{df.head()}') # preview the first 5 rows
    if show_missing:
        # find any non-numeric data
        logger.info(f'Missing values:\n{df.isna().sum()}')
    if show_info:
        logger.info(f'Info:\n{df.info()}')


def data_disposal(df:pd.DataFrame) -> pd.DataFrame:
    """Clean-up the DataFrame.

    Remove rows:
        - missing any of the symptoms
        - diagnosis of 'other'

    :param df: The data.
    :type df: pd.DataFrame
    :return: The data without disposals.
    :rtype: pd.DataFrame
    """
    # remove rows missing too many values
    required_fields=[TARGET_LABEL, 'Cough_symptoms', 'Fever', 'Sore_throat', 'Shortness_of_breath', 'Headache']
    logger.info(f'Dropping the rows missing required columns: {required_fields}')
    df = df.dropna(subset=required_fields)
    # weird find, get rid of rows where diagnosis is 'other'
    df = df[df[TARGET_LABEL] != 'other']
    return df


def data_conversions(df:pd.DataFrame) -> pd.DataFrame:
    """Convert type in the DataFrame.

    Update values:
        - Convert bools to `0|1`.
        - Fill nulls for typically-binary variables with 0.5.
        - Scale 'Known_contact' with best-guess weights. Could use SA to fine-tune.
        - convert 'Test_date' to unix epoch

    :param df: The data.
    :type df: pd.DataFrame
    :return: The data without conversions.
    :rtype: pd.DataFrame
    """
    # check for "weird" data
    weird_check_cols = ['Test_date', TARGET_LABEL, 'Age_60_above', 'Sex', 'Known_contact']
    for col in weird_check_cols:
        logger.debug(f'Column "{col}" distinct values:\t{df[col].unique()}')
    # filter bools
    df = df.replace(to_replace={
        False: 0, True: 1,
        'negative': 0, 'positive': 1,
        'No': 0, 'Yes': 1,
        'male': 0, 'female': 1
    })
    # weird finds, fill null values for typically-binary variables with 0.5
    df = df.fillna({
        'Age_60_above': 0.5,
        'Sex': 0.5
    })
    # weird find, scale 'Known_contact' with best-guess weights. Could use SA to fine-tune.
    df = df.replace(to_replace={'Known_contact': {'Abroad': 1, 'Contact with confirmed': 0.6, 'Other': 0}})
    # last weird find, convert 'Test_date' to unix epoch
    df['Test_date'] = pd.to_datetime(df['Test_date'], format='%d-%m-%Y').astype('int64') / 10**9
    # finally infer objects
    return df.infer_objects()


def main(dataset_filename:str) -> str:
    """ Execute the command.
    
    :param dataset_filename: Name of a file. Use .csv for now.
    :type dataset_filename: str
    :return: Greeting for the user.
    :rtype: str
    """
    logger.debug('executing svm command')
    pd.set_option('mode.copy_on_write', True)
    pd.set_option('future.no_silent_downcasting', True)
    try:
        df = pd.read_csv(dataset_filename)
    except FileNotFoundError:
        logger.error(f'Could not open file for read: {dataset_filename}')
        return 1;
    display_df(df)
    # Remove bad data
    df = data_disposal(df)
    # Numerify some data
    df = data_conversions(df)
    # shuffle rows
    # when you shuffle rows, you are better prepared for future data scenarios
    # but you lose model training-reproducibility
    df = df.sample(frac=1)
    # display again
    display_df(df, show_info=True)
    # Split into Training/Validation sets
    X = df.drop([TARGET_LABEL], axis=1)
    y = df[TARGET_LABEL]
    # drop id. it would poison the data.
    X = X.drop(['Ind_ID'], axis=1)
    # after some thought, I will remove the 'Test_date' from training set.
    X = X.drop(['Test_date'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
    logger.info(f'Test set:\n{X_train.head()}')
    # ndf = X_train.apply(lambda x: (x - x.mean()) / x.std(), axis=0)
    # for predictor in ndf.columns[0:]:
    #     plt.hist(ndf[predictor])
    #     plt.title(predictor)
    #     plt.ylabel(predictor)
    #     plt.show()
    # logger.info(f'Normalized:\n{ndf.head()}')
    # Input features
    logger.info(f'X_train: {X_train.shape}')
    logger.info(f'X_test: {X_test.shape}')
    if plt is not None:
        sns.set()
        plt.figure(figsize = (14,9))
        #sns.heatmap(X_train.corr(), cmap='GnBu', annot=True)
        plt.title('Correlation Graph')
        # Plotting the heatmap to check the correlation between the Target Label and other features
        sns.heatmap(df.corr()[[TARGET_LABEL]].sort_values(by=TARGET_LABEL, ascending=False), vmin=-1, vmax=1, annot=True, cmap='GnBu')
        plt.show()
    # create and train the model
    model = SVC(kernel='linear')
    model.fit(X_train, y_train)
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    scores = {
        'accuracy': {'train': accuracy_score(y_train, train_preds), 'test': accuracy_score(y_test, test_preds)},
        'precision': {'train': precision_score(y_train, train_preds), 'test': precision_score(y_test, test_preds)},
        'recall': {'train': recall_score(y_train, train_preds), 'test': recall_score(y_test, test_preds)},
        'f1-score': {'train': f1_score(y_train, train_preds), 'test': f1_score(y_test, test_preds)},
    }
    logger.info(scores)
    logger.info(y_test.head())
    logger.info(test_preds[0:5])
    scores_df = pd.DataFrame(scores)
    logger.info(scores_df)
    return f'Hello, {dataset_filename}!'
