import pandas as pd
import numpy as np
import plotly.graph_objects as go

def initialize_plot() -> go.Figure:
    return go.Figure()

def plot_base_outcome(df: pd.DataFrame, x_column_name: str, y_column_name: str, fig: go.Figure) -> go.Figure:
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Scatter(
            x=coin_df[x_column_name],
            y=coin_df[y_column_name],
            mode='lines+markers',
            name=f'{coin} {y_column_name}'
        ))

    return fig

def plot_predicted_outcome(df: pd.DataFrame, x_column_name: str, y_column_name: str, fig: go.Figure) -> go.Figure:
    for coin in df["Name"].unique():
        coin_df = df[df["Name"] == coin]
        fig.add_trace(go.Scatter(
            x=coin_df[x_column_name],
            y=coin_df[y_column_name],
            mode='lines+markers',
            name=f'{coin} {y_column_name} prediction'
        ))

    return fig