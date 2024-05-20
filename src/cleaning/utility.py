import pandas as pd

def count_nans_per_column(df: pd.DataFrame) -> pd.Series:
    return df.isnull().sum()

