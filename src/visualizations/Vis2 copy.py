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

# Plotting with Plotly
fig = make_subplots(rows=2, cols=2, subplot_titles=(
    "Candlestick Chart", "Volume Traded", "Price Chart", "Relative Strength Index (RSI)"))

# Initial empty traces
fig.add_trace(go.Candlestick(), row=1, col=1)
fig.add_trace(go.Bar(), row=1, col=2)
fig.add_trace(go.Scatter(), row=2, col=1)
fig.add_trace(go.Scatter(), row=2, col=1)
fig.add_trace(go.Scatter(), row=2, col=1)
fig.add_trace(go.Scatter(), row=2, col=2)
fig.add_trace(go.Scatter(), row=2, col=2)
fig.add_trace(go.Scatter(), row=2, col=2)


def update_figure(coin, start_date):
    filtered_data = data[(data['Name'] == coin) & (data['Date'] >= pd.to_datetime(start_date))].copy()
    filtered_data['Close_RSI'] = computeRSI(filtered_data['Close'], RSI_TIME_WINDOW)

    candlestick = go.Candlestick(x=filtered_data['Date'],
                                 open=filtered_data['Open'], high=filtered_data['High'],
                                 low=filtered_data['Low'], close=filtered_data['Close'])

    volume = go.Bar(x=filtered_data['Date'], y=filtered_data['Volume'], marker_color='aqua')

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


# Initial plot
initial_traces = update_figure(coins[0], START_DATE)
for i, trace in enumerate(initial_traces):
    fig.data[i].update(trace)


# Add dropdown menus for coins
coin_buttons = []
for coin in coins:
    new_traces = update_figure(coin, START_DATE)
    button = dict(
        label=coin,
        method="update",
        args=[{
            "x": [trace.x for trace in new_traces],
            "y": [trace.y if hasattr(trace, 'y') else None for trace in new_traces],
            "open": [trace.open if hasattr(trace, 'open') else None for trace in new_traces],
            "high": [trace.high if hasattr(trace, 'high') else None for trace in new_traces],
            "low": [trace.low if hasattr(trace, 'low') else None for trace in new_traces],
            "close": [trace.close if hasattr(trace, 'close') else None for trace in new_traces],
        }]
    )
    coin_buttons.append(button)

fig.update_layout(
    updatemenus=[
        dict(
            buttons=coin_buttons,
            direction="down",
            showactive=True,
            x=0.0,
            y=1.15,
            xanchor='left',
            yanchor='top'
        )
    ]
)

# Add annotation for static start date
fig.add_annotation(
    text=f"Start Date: {START_DATE}",
    xref="paper", yref="paper",
    x=0.5, y=1.08,
    showarrow=False,
    font=dict(size=12, color="black")
)

fig.update_layout(title_text="Interactive Dashboard", showlegend=False)
fig.show()
