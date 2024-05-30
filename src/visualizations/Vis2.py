import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define constants
START_DATE = "2010-10-05"  # static start date
RSI_TIME_WINDOW = 7  # number of days

def computeRSI(data, time_window):
    diff = data.diff(1).dropna()
    up_chg = 0 * diff
    down_chg = 0 * diff
    up_chg[diff > 0] = diff[diff > 0]
    down_chg[diff < 0] = diff[diff < 0]
    up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    rs = abs(up_chg_avg / down_chg_avg)
    rsi = 100 - 100 / (1 + rs)
    return rsi

# Load data from CSV file
data = pd.read_csv('coins.csv')
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data = data.dropna(subset=['Date'])

# List of unique coins
coins = data['Name'].unique()

def update_figure(coin, start_date):
    filtered_data = data[(data['Name'] == coin) & (data['Date'] >= pd.to_datetime(start_date))].copy()
    filtered_data['Close_RSI'] = computeRSI(filtered_data['Close'], RSI_TIME_WINDOW)
    # Normalize the volume data
    #max_volume = filtered_data['Volume'].max()
    #filtered_data['Volume_Normalized'] = filtered_data['Volume'] / max_volume * 100

    candlestick = go.Candlestick(x=filtered_data['Date'],
                                 open=filtered_data['Open'], high=filtered_data['High'],
                                 low=filtered_data['Low'], close=filtered_data['Close'])

    volume = go.Bar(x=filtered_data['Date'], y=filtered_data['Volume'], marker_color='blue',opacity=1)

    close_price = go.Scatter(x=filtered_data['Date'], y=filtered_data['Close'], mode='lines', name='Close Price',
                             line=dict(color='red'))

    high_price = go.Scatter(x=filtered_data['Date'], y=filtered_data['High'], mode='lines', name='High Price',
                            line=dict(color='pink', dash='dash'))

    low_price = go.Scatter(x=filtered_data['Date'], y=filtered_data['Low'], mode='lines', name='Low Price',
                           line=dict(color='pink', dash='dash'))

    rsi = go.Scatter(x=filtered_data['Date'], y=filtered_data['Close_RSI'], mode='lines', name='RSI',
                     line=dict(color='aquamarine'))

    low_rsi = go.Scatter(x=filtered_data['Date'], y=[30] * len(filtered_data), mode='lines', name='Low RSI',
                         line=dict(color='aqua', dash='dash'))

    high_rsi = go.Scatter(x=filtered_data['Date'], y=[70] * len(filtered_data), mode='lines', name='High RSI',
                          line=dict(color='aqua', dash='dash'))

    return [candlestick, volume, close_price, high_price, low_price, rsi, low_rsi, high_rsi]

# def plot_market_cap():
#     market_cap_data = data.groupby('Date')['Marketcap'].sum().reset_index()
#     market_cap_trace = go.Scatter(x=market_cap_data['Date'], y=market_cap_data['Marketcap'], mode='lines',
#                                   name='Market Cap', line=dict(color='blue'))
#     return market_cap_trace
#
# def plot_market_share(date):
#     market_share_data = data[data['Date'] == pd.to_datetime(date)].groupby('Name')['Marketcap'].sum().reset_index()
#     market_share_trace = go.Pie(labels=market_share_data['Name'], values=market_share_data['Marketcap'], name='Market Share')
#     return market_share_trace