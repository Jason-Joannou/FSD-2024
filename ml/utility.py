from sklearn.model_selection import train_test_split
import pandas as pd
from typing import Tuple

def split_data(features, target, split=0.2):
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=split)
    return X_train, X_test, y_train, y_test

def calculate_sma(data: pd.Series, window: int = 5) -> pd.Series:
    data = data.rolling(window=window).mean()
    return data

def calculate_ema(data: pd.Series, span: int = 10) -> pd.Series:
    data = data.ewm(span=span, adjust=False)
    return data

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series: pd.Series, span1: int = 12, span2: int = 26) -> pd.Series:
    exp1 = series.ewm(span=span1, adjust=False).mean()
    exp2 = series.ewm(span=span2, adjust=False).mean()
    macd = exp1 - exp2
    return macd

def calculate_bollinger_bands(series: pd.Series, window: int = 20) -> Tuple[pd.Series, pd.Series]:
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    bollinger_high = sma + (std * 2)
    bollinger_low = sma - (std * 2)
    return bollinger_high, bollinger_low

def calculate_volume_oscillator(volume: pd.Series, short_window: int = 12, long_window: int = 26) -> pd.Series:
    short_volume_ma = volume.rolling(window=short_window).mean()
    long_volume_ma = volume.rolling(window=long_window).mean()
    volume_oscillator = (short_volume_ma - long_volume_ma) / long_volume_ma
    return volume_oscillator

def calculate_roc(series: pd.Series, period: int = 12) -> pd.Series:
    roc = ((series - series.shift(period)) / series.shift(period)) * 100
    return roc

def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
    tr = pd.DataFrame()
    tr['TR1'] = abs(high - low)
    tr['TR2'] = abs(high - close.shift())
    tr['TR3'] = abs(low - close.shift())
    true_range = tr.max(axis=1)
    atr = true_range.rolling(window=window).mean()
    return atr

def calculate_lag_features(df: pd.DataFrame, lags: int = 1) -> pd.DataFrame:
    for lag in range(1, lags + 1):
        df[f'Lag_{lag}_Close'] = df['Close'].shift(lag)
        df[f'Lag_{lag}_High'] = df['High'].shift(lag)
        df[f'Lag_{lag}_Low'] = df['Low'].shift(lag)
        df[f'Lag_{lag}_Volume'] = df['Volume'].shift(lag)
    return df