import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.src.layers import Dense

from sklearn.metrics import explained_variance_score, mean_squared_error, r2_score, mean_absolute_error

__all__ = [
    'data_downcasting', 'display_df',
    'generate_neural_pyramid',
    'plot_training_loss', 'plot_training_loss_from_dict', 'plot_true_vs_pred_from_dict',
    'score_comparator', 'score_model'
]


def _decide_subplot_shape(n:int, n_cols:int=2) -> tuple[int, int]:
    """Decide the shape of the subplots from the number of plots and columns.

    :param n: The number of subplots.
    :param n_cols: The number of columns. Default is 2.
    :return: The shape of the subplots.
    """
    if n == 1:
        return 1, 1
    n_rows = int(np.ceil(n // n_cols))
    if n % n_cols > 0:
        n_rows += 1
    return n_rows, n_cols


def _decide_subplot_size(shape:tuple[int, int]) -> tuple[int, int]:
    """Decide the display size of the figure from a shape of subplots.

    :param shape: The shape of the subplots.
    :return: The size of the subplots.
    """
    return 10 if 1 == shape[0] == shape[1] else 20, 10*shape[0]


def generate_neural_pyramid(n_layers:int, n_max_neurons:int) -> list[Dense]:
    """Generate a pyramid of neural layers.

    :param n_layers: The number of layers.
    :param n_max_neurons: The maximum number of neurons.
    :return: The pyramid of neural layers.
    """
    return [Dense(units=n_max_neurons >> _, activation='relu') for _ in range(n_layers)]


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
        show_describe:bool=False):
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


def plot_training_loss(history:pd.DataFrame, model_name:str='', figsize:tuple[int]=(20, 10)):
    """Plot the training loss over time.

    Plot loss on the training set and loss on the validation set given a regression model's history dataframe.

    :param history: The history dataframe from the model training.
    :param model_name: The name of the model. Default is ''.
    :param figsize: The size of the figure. Default is (20, 10).
    """
    plt.figure(figsize=figsize)
    plt.title(f'{model_name} Training Loss over Time')
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.ylim([0, 10])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='lower right')


def plot_training_loss_from_dict(history_map:dict[str, pd.DataFrame], n_cols:int=2):
    """Plot the training loss over time from a dictionary.

    Input shape: {'model_name': history_dataframe}
    """
    n_rows, n_cols = _decide_subplot_shape(len(history_map), n_cols)
    fig, axs = plt.subplots(n_rows, n_cols, figsize=_decide_subplot_size((n_rows, n_cols)))
    for i, items in enumerate(history_map.items()):
        model_name, history = items
        axs[i//n_cols][i%n_cols].plot(history.history['loss'], label='loss')
        axs[i//n_cols][i%n_cols].plot(history.history['val_loss'], label='val_loss')
        axs[i//n_cols][i%n_cols].set_title(f'{model_name} Training Loss over Time')
        axs[i//n_cols][i%n_cols].set_ylim([0, 10])
        axs[i//n_cols][i%n_cols].set_xlabel('Epoch')
        axs[i//n_cols][i%n_cols].set_ylabel('Loss')
        axs[i//n_cols][i%n_cols].legend(loc='lower right')


def plot_true_vs_pred_from_dict(
        pred_map:dict[str, dict[str, np.array]],
        n_cols:int=2,
        show_target_line:bool=False,
        show_best_fit_line:bool=False):
    """Plot the true vs predicted values from a dictionary.

    Input shape: {'model_name': {'true': true_values, 'pred': predicted_values}}

    :param pred_map: {'model_name': {'true': true_values, 'pred': predicted_values}}
    :param n_cols: The number of columns to display. Default is 2.
    :param show_target_line: Show the target line. This is a perfect guess. Default is False.
    :param show_best_fit_line: Show the line of best fit. Default is False. WARNING!!! This can be slow.
    """
    n_rows, n_cols = _decide_subplot_shape(len(pred_map), n_cols)
    fig, axs = plt.subplots(n_rows, n_cols, figsize=_decide_subplot_size((n_rows, n_cols)))
    for i, items in enumerate(pred_map.items()):
        model_name, preds = items
        # if feature 'Show target line' is enabled
        if show_target_line:
            # draw a line with a slope of 1
            upper_bound = max(preds['true'].max(), preds['pred'].max())
            lower_bound = min(preds['true'].min(), preds['pred'].min())
            axs[i//n_cols][i%n_cols].plot([lower_bound, upper_bound], [lower_bound, upper_bound], color='green')
        # if feature 'Show line of best fit' is enabled
        if show_best_fit_line:
            # WARNING!!! This is unnecessarily slow.
            # find the slope and intercept of the line of best fit
            m, b = np.polyfit(preds['true'], preds['pred'], 1)
            # add the line to the plot
            axs[i//n_cols][i%n_cols].plot(preds['true'], m*preds['true'] + b, color='red')
        # plot the true vs pred on a scatter plot
        axs[i//n_cols][i%n_cols].scatter(preds['true'], preds['pred'], alpha=0.5)
        axs[i//n_cols][i%n_cols].set_title(f'{model_name} True vs Predicted Age')
        axs[i//n_cols][i%n_cols].set_xlabel('True Age')
        axs[i//n_cols][i%n_cols].set_ylabel('Predicted Age')


def score_combine(leaderboard:pd.DataFrame, qualifier:pd.DataFrame) -> pd.DataFrame:
    """Combine two score DataFrames using upsert (update if exists, insert if not).

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
        test_label:str='test'):
    """Plot the scores of two models to compare them.

    Disclaimer: Columns may or may not need to match.

    :param train_scores: The scores of the training model.
    :param test_scores: The scores of the testing model.
    :param train_label: The label for the training model. Default is 'train'.
    :param test_label: The label for the testing model. Default is 'test'.
    """
    fig, axs = plt.subplots(len(train_scores.columns), sharex=True, figsize=(10, 12))
    for i, col in enumerate(train_scores.columns):
        axs[i].set_title(f'{col}')
        axs[i].bar(0, train_scores[col])
        axs[i].bar(1, test_scores[col])
        axs[i].set_xticks(ticks=[0, 1], labels=[train_label, test_label])


# Add more scores here if needed, they'll automatically show up in the Notebook upon next run.
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
    }
    return pd.DataFrame(scores, index=[index])
