import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define constants
START_DATE = "2020-10-05"  # start date for historical data
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
data = pd.read_csv('coin_Aave.csv')
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Convert 'Date' column to datetime, handle invalid dates

# Drop rows with NaN or Inf in the 'Date' column
data = data.dropna(subset=['Date'])

# Filter data based on START_DATE
data = data[data['Date'] > START_DATE]

# Compute RSI
data['Close_RSI'] = computeRSI(data['Close'], RSI_TIME_WINDOW)
data['High_RSI'] = 30
data['Low_RSI'] = 70

# Plotting with Plotly Express
fig = make_subplots(rows=2, cols=2, subplot_titles=("Candlestick Chart", "Volume Traded", "Price Chart", "Relative Strength Index (RSI)"))

# Candlestick Chart
fig.add_trace(go.Candlestick(x=data['Date'],
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close']),
                row=1, col=1)
fig.update_xaxes(title_text="Date", row=1, col=1)
fig.update_yaxes(title_text="Price", row=1, col=1)

# Volume Traded
fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], marker_color='aqua'),
              row=1, col=2)
fig.update_xaxes(title_text="Date", row=1, col=2)
fig.update_yaxes(title_text="Volume", row=1, col=2)

# Price Chart
fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price', line=dict(color='red')),
              row=2, col=1)
fig.add_trace(go.Scatter(x=data['Date'], y=data['High'], mode='lines', name='High Price', line=dict(color='pink', dash='dash')),
              row=2, col=1)
fig.add_trace(go.Scatter(x=data['Date'], y=data['Low'], mode='lines', name='Low Price', line=dict(color='pink', dash='dash')),
              row=2, col=1)
fig.update_xaxes(title_text="Date", row=2, col=1)
fig.update_yaxes(title_text="Price", row=2, col=1)

# RSI
fig.add_trace(go.Scatter(x=data['Date'], y=data['Close_RSI'], mode='lines', name='RSI', line=dict(color='aquamarine')),
              row=2, col=2)
fig.add_trace(go.Scatter(x=data['Date'], y=[30]*len(data), mode='lines', name='Low RSI', line=dict(color='aqua', dash='dash')),
              row=2, col=2)
fig.add_trace(go.Scatter(x=data['Date'], y=[70]*len(data), mode='lines', name='High RSI', line=dict(color='aqua', dash='dash')),
              row=2, col=2)
fig.update_xaxes(title_text="Date", row=2, col=2)
fig.update_yaxes(title_text="RSI", row=2, col=2)

fig.update_layout(title_text="Interactive Dashboard FSD Group 2 2024", showlegend=False)
fig.show()
