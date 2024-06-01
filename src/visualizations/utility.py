import plotly.graph_objects as go

def update_fig_layout(fig: go.Figure, title: str = None, xaxis_title: str = None, yaxis_title: str = None, **kwargs):
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        template='plotly_white',
        **kwargs
    )
    return fig