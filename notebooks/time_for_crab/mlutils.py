import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.metrics import explained_variance_score, max_error, mean_squared_error, r2_score

__all__ = ['data_downcasting', 'display_df', 'score_comparator', 'score_model']


def data_downcasting(df: pd.DataFrame) -> pd.DataFrame:
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
        df: pd.DataFrame,
        show_info: bool = True,
        show_missing: bool = False,
        show_distinct: bool = False,
        show_describe: bool = False
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


def score_comparator(
        train_scores: pd.DataFrame,
        test_scores: pd.DataFrame,
        train_label: str = 'Train',
        test_label: str = 'Test'
):
    """Plot the scores of two models to compare them.

    Disclaimer: Columns may or may not need to match.

    :param train_scores: The scores of the training model.
    :param test_scores: The scores of the testing model.
    :param train_label: The label for the training model. Default is 'Train'.
    :param test_label: The label for the testing model. Default is 'Test'.
    """

    for i, col in enumerate(train_scores.columns):
        plt.figure()
        plt.title(f'{train_label} vs {test_label}\n{col}')
        plt.bar(i * 2, train_scores[col])
        plt.bar(i * 2 + 1, test_scores[col])
        plt.xticks(ticks=[i * 2, i * 2 + 1], labels=[train_label, test_label])
    plt.show()


def score_model(preds, target):
    """Score the model using some common regression metrics.

    :param preds: Predictions by the model.
    :param target: Target values.
    :return: Dictionary of scores.
    """
    return {
        'explained_variance_score': explained_variance_score(preds, target),
        'max_error': max_error(preds, target),
        'mean_squared_error': mean_squared_error(preds, target),
        'r2_score': r2_score(preds, target)
    }
