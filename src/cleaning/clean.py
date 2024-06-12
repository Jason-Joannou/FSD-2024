import pandas as pd
from .utility import count_outliers


def fill_na_with_median_and_mode(df: pd.DataFrame) -> pd.DataFrame:
    # Fill NA in numeric columns with the median
    for col in df.select_dtypes(include=["number"]).columns:
        median = df[col].median()
        df[col].fillna(median)

    # Fill NA in non-numeric columns with the mode
    for col in df.select_dtypes(exclude=["number"]).columns:
        mode = df[col].mode()[0]
        df[col].fillna(mode)

    return df


def convert_datetime_column(df: pd.DataFrame) -> pd.DataFrame:
    df = pd.to_datetime(df["Date"])
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df.drop_duplicates(inplace=True)
    return df


def remove_outliers(
    df: pd.DataFrame,
    columns: list = ["High", "Low", "Open", "Close", "Volume", "Marketcap"],
) -> pd.DataFrame:
    cleaned_dfs = []

    for coin_name, temp_df in df.groupby("Name"):
        for col in columns:
            Q1 = temp_df[col].quantile(0.25)
            Q3 = temp_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            temp_df = temp_df[
                (temp_df[col] >= lower_bound) & (temp_df[col] <= upper_bound)
            ]

        cleaned_dfs.append(temp_df)

    return pd.concat(cleaned_dfs, ignore_index=True)


if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    print(df.head())
    print("----------")
    print(count_outliers(df=df))
    print("----------")
    df = fill_na_with_median_and_mode(df=df)
    print(df.head())
    print("----------")
    df = remove_outliers(df=df)
    print(df.head())
    print(len(df))
    print("---------------")

    print(count_outliers(df=df))
