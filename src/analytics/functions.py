import pandas as pd
import numpy as np
from typing import List, Tuple

def daily_price_change(df: pd.DataFrame) ->  Tuple:
    raise NotImplementedError("Not implemented yet")

def daily_price_range(df: pd.DataFrame) -> Tuple:
    raise NotImplementedError("Not implemented yet")

def daily_price_volatilty(df: pd.DataFrame) -> Tuple:
    raise NotImplementedError("Not implemented yet")

def moving_average(df: pd.DataFrame) -> Tuple:
    raise NotImplementedError("Not implemented yet")

def find_peaks_and_valleys(df: pd.DataFrame) ->Tuple:
    raise NotImplementedError("Not implemented yet")

def correlation_analysis(df: pd.DataFrame) -> Tuple:
    raise NotImplementedError("Not implemented yet")



if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    print(df.head())