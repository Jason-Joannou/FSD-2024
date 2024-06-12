import pandas as pd


def count_nans_per_column(df: pd.DataFrame) -> pd.Series:
    return df.isnull().sum().to_dict()


def count_outliers(df: pd.DataFrame) -> pd.Series:
    # Columns to check for outliers
    columns_to_check = ["High", "Low", "Open", "Close", "Volume", "Marketcap"]
    outliers = {}

    # Group DataFrame by coin name
    grouped_df = df.groupby("Name")

    for coin_name, temp_df in grouped_df:
        for col in columns_to_check:
            if col in temp_df.columns:
                Q1 = temp_df[col].quantile(0.25)
                Q3 = temp_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outlier_count = (
                    (temp_df[col] < lower_bound) | (temp_df[col] > upper_bound)
                ).sum()
                outliers[f"{coin_name}_{col}"] = outlier_count

    return outliers


if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    print(count_nans_per_column(df=df))
    print(count_outliers(df=df))
