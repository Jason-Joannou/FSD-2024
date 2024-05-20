import pandas as pd

def fill_na_with_median_and_mode(df: pd.DataFrame) -> pd.DataFrame:
    # Fill NA in numeric columns with the median
    for col in df.select_dtypes(include=['number']).columns:
        median = df[col].median()
        df[col].fillna(median, inplace=True)

    # Fill NA in non-numeric columns with the mode
    for col in df.select_dtypes(exclude=['number']).columns:
        mode = df[col].mode()[0]
        df[col].fillna(mode, inplace=True)

    return df

def remove_outliers():
    raise NotImplementedError("Not implemented yet")