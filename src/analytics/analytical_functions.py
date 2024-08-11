import pandas as pd
import numpy as np
from typing import List, Tuple
import plotly.graph_objs as go

def daily_price_change(df: pd.DataFrame) -> pd.DataFrame:
    df.sort_values(["Name", "Date"], inplace=True)
    df['DailyPriceChangeClosing'] = df.groupby("Name")['Close'].diff() 
    return df

def daily_price_range(df: pd.DataFrame) -> pd.DataFrame:
    df.sort_values(["Name", "Date"], inplace=True)
    df['DailyPriceRange'] = df['High'] - df['Low']
    return df

def daily_price_range_volatility(df: pd.DataFrame) -> pd.DataFrame:
    df.sort_values(["Name", "Date"], inplace=True)
    df['DailyPriceRangeVolatility'] = (df['High'] - df['Low']) / df['Open']
    return df

def daily_price_volatility(df: pd.DataFrame) -> pd.DataFrame:
    df.sort_values(["Name", "Date"], inplace=True)
    df['DailyPriceVolatility'] = df['Close'] - df['Open']
    return df

def moving_average(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    df[f'MovingAverage_{window}'] = df.groupby("Name")['Close'].transform(lambda x: x.rolling(window, min_periods=1).mean())
    return df

def find_peaks_and_valleys(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    df['Peak'] = df.groupby("Name")['Close'].transform(lambda x: x[(x.shift(1) < x) & (x.shift(-1) < x)])
    df['Valley'] = df.groupby("Name")['Close'].transform(lambda x: x[(x.shift(1) > x) & (x.shift(-1) > x)])
    return df

def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    #TODO Fix the correlation function
    # This function does a correlation analysis between all the columns in the data and not within any specific coin
    # The correlation analysis should be between a selected coin and other coins
    df_pivot = df.pivot(index='Date', columns='Name', values='Close')
    correlation_matrix = df_pivot.corr()
    # numeric_cols = df.select_dtypes(include=[np.number]).columns
    # correlation_matrix = df[numeric_cols].corr()
    return correlation_matrix

if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")

    selected_coins = ["Aave", "Binance Coin"]
    df = df[df["Name"].isin(selected_coins)]
    df["Date"] = pd.to_datetime(df["Date"])

    # Calculate daily price change for each coin
    report_df = daily_price_change(df)