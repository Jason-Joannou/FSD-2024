from fastapi import FastAPI, Query, HTTPException, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
import json
import plotly.graph_objects as go
from typing import List, Union
from io import BytesIO
import logging

# Can also include ingestion api call to get kaggle datasets

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="FSD API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # All origins allowed for dev purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root() -> Response: # Need to establish connection to database on connection to site
    return Response(content=json.dumps({"message":"Welcome to the FSD public API",}), media_type="application/json")


@app.post('/line_graph')
async def plot_line_graph(
    x: List[Union[int, float, str]] = Body(...),
    y: List[Union[int, float]] = Body(...),
    x_axis_title: str = Body("X data"),
    y_axis_title: str = Body("Y data"),
    plot_title: str = Body("Simple Line Graph"),
    line_color: str = Body("blue"),
    marker_style: str = Body("circle"),
    html_embedding: bool = Body(False),
) -> Response:
    logging.debug("Received request with data: x=%s, y=%s", x, y)
    # Validate input lengths
    if len(x) != len(y):
        raise HTTPException(status_code=400, detail="Length of x and y must match.")

    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        line=dict(color=line_color),
        marker=dict(symbol=marker_style)
    ))

    fig.update_layout(
        title=plot_title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
    )

    if html_embedding:
        try:
            logging.debug("Attempting to write image...")
            fig_html = fig.to_html(full_html=False)
            logging.debug("Image Written")
        except Exception as e:
            logging.error(f"Error generating image bytes: {e}")
            raise HTTPException(status_code=500, detail="Image generation failed.")
        return StreamingResponse(content=BytesIO(fig_html.encode()), media_type="text/html")
    
    return JSONResponse(content=fig.to_dict())

@app.post('/bar_graph')
async def plot_bar_graph(
    x: List[Union[int, float, str]] = Body(...),
    y: List[Union[int, float]] = Body(...),
    x_axis_title: str = Body("X data"),
    y_axis_title: str = Body("Y data"),
    plot_title: str = Body("Simple Bar Graph"),
    bar_color: str = Body("blue"),
    html_embedding: bool = Body(False),
) -> Response:
    logging.debug("Received request with data: x=%s, y=%s", x, y)
    # Validate input lengths
    if len(x) != len(y):
        raise HTTPException(status_code=400, detail="Length of x and y must match.")

    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=y,
        marker=dict(color=bar_color)
    ))

    fig.update_layout(
        title=plot_title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
    )

    if html_embedding:
        try:
            logging.debug("Attempting to write image...")
            fig_html = fig.to_html(full_html=False)
            logging.debug("Image Written")
        except Exception as e:
            logging.error(f"Error generating image bytes: {e}")
            raise HTTPException(status_code=500, detail="Image generation failed.")
        return StreamingResponse(content=BytesIO(fig_html.encode()), media_type="text/html")
    
    return JSONResponse(content=fig.to_dict())

@app.post('/scatter_plot')
async def plot_scatter_plot(
    x: List[Union[int, float, str]] = Body(...),
    y: List[Union[int, float]] = Body(...),
    x_axis_title: str = Body("X data"),
    y_axis_title: str = Body("Y data"),
    plot_title: str = Body("Simple Scatter Plot"),
    point_color: str = Body("blue"),
    marker_style: str = Body("circle"),
    html_embedding: bool = Body(False),
) -> Response:
    logging.debug("Received request with data: x=%s, y=%s", x, y)
    if len(x) != len(y):
        raise HTTPException(status_code=400, detail="Length of x and y must match.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker=dict(color=point_color, symbol=marker_style)
    ))

    fig.update_layout(
        title=plot_title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
    )

    if html_embedding:
        try:
            logging.debug("Attempting to write image...")
            fig_html = fig.to_html(full_html=False)
            logging.debug("Image Written")
        except Exception as e:
            logging.error(f"Error generating image bytes: {e}")
            raise HTTPException(status_code=500, detail="Image generation failed.")
        return StreamingResponse(content=BytesIO(fig_html.encode()), media_type="text/html")
    
    return JSONResponse(content=fig.to_dict())

@app.post('/histogram')
async def plot_histogram(
    data: List[Union[int, float]] = Body(...),
    x_axis_title: str = Body("Values"),
    y_axis_title: str = Body("Frequency"),
    plot_title: str = Body("Sample Histogram"),
    bar_color: str = Body("blue"),
    html_embedding: bool = Body(False),
) -> Response:
    logging.debug("Received request with data: %s", data)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data,
        marker=dict(color=bar_color)
    ))

    fig.update_layout(
        title=plot_title,
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
    )

    if html_embedding:
        try:
            logging.debug("Attempting to write image...")
            fig_html = fig.to_html(full_html=False)
            logging.debug("Image Written")
        except Exception as e:
            logging.error(f"Error generating image bytes: {e}")
            raise HTTPException(status_code=500, detail="Image generation failed.")
        return StreamingResponse(content=BytesIO(fig_html.encode()), media_type="text/html")
    
    return JSONResponse(content=fig.to_dict())

@app.post('/pie_chart')
async def plot_pie_chart(
    labels: List[str] = Body(...),
    values: List[Union[int, float]] = Body(...),
    plot_title: str = Body("Simple Pie Chart"),
    html_embedding: bool = Body(False),
) -> Response:
    logging.debug("Received request with labels: %s and values: %s", labels, values)

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=labels, values=values))

    fig.update_layout(
        title=plot_title,
    )

    if html_embedding:
        try:
            logging.debug("Attempting to write image...")
            fig_html = fig.to_html(full_html=False)
            logging.debug("Image Written")
        except Exception as e:
            logging.error(f"Error generating image bytes: {e}")
            raise HTTPException(status_code=500, detail="Image generation failed.")
        return StreamingResponse(content=BytesIO(fig_html.encode()), media_type="text/html")
    
    return JSONResponse(content=fig.to_dict())






