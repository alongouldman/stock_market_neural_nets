from pathlib import Path
from typing import Optional, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display


class StockData:
    data_sets = ['training', 'validation', 'test']

    def __init__(self, stock_ticker: str):
        self.ticker = stock_ticker
        data_folder = Path('data_feather')
        for val in self.data_sets:
            folder = data_folder / val
            ticker_data_file = next(ticker for ticker in folder.iterdir() if ticker.name.split(".")[0].lower() == self.ticker.lower())
            df = pd.read_feather(ticker_data_file)
            setattr(self, val, df)


def get_all_stocks():
    data_folder = Path('data_feather/training')
    for stock in data_folder.iterdir():
        yield stock.name.split(".")[0]


def normalize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    return (dataframe - dataframe.min()) / (dataframe.max() - dataframe.min())


def plot_ohlc_graph_from_dataframe(datafram: pd.DataFrame):
    fig = go.Figure(data=go.Ohlc(x=datafram['datetime'],
                                 open=datafram['open'],
                                 high=datafram['high'],
                                 low=datafram['low'],
                                 close=datafram['close']))
    fig.show()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df['datetime'] = df['date'] + "," + df['minute']
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d,%H:%M')
    del df['date']
    del df['label']
    df['minute'] = df['minute'].str.replace(":", "", regex=False).astype(int)
    df['dayofweek'] = df['datetime'].dt.dayofweek
    df = df[df['open'].notna()]
    df = df.sort_values(by=['datetime']).reset_index(drop=True)
    return df


def get_stock_data(ticker: str, columns: Optional[List[str]] = None, optional_file_paths: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
    if not optional_file_paths:
        optional_file_paths = ['data/relevant/snp500_from_iex', 'data/relevant/iex_data']
    for path in optional_file_paths:
        file_path = Path(path) / f"{ticker}.csv"
        if file_path.exists():
            if columns:
                return pd.read_csv(file_path, usecols=columns)
            else:
                return pd.read_csv(file_path)
    return None


def get_dukas_data(ticker: str):
    return get_stock_data(f'{ticker}.USUSD', optional_file_paths=['data/relevant/dukascopy/BID'])


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


def add_times(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """ split datetime column to its components (ie minute, hour, day etc...) """

    df['minute'] = df[col].dt.minute
    df['hour'] = df[col].dt.hour
    df['day'] = df[col].dt.day
    df['month'] = df[col].dt.month
    df['minute_of_day'] = df['minute'] + df['hour'] * 60
    df['day_of_week'] = df['datetime'].dt.dayofweek
    return df


def display_all(df: pd.DataFrame):
    """ display dataframe up to 1000 rows and columns (taken from FastAI) """
    with pd.option_context("display.max_rows", 1000, "display.max_columns", 1000):
        display(df)


def rate_of_change_PnL(pred_roc, actual_roc):
    """ calculate the profit/loss of every prediction """
    return (pred_roc > 0) * actual_roc - (pred_roc <= 0) * actual_roc


def normalize_with_window(dataframe: pd.DataFrame, window_size: int) -> pd.DataFrame:
    # epsilon is added in order to prevent zero devision
    return (dataframe - dataframe.rolling(window_size).min()) / (dataframe.rolling(window_size).max() - dataframe.rolling(window_size).min() + np.finfo(float).eps)
