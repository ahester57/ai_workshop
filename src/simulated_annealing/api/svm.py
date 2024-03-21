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


def to_unix_epoch(dt):
    return dt.astype9


def normalize(df, column):
    scaler = MinMaxScaler(feature_range=(0, 1))
    return scaler.fit_transform(df[column])


def display_df(df:pd.DataFrame, show_missing:bool=True, show_info:bool=False) -> None:
    logger.info(f'DataFrame shape: {df.shape}')
    logger.info(f'First 5 rows:\n{df.head()}') # preview the first 5 rows
    if show_missing:
        # find any non-numeric data
        logger.info(f'Missing values:\n{df.isna().sum()}')
    if show_info:
        logger.info(f'Info:\n{df.info()}')


def data_disposal(df:pd.DataFrame) -> pd.DataFrame:
    # remove rows missing too many values
    required_fields=['Corona', 'Cough_symptoms', 'Fever', 'Sore_throat', 'Shortness_of_breath', 'Headache']
    logger.info(f'Dropping the rows missing required columns: {required_fields}')
    df = df.dropna(subset=required_fields)
    # weird find, get rid of rows where diagnosis is 'other'
    df = df[df['Corona'] != 'other']
    return df


def data_conversions(df:pd.DataFrame) -> pd.DataFrame:
    # filter bools
    df = df.replace(to_replace={
        False: 0, True: 1,
        'negative': 0, 'positive': 1,
        'No': 0, 'Yes': 1,
        'male': 0, 'female': 1
    })
    # check for "weird" data
    weird_check_cols = ['Test_date', 'Corona', 'Age_60_above', 'Sex', 'Known_contact']
    for col in weird_check_cols:
        logger.debug(f'Column "{col}" distinct values:\t{df[col].unique()}')
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


def main(dataset_filename:str, max_missing_vals:int=9) -> str:
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
    # display again
    display_df(df, show_info=True)
    # Split into Training/Validation sets
    X = df.drop(['Corona'], axis=1)
    y = df['Corona']
    # drop id. it would poison the data.
    X.drop(['Ind_ID'], axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
    logger.info(X_train.head())
    for predictor in X_train.columns[1:]:
        plt.hist(X_train[predictor])
        plt.title(predictor)
        plt.ylabel(predictor)
        plt.show()
    return f'Hello, {dataset_filename}!'
