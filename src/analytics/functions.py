import pandas as pd
import numpy as np
from typing import List, Tuple

def daily_price_change(df: pd.DataFrame) ->  Tuple:
    raise NotImplementedError("Not implemented yet")

def daily_price_range(df: pd.DataFrame) -> Tuple:
    df['Date'] = pd.to_datetime(df['Date'])
    df['PriceRange'] = df['High'] - df['Low']
    # Select relevant columns for the result
    result = df[['Name', 'Date', 'PriceRange']]
    return result

def daily_price_volatilty(df: pd.DataFrame) -> Tuple:
    raise NotImplementedError("Not implemented yet")

def moving_averages(df: pd.DataFrame) -> pd.DataFrame:

# As a user of the dashboard i would like to view the overall trends of movements within specific coins
# so that i can get a calculated understanding of the history of the coins movements whithout noise within the data altering my interpretation of the price movements.
    move_df = df
    move_df = move_df.sort_values(["Name", "Date"])
    move_df['Closing_MA_5'] = move_df['Close'].rolling(window=1).mean()
    moving_avg = move_df['Closing_MA_5'].to_list()
    coin_names = move_df['Name'].to_list()
    dates = move_df['Date'].to_list()
    return moving_avg, coin_names, dates



def find_peaks_and_valleys(df: pd.DataFrame) ->Tuple:
    raise NotImplementedError("Not implemented yet")

def correlation_analysis(df: pd.DataFrame) -> Tuple:
    raise NotImplementedError("Not implemented yet")

def test_function(df: pd.DataFrame) -> Tuple:
    test_dict = {}
    for i, coin_name in enumerate(set(df["Name"].to_list())):
        print(i)
        test_dict[i] = coin_name
    return test_dict
    

if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    print(df.head())


