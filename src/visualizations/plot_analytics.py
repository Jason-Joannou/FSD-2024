import pandas as pd
import plotly.graph_objects as go
from typing import List, Any
from datetime import datetime
from .utility import update_fig_layout

def xy_plot(df: pd.DataFrame, x_column_name: str, y_column_name: str, graph_type: str) -> go.Figure:
    """
    Creates a graph based on the specified type.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        x_column_name (str): Column name for x-axis values.
        y_column_name (str): Column name for y-axis values.
        graph_type (str): Type of graph to create ('candlestick' or 'line').

    Returns:
        go.Figure: A Plotly Figure object.
    """
    if graph_type == "candlestick":
        pass
    elif graph_type == "line":
        fig = plot_line(df=df, x_column_name=x_column_name, y_column_name=y_column_name)
    else:
        pass
    return fig

# Define constants
START_DATE = "2010-10-05"  # static start date
START_DATE2 = "2018-06-06"
RSI_TIME_WINDOW = 7  # number of days

def computeRSI(data, time_window):
    """
    Computes the Relative Strength Index (RSI) for a given dataset and time window.

    Parameters:
        data (pd.Series): Series of prices.
        time_window (int): The period over which to calculate RSI.

    Returns:
        pd.Series: The RSI values.
    """
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
    """
    Plots a candlestick chart for each unique coin in the DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.

    Returns:
        go.Figure: A Plotly Figure object.
    """
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
    """
    Plots a line chart for each unique coin in the DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        x_column_name (str): Column name for x-axis values.
        y_column_name (str): Column name for y-axis values.

    Returns:
        go.Figure: A Plotly Figure object.
    """
    fig = go.Figure()
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Scatter(
            x=coin_df[x_column_name],
            y=coin_df[y_column_name],
            mode='lines+markers',
            name=f'{coin} {y_column_name}'
        ))

    return fig

def plot_bar(df: pd.DataFrame, x_column_name: str, y_column_name: str):
    """
    Plots a bar chart for each unique coin in the DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        x_column_name (str): Column name for x-axis values.
        y_column_name (str): Column name for y-axis values.

    Returns:
        go.Figure: A Plotly Figure object.
    """
    fig = go.Figure()
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Bar(
            x=coin_df[x_column_name],
            y=coin_df[y_column_name],
            name=f'{coin} {y_column_name}'
        ))

    return fig

def plot_pie(df: pd.DataFrame, names_column_name: str, values_column_name: str):
    """
    Plots a pie chart to show market share distribution.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        names_column_name (str): Column name for the labels.
        values_column_name (str): Column name for the values.

    Returns:
        go.Figure: A Plotly Figure object.
    """
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df[names_column_name],
        values=df[values_column_name],
        name='Market Share'
    ))
    fig.update_layout(title="Market Share Distribution")
    return fig

def plot_rsi(df: pd.DataFrame, x_column_name: str, y_column_name: str):
    """
    Plots the Relative Strength Index (RSI) for each unique coin in the DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        x_column_name (str): Column name for x-axis values.
        y_column_name (str): Column name for price values (used to calculate RSI).

    Returns:
        go.Figure: A Plotly Figure object.
    """
    df['RSI'] = df.groupby('Name')["Close"].transform(lambda x: computeRSI(x, RSI_TIME_WINDOW)) #changed [y_column_name] to  Close
    fig = go.Figure()
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Scatter(
            x=coin_df[x_column_name],
            y=coin_df['RSI'],
            mode='lines',
            name=f'{coin} RSI'
        ))
        
    return fig

def compute_and_plot_correlation_matrix(df: pd.DataFrame, price_column='Close'):
    #TODO Fix correlation function
    """
    Computes the percentage change in price for each coin in the DataFrame
    and plots a correlation matrix of these changes using Plotly.

    Parameters:
        df (pd.DataFrame): DataFrame containing price data for different coins.
        price_column (str): Column name for price values.

    Returns:
        go.Figure: A Plotly Figure object representing the correlation matrix heatmap.
    """
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure 'Date' column is datetime
    df.sort_values(['Name', 'Date'], inplace=True)  # Sort by 'Name' and 'Date' for correct calculations

    # Compute percentage change
    df['PriceChangePct'] = df.groupby('Name')[price_column].pct_change() * 100

    # Pivot to get percentage change as columns for each coin
    correlation_data = df.pivot(index='Date', columns='Name', values='PriceChangePct')

    # Compute correlation matrix
    correlation_matrix = correlation_data.corr()

    # Plotting the correlation matrix using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='Viridis'))

    fig.update_layout(
        title='Correlation Matrix of Price Change Percentage between Coins',
        xaxis_title='Coins',
        yaxis_title='Coins',
        xaxis_nticks=len(correlation_matrix.columns),
        yaxis_nticks=len(correlation_matrix.columns),
        width=800,
        height=600,
    )

    return fig
