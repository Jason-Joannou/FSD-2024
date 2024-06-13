import pandas as pd
import plotly.graph_objects as go
from typing import List, Any
from datetime import datetime
from .utility import update_fig_layout

def xy_plot(df: pd.DataFrame, x_column_name: str, y_column_name: str, graph_type: str) -> go.Figure:
    if graph_type == "candlestick":
        pass
    elif graph_type == "line":
        fig = plot_line(df=df, x_column_name=x_column_name, y_column_name=y_column_name)
    else:
        pass
    # http://127.0.0.1:8000/query_coin_example?coin_names=Bitcoin&coin_names=Ethereum&coin_names=Cardano&graph_type=scatter
    # Add other graphs if needed

    return fig


# Define constants
START_DATE = "2010-10-05"  # static start date
START_DATE2 = "2018-06-06"
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


def plot_candlestick(df: pd.DataFrame):
    fig = go.Figure()
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Candlestick(
            x=coin_df['Date'],
            open=coin_df['Open'],
            high=coin_df['High'],
            low=coin_df['Low'],
            close=coin_df['Close'],
            name=f'{coin} Candlestick'
        ))
    return fig


def plot_line(df: pd.DataFrame, x_column_name: str, y_column_name: str):
    fig = go.Figure()
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Scatter(
            x=coin_df[x_column_name],
            y=coin_df[y_column_name],
            mode='lines+markers',
            name=f'{coin} {y_column_name}'
        ))
    fig.update_layout(title=f"Line graph of {y_column_name} over {x_column_name}", xaxis_title=x_column_name,
                      yaxis_title=y_column_name)

    return fig

def plot_bar(df: pd.DataFrame, x_column_name: str, y_column_name: str):
    fig = go.Figure()
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Bar(
            x=coin_df[x_column_name],
            y=coin_df[y_column_name],
            name=f'{coin} {y_column_name}'
        ))
        fig.update_layout(title=f"Bar graph of {y_column_name} over {x_column_name}", xaxis_title=x_column_name,
                      yaxis_title=y_column_name)
    return fig

def plot_pie(df: pd.DataFrame, names_column_name: str, values_column_name: str):
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df[names_column_name],
        values=df[values_column_name],
        name='Market Share'
    ))
    fig.update_layout(title="Market Share Distribution")
    return fig

def plot_rsi(df: pd.DataFrame, x_column_name: str, y_column_name: str):
    df['RSI'] = df.groupby('Name')[y_column_name].transform(lambda x: computeRSI(x, RSI_TIME_WINDOW))
    fig = go.Figure()
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Scatter(
            x=coin_df[x_column_name],
            y=coin_df['RSI'],
            mode='lines',
            name=f'{coin} RSI'
        ))
    fig.update_layout(title="Relative Strength Index (RSI)", xaxis_title=x_column_name, yaxis_title="RSI")
    return fig
