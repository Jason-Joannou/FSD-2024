import plotly.graph_objects as go

def update_fig_layout(fig: go.Figure, title: str = "Plot Name", xaxis_title: str = "Axis title", yaxis_title: str = "Axis tile", **kwargs):
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        template='plotly_white',
        **kwargs
    )
    return fig