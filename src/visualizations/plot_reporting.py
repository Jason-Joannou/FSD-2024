import pandas as pd
import plotly.graph_objects as go
from .utility import update_fig_layout
import numpy as np

def plot_histogram(df: pd.DataFrame, coin_name: str, x_column_name: str, num_bins: int = 50) -> go.Figure:
    df = df[df["Name"] == coin_name]
    density_line = np.histogram(df[x_column_name], bins=num_bins, density=True)
    x_density, y_density = density_line[1], density_line[0]

    median_line = np.median(df[x_column_name])

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df[x_column_name], histnorm='probability density', name='Histogram', nbinsx=num_bins))

    fig.add_trace(go.Scatter(x=x_density, y=y_density, mode='lines', name='Density'))

    fig.add_shape(type="line", x0=median_line, y0=0, x1=median_line, y1=max(y_density),
                  line=dict(color="red", width=2, dash="dot"), name="Median")

    fig = update_fig_layout(fig=fig, title=f"Histogram of {x_column_name} for {coin_name}",
                            xaxis_title=x_column_name, yaxis_title="Density")

    return fig

def plot_boxplots(df: pd.DataFrame, coin_name: str) -> go.Figure:
    df = df[df["Name"] == coin_name]
    numeric_cols = df.select_dtypes(include=['number']).columns
    fig = go.Figure()
    for col in numeric_cols:
        fig.add_trace(go.Box(y=df[col], name=col))
    fig = update_fig_layout(fig=fig, title=f"Box plots of numeric columns for {coin_name}", xaxis_title="Fields", yaxis_title="Values")
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

def plot_switch(graph_type: str, coin_name: str, df: pd.DataFrame, x_column_name: str = "Close") -> go.Figure:
    if graph_type == "histogram":
        fig = plot_histogram(df=df, coin_name=coin_name, x_column_name=x_column_name)
    elif graph_type == "boxplot":
        fig = plot_boxplots(df=df, coin_name=coin_name)
    else:
        fig = go.Figure()

    return fig
