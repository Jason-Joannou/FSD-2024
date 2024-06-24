import pandas as pd
import numpy as np
from typing import List, Tuple
import plotly.graph_objs as go

def daily_price_change(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the daily closing price change for each coin.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'Name', 'Date', and 'Close'.

    Returns:
        pd.DataFrame: DataFrame with a new column 'DailyPriceChangeClosing' representing the difference in closing price from the previous day.
    """
    df.sort_values(["Name", "Date"], inplace=True)
    df['DailyPriceChangeClosing'] = df.groupby("Name")['Close'].diff()
    #return 
    return df


def daily_price_range(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the daily price range for each coin.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'Name', 'Date', 'High', and 'Low'.

    Returns:
        pd.DataFrame: DataFrame with a new column 'DailyPriceRange' representing the difference between the high and low prices for each day.
    """
    df.sort_values(["Name", "Date"], inplace=True)
    df['DailyPriceRange'] = df['High'] - df['Low']
    return df

def daily_price_range_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the daily price range volatility for each coin.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'Name', 'Date', 'High', 'Low', and 'Open'.

    Returns:
        pd.DataFrame: DataFrame with a new column 'DailyPriceRangeVolatility' representing the ratio of the daily price range to the opening price.
    """

    df.sort_values(["Name", "Date"], inplace=True)
    df['DailyPriceRangeVolatility'] = (df['High'] - df['Low']) / df['Open']
    return df

def daily_price_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the daily price volatility for each coin.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'Name', 'Date', 'Open', and 'Close'.

    Returns:
        pd.DataFrame: DataFrame with a new column 'DailyPriceVolatility' representing the difference between the closing and opening prices for each day.
    """
    df.sort_values(["Name", "Date"], inplace=True)
    df['DailyPriceVolatility'] = df['Close'] - df['Open']
    return df

def moving_average(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """Calculate the moving average for the closing price of each coin.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'Name', 'Date', and 'Close'.
        window (int, optional): The window size for the moving average. Defaults to 5.

    Returns:
        pd.DataFrame: DataFrame with a new column representing the moving average of the closing price over the specified window.
    """
    df[f'MovingAverage_{window}'] = df.groupby("Name")['Close'].transform(lambda x: x.rolling(window, min_periods=1).mean())
    return df

def find_peaks_and_valleys(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """Identify peaks and valleys in the closing price for each coin.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'Name' and 'Close'.
        window (int, optional): The window size for identifying peaks and valleys. Defaults to 3.

    Returns:
        pd.DataFrame: DataFrame with new columns 'Peak' and 'Valley' indicating local peaks and valleys in the closing price.
    """
    df['Peak'] = df.groupby("Name")['Close'].transform(lambda x: x[(x.shift(1) < x) & (x.shift(-1) < x)])
    df['Valley'] = df.groupby("Name")['Close'].transform(lambda x: x[(x.shift(1) > x) & (x.shift(-1) > x)])
    return df

def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Perform correlation analysis on numeric columns of the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing numeric columns.

    Returns:
        pd.DataFrame: Correlation matrix of the numeric columns.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    return correlation_matrix

if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")

    selected_coins = ["Aave", "Binance Coin"]
    df = df[df["Name"].isin(selected_coins)]
    df["Date"] = pd.to_datetime(df["Date"])

    # Calculate daily price change for each coin
    report_df = daily_price_change(df)