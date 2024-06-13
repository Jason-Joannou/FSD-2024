import pandas as pd
import numpy as np
from .utility import (calculate_sma,
                      calculate_ema,
                      calculate_macd,
                      calculate_bollinger_bands,
                      calculate_rsi, 
                      calculate_volume_oscillator,
                      calculate_roc,
                      calculate_atr,
                      calculate_lag_features)


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)

    return df

def add_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    df = calculate_lag_features(df=df, lags=2)
    df["SMA_10"] = calculate_sma(data=df["Close"], window=10)
    df["SMA_50"] = calculate_sma(data=df["Close"], window=50)
    df["EMA_10"] = calculate_ema(data=df["Close"], span=10)
    df["EMA_50"] = calculate_ema(data=df["Close"], span=50)
    df['RSI'] = calculate_rsi(df['Close'])
    df['MACD'] = calculate_macd(df['Close'])
    df['Bollinger_High'], df['Bollinger_Low'] = calculate_bollinger_bands(df['Close'])
    df['Volume_Oscillator'] = calculate_volume_oscillator(df['Volume'])
    df['ROC'] = calculate_roc(df['Close'])
    df['ATR'] = calculate_atr(df['High'], df['Low'], df['Close'])

    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = add_date_features(df=df)
    df = add_technical_features(df=df)

    return df

if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    df = preprocess_data(df=df)
    


