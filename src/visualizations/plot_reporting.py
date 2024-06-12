import pandas as pd
import plotly.graph_objects as go
from .utility import update_fig_layout
import numpy as np

def plot_boxplots(df: pd.DataFrame, coin_name: str) -> go.Figure:
    df = df[df["Name"] == coin_name]
    numeric_cols = df.select_dtypes(include=['number']).columns
    fig = go.Figure()
    for col in numeric_cols:
        fig.add_trace(go.Box(y=df[col], name=col))
    fig = update_fig_layout(fig=fig, title=f"Box plots of numeric columns for {coin_name}", xaxis_title="Fields", yaxis_title="Values")
    return fig

def plot_summary_table(summary_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Table(
    header=dict(values=list(summary_df.columns), fill_color='lightblue', align='center'),
    cells=dict(values=[summary_df[col] for col in summary_df.columns], fill_color='lightcyan', align='center')))

    return fig

def plot_piechart(coin_counts: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=coin_counts.index, values=coin_counts.values, hole=.3))
    fig = update_fig_layout(fig=fig, title="Percentage of Coins in the Dataset")
    return fig


def plot_barchart(date_ranges: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    for coin in date_ranges.index:
        fig.add_trace(go.Bar(
            x=[coin],
            y=[(date_ranges.loc[coin, 'max'] - date_ranges.loc[coin, 'min']).days],
            name=coin,
            text=f"{date_ranges.loc[coin, 'min'].date()} to {date_ranges.loc[coin, 'max'].date()}",
            hoverinfo='text',
            orientation='v'
        ))

    fig = update_fig_layout(fig=fig, title="Date range for each coin", xaxis_title="Coin", yaxis_title="Date range (days)", showlegend=False)
    return fig

def plot_switch(graph_type: str, coin_name: str, df: pd.DataFrame) -> go.Figure:
    if graph_type == "boxplot":
        fig = plot_boxplots(df=df, coin_name=coin_name)
    else:
        fig = go.Figure()

    return fig
