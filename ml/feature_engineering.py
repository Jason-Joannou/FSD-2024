import pandas as pd
import numpy as np

def date_features(df: pd.DataFrame) -> pd.DataFrame:
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)

    return df

def price_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["Name", "Date"])
    df['ClosingPriceChange'] = df.groupby('Name')['Close'].pct_change().fillna(0)
    df['OpeningPriceChange'] = df.groupby('Name')['Open'].pct_change().fillna(0)

    return df

def volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["Name", "Date"])
    df['PriceRange'] = df['High'] - df['Low']
    df['PriceRangePercentage'] = (df['PriceRange'] / df['Low']) * 100
    return df

def moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["Name", "Date"])
    df['Closing_MA_5'] = df['Close'].rolling(window=5).mean()
    df['Closing_MA_10'] = df['Close'].rolling(window=10).mean()
    df['Volume_MA_5'] = df['Volume'].rolling(window=5).mean()
    df['Volume_MA_10'] = df['Volume'].rolling(window=10).mean()

    return df


if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    df = date_features(df=df)
    df = price_features(df=df)
    df = volatility_features(df=df)
    print(df.head(20))


