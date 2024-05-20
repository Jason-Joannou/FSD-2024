import pandas as pd


def count_nans_per_column(df: pd.DataFrame) -> pd.Series:
    return df.isnull().sum()


def count_outliers(df: pd.DataFrame) -> pd.Series:
    # Columns to check for outliers
    # Make sure to check for ML
    columns_to_check = ["High", "Low", "Open", "Close", "Volume", "Marketcap"]
    outliers = {}
    coin_names = set(df["Name"].to_list())

    for coin_name in coin_names:
        temp_df = df[df["Name"] == coin_name]

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

    return pd.Series(outliers)


if __name__ == "__main__":
    df = pd.read_csv("./.data/coins.csv")
    print(count_nans_per_column(df=df))
    print(count_outliers(df=df))
