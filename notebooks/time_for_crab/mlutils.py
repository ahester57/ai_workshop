import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.metrics import explained_variance_score, max_error, mean_squared_error, r2_score, mean_absolute_error

__all__ = ['data_downcasting', 'display_df', 'plot_training_loss', 'score_comparator', 'score_model']


def data_downcasting(df:pd.DataFrame) -> pd.DataFrame:
    """Reduce the memory usage of the DataFrame by downcasting numeric types.

    :param df: DataFrame to be reduced.
    :return: DataFrame with reduced memory usage.
    """
    start_mem = df.memory_usage().sum() / 1024 ** 2
    print(f'Memory usage of dataframe is {start_mem:.4f} MB (before)')

    # Define mapping of types to numpy types
    type_ranges = {
        'int': [(np.iinfo(np.int8).min, np.iinfo(np.int8).max, np.int8),
                (np.iinfo(np.int16).min, np.iinfo(np.int16).max, np.int16),
                (np.iinfo(np.int32).min, np.iinfo(np.int32).max, np.int32),
                (np.iinfo(np.int64).min, np.iinfo(np.int64).max, np.int64)],
        'float': [(np.finfo(np.float16).min, np.finfo(np.float16).max, np.float16),
                  (np.finfo(np.float32).min, np.finfo(np.float32).max, np.float32),
                  (np.finfo(np.float64).min, np.finfo(np.float64).max, np.float64)]
    }

    for col in df.columns:
        col_type = df[col].dtype
        c_min, c_max = df[col].min(), df[col].max()

        if col_type in ['int16', 'int32', 'int64']:
            for min_val, max_val, new_type in type_ranges['int']:
                if c_min > min_val and c_max < max_val:
                    df[col] = df[col].astype(new_type)
                    break

        elif col_type in ['float16', 'float32', 'float64']:
            for min_val, max_val, new_type in type_ranges['float']:
                if c_min > min_val and c_max < max_val:
                    df[col] = df[col].astype(new_type)
                    break

    end_mem = df.memory_usage().sum() / 1024 ** 2
    print(f'Memory usage of dataframe is {end_mem:.4f} MB (after)')
    print(f'Reduced {100 * (start_mem - end_mem) / start_mem:.1f}%')
    return df


def display_df(
        df:pd.DataFrame,
        show_info:bool=True,
        show_missing:bool=False,
        show_distinct:bool=False,
        show_describe:bool=False
):
    """Display the DataFrame.

    :param df: The data.
    :param show_info: Whether to show info on the data.
    :param show_missing: Whether to show missing data counts.
    :param show_distinct: Whether to show distinct values.
    :param show_describe: Whether to show the describe method.
    """
    print(f'DataFrame shape: {df.shape}')
    print(f'First 5 rows:\n{df.head()}')  # preview the first 5 rows
    if show_info:
        print(f'Info:\n{df.info()}')
    if show_missing:
        print(f'Missing values:\n{df.isna().sum()}')
    if show_distinct:
        for col in df:
            print(f'{col} distinct values:\n{df[col].unique()[0:10]}')
    if show_describe:
        df.describe()


def plot_training_loss(history:pd.DataFrame):
    """Plot the training loss over time.

    :param history: The history object from the model training.
    """
    plt.figure(figsize=(20, 10))
    plt.title('Training Loss over Time')
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.ylim([0, 10])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.show()


def score_combine(leaderboard:pd.DataFrame, qualifier:pd.DataFrame) -> pd.DataFrame:
    """Combine two score DataFrames.

    :param leaderboard: The scores accumulated so far.
    :param qualifier: The scores to add to the leaderboard.
    """
    leaderboard = leaderboard.drop(qualifier.index, errors='ignore')
    leaderboard = pd.concat(
        [
            leaderboard,  # only add to combination if it's not already there
            qualifier[~qualifier.index.isin(leaderboard.index)]
        ]
        , axis=0
    )
    return leaderboard


def score_comparator(
        train_scores:pd.DataFrame,
        test_scores:pd.DataFrame,
        train_label:str='train',
        test_label:str='test'
):
    """Plot the scores of two models to compare them.

    Disclaimer: Columns may or may not need to match.

    :param train_scores: The scores of the training model.
    :param test_scores: The scores of the testing model.
    :param train_label: The label for the training model. Default is 'train'.
    :param test_label: The label for the testing model. Default is 'test'.
    """
    fig, axs = plt.subplots(len(train_scores.columns), sharex=True, figsize=(10, 10))
    for i, col in enumerate(train_scores.columns):
        axs[i].set_title(f'{col}')
        axs[i].bar(0, train_scores[col])
        axs[i].bar(1, test_scores[col])
        axs[i].set_xticks(ticks=[0, 1], labels=[train_label, test_label])


def score_model(preds, target, index:str='index') -> pd.DataFrame:
    """Score the model using some common regression metrics.

    :param preds: Predictions by the model.
    :param target: Target values.
    :param index: Index for the DataFrame. Default is 'index'.
    :return: DataFrame of scores.
    """
    scores = {
        'mean_squared_error': mean_squared_error(preds, target),
        'mean_absolute_error': mean_absolute_error(preds, target),
        'explained_variance_score': explained_variance_score(preds, target),
        'r2_score': r2_score(preds, target),
        'max_error': max_error(preds, target),
    }
    return pd.DataFrame(scores, index=[index])
