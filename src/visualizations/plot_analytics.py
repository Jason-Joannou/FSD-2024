import pandas as pd
import plotly.graph_objects as go
from typing import List, Any
from datetime import datetime
from .utility import update_fig_layout

def xy_plot(df: pd.DataFrame, x_column_name: str, y_column_name: str, graph_type: str, **kwargs) -> go.Figure:
    fig = go.Figure()
    if graph_type == "candlestick":
        pass
    elif graph_type == "scatter":
        for coin in df["Name"].unique():
            coin_df = df[df["Name"] == coin]
            fig.add_trace(go.Scatter(
            x=coin_df[x_column_name], 
            y=coin_df[y_column_name], 
            mode='lines+markers', 
            name=f'{coin} Daily Price Change'))
    else:
        pass
    # Line plots are simple x, y plots
    # http://127.0.0.1:8000/query_coin_example?coin_names=Bitcoin&coin_names=Ethereum&coin_names=Cardano&graph_type=scatter

    return fig

