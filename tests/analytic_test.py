import pandas as pd
import numpy as np
import pytest


# Assuming the functions to be tested are imported from your module
from src.analytics.analytical_functions import (
    daily_price_change,
    daily_price_range,
    daily_price_range_volatility,
    daily_price_volatility,
    moving_average,
    find_peaks_and_valleys,
    correlation_analysis
)

@pytest.fixture
def sample_data():
    data = {
        'Name': ['Aave', 'Aave', 'Aave', 'Binance Coin', 'Binance Coin', 'Binance Coin'],
        'Date': pd.date_range(start='2023-01-01', periods=3).tolist() * 2,
        'Open': [100, 105, 110, 200, 210, 220],
        'High': [110, 115, 120, 220, 225, 230],
        'Low': [90, 95, 100, 180, 190, 200],
        'Close': [105, 110, 115, 210, 215, 225],
        'Volume': [1000, 1500, 2000, 3000, 3500, 4000]
    }
    return pd.DataFrame(data)


def test_daily_price_change(sample_data):
    df = daily_price_change(sample_data.copy())
    expected_changes = [None, 5.0, 5.0, None, 5.0, 10.0]
    assert df['DailyPriceChangeClosing'].tolist() == expected_changes

def test_daily_price_range(sample_data):
    df = daily_price_range(sample_data.copy())
    expected_ranges = [20, 20, 20, 40, 35, 30]
    assert df['DailyPriceRange'].tolist() == expected_ranges

def test_daily_price_range_volatility(sample_data):
    df = daily_price_range_volatility(sample_data.copy())
    expected_volatility = [0.2, 0.19047619047619047, 0.18181818181818182, 0.2, 0.16666666666666666, 0.13636363636363635]
    assert np.allclose(df['DailyPriceRangeVolatility'].tolist(), expected_volatility, rtol=1e-05)

def test_daily_price_volatility(sample_data):
    df = daily_price_volatility(sample_data.copy())
    expected_volatility = [5, 5, 5, 10, 5, 5]
    assert df['DailyPriceVolatility'].tolist() == expected_volatility

def test_moving_average(sample_data):
    df = moving_average(sample_data.copy(), window=2)
    expected_moving_averages = [105.0, 107.5, 112.5, 210.0, 212.5, 220.0]
    assert np.allclose(df['MovingAverage_2'].dropna().tolist(), expected_moving_averages, rtol=1e-05)

def test_find_peaks_and_valleys(sample_data):
    df = find_peaks_and_valleys(sample_data.copy(), window=1)
    expected_peaks = [105, 110, 115, 210, 215, 225]
    expected_valleys = [105, 110, 115, 210, 215, 225]
    assert df['Peak'].tolist() == expected_peaks
    assert df['Valley'].tolist() == expected_valleys

def test_correlation_analysis(sample_data):
    correlation_matrix = correlation_analysis(sample_data.copy())
    assert isinstance(correlation_matrix, pd.DataFrame)
    assert correlation_matrix.shape == (5, 5)  # Since we have 5 numeric columns

if __name__ == "__main__":
    pytest.main()

