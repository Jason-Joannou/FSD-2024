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
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    summary_info = df.groupby('Name').agg({
        'Date': ['min', 'max', 'count'],
        'Volume': 'sum',
        'Marketcap': 'mean'
    })

    # Rename columns
    summary_info.columns = ['Start Date', 'End Date', 'Number of Records', 'Total Volume', 'Average Market Cap']
    summary_info = summary_info.reset_index()

    # Format dates to 'YYYY-MM-DD'
    summary_info['Start Date'] = summary_info['Start Date'].dt.strftime('%Y-%m-%d')
    summary_info['End Date'] = summary_info['End Date'].dt.strftime('%Y-%m-%d')

    # Format 'Total Volume' and 'Average Market Cap' to human-readable format
    summary_info['Total Volume'] = summary_info['Total Volume'].apply(human_readable_format)
    summary_info['Average Market Cap'] = summary_info['Average Market Cap'].apply(human_readable_format)

    return summary_info

def human_readable_format(num):
    """Convert a large number to a human-readable format (e.g., 1.3B, 2.4M)."""
    if abs(num) >= 1_000_000_000:
        return f'{num / 1_000_000_000:.1f}B'
    elif abs(num) >= 1_000_000:
        return f'{num / 1_000_000:.1f}M'
    elif abs(num) >= 1_000:
        return f'{num / 1_000:.1f}K'
    else:
        return str(num)


