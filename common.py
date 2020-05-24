
import pandas as pd
from typing import Optional
from pathlib import Path
from IPython.display import display


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df['datetime'] = df['date'] + "," + df['minute']
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d,%H:%M')
    del df['date']
    del df['label']
    df['minute'] = df['minute'].str.replace(":",  "", regex=False).astype(int)
    df['dayofweek'] = df['datetime'].dt.dayofweek
    df = df[df['open'].notna()]
    df = df.sort_values(by=['datetime']).reset_index(drop=True)
    return df


def get_stock_data(ticker: str) -> Optional[pd.DataFrame]:
    optional_file_paths = ['data/relevant/snp500_from_iex', 'data/relevant/iex_data']
    for path in optional_file_paths:
        file_path = Path(path) / f"{ticker}.csv"
        if file_path.exists:
            return pd.read_csv(file_path)
    return None


def minimal_IEX_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    """ get raw IEX-OHLC dataframe, make minimal preprocessing on it and remove redundant columns """

    # make 1 datetime column
    df['datetime'] = df['date'] + "," + df['minute']
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d,%H:%M')
    del df['date']
    del df['minute']
    del df['label']

    # sort data by from old datetime to new datetime
    df.sort_values(by=['datetime']).reset_index(drop=True, inplace=True)

    return df


def rate_of_change(df: pd.DataFrame, col: str, length: int) -> pd.DataFrame:
    """ calc rate of change on given column, using given length """
    return df[col] / df[col].shift(length) - 1


def add_times(df: pd.DataFrame, col: str):
    """ split datetime column to its components (ie minute, hour, day etc...) """

    df['minute'] = df[col].dt.minute
    df['hour'] = df[col].dt.hour
    df['day'] = df[col].dt.day
    df['month'] = df[col].dt.month
    df['minute_of_day'] = df['minute'] + df['hour']*60
    df['day_of_week'] = df['datetime'].dt.dayofweek


def display_all(df: pd.DataFrame):
    """ display dataframe up to 1000 rows and columns (taken from FastAI) """
    with pd.option_context("display.max_rows", 1000, "display.max_columns", 1000):
        display(df)


def rate_of_change_PnL(pred_roc, actual_roc):
    """ calculate the profit/loss of every prediction """
    return (pred_roc > 0) * actual_roc - (pred_roc <= 0) * actual_roc
