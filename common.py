
import pandas as pd
from typing import Optional
from pathlib import Path


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
    df.drop(columns=['date', 'minute', 'label'], inplace=True)

    # sort data by from old datetime to new datetime
    df.sort_values(by=['datetime']).reset_index(drop=True, inplace=True)

    return df


def get_raw_data(csv_file_path: [str, Path]) -> Optional[pd.DataFrame]:
    """ get path to csv file, and return it as dataframe """

    # convert string input to Path type
    if isinstance(csv_file_path, str):
        csv_file_path = Path(csv_file_path)

    df = None
    if csv_file_path.exists():
        df = pd.read_csv(csv_file_path)

    return df


<<<<<<< Updated upstream
def calc_roc(df, col, length):
    df[col + ]
=======
def roc(df, col, length):
    """ calc rate of change on given column, using given length """
    return df[col] / df[col].shift(length) - 1


def add_times(df, col):
    """ split datetime column to its components (ie minute, hour, day etc...) """

    df['minute'] = df[col].dt.minute
    df['hour'] = df[col].dt.hour
    df['day'] = df[col].dt.day
    df['month'] = df[col].dt.month

    df['minute_of_day'] = df['minute'] + df['hour']*60
    df['day_of_week'] = df['datetime'].dt.dayofweek
>>>>>>> Stashed changes
