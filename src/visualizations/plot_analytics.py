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


def plot_candlestick():
    pass

def plot_line(df: pd.DataFrame, x_column_name: str, y_column_name: str):
    fig = go.Figure()
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Scatter(
        x=coin_df[x_column_name], 
        y=coin_df[y_column_name], 
        mode='lines+markers', 
        name=f'{coin} Daily Price Change'))

    fig = update_fig_layout(fig=fig, title=f"Line graph of {y_column_name} over {x_column_name}", xaxis_title=x_column_name, yaxis_title=y_column_name)
    
    return fig

def plot_volume():
    pass

def plot_heatmap():
    pass