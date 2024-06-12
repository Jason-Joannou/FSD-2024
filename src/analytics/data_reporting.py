import pandas as pd


def coin_proportion(df: pd.DataFrame) -> pd.DataFrame:
    coin_proportion = df['Name'].value_counts(normalize=True) * 100
    return coin_proportion

def date_range_coins(df: pd.DataFrame) -> pd.DataFrame:
    date_ranges = df.groupby('Name')['Date'].agg(['min', 'max'])
    return date_ranges

def records_per_coin(df: pd.DataFrame):
    coin_counts = df['Name'].value_counts()
    return coin_counts

def coin_summary_info(df: pd.DataFrame):
    summary_info = df.groupby('Name').agg({
        'Date': ['min', 'max', 'count'],
        'Volume': 'sum',
        'Marketcap': 'mean'
    })
    summary_info.columns = ['Start Date', 'End Date', 'Number of Records', 'Total Volume', 'Average Market Cap']
    return summary_info.reset_index()


