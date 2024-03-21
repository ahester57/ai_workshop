""" Implement the hello command.

"""
import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

try:
    # for visual mode. `pip install -e .[visual]`
    import matplotlib.pyplot as plt
    import seaborn as sns
except ModuleNotFoundError:
    plt = None
    sns = None

from ..core.logger import logger


def display_df(df:pd.DataFrame, show_missing:bool=True, show_info:bool=False) -> None:
    logger.info(f'DataFrame shape: {df.shape}')
    logger.info(f'First 5 rows:\n{df.head()}') # preview the first 5 rows
    if show_missing:
        # find any non-numeric data
        logger.info(f'Missing values:\n{df.isna().sum()}')
    if show_info:
        logger.info(f'Info:\n{df.info()}')


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
        df = pd.read_csv(dataset_filename,)
    except FileNotFoundError:
        logger.error(f'Could not open file for read: {dataset_filename}')
        return 1;
    display_df(df)
    # remove rows missing too many values
    required_fields=['Corona', 'Cough_symptoms', 'Fever', 'Sore_throat', 'Shortness_of_breath', 'Headache']
    logger.info(f'Dropping the rows missing required columns: {required_fields}')                                                           
    df.dropna(subset=required_fields, inplace=True)
    # filter bools
    df.replace(to_replace={False: 0, True: 1}, inplace=True)
    df.replace(to_replace={'negative': 0, 'positive': 1}, inplace=True)
    df.replace(to_replace={'no': 0, 'yes': 1}, inplace=True)
    # check for "weird" data
    weird_check_cols = ['Corona', 'Age_60_above', 'Sex', 'Known_contact']
    for col in weird_check_cols:
        logger.debug(f'Column "{col}" distinct values:\t{df[col].unique()}')
    # weird find, get rid of rows where diagnosis is 'other'
    df = df[df['Corona'] != 'other']
    # weird finds, fill null values for typically-binary variables with 0.5
    df['Age_60_above'].fillna(0.5);
    # finally infer objects
    df = df.infer_objects()
    # display again
    display_df(df, show_info=True)
    return f'Hello, {dataset_filename}!'
