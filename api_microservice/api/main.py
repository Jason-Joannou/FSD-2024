from fastapi import FastAPI, HTTPException, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
import json
import plotly.graph_objects as go
from pydantic import BaseModel
from typing import List, Union, Optional
from io import BytesIO
import logging

# Can also include ingestion api call to get kaggle datasets
# Query our database

class CalculationInput(BaseModel):
    principal: Optional[float] = None
    rate: Optional[float] = None
    time: Optional[int] = None
    n: Optional[int] = None
    annual_rate: Optional[float] = None
    num_payments: Optional[int] = None
    deposit: Optional[float] = None
    periods: Optional[int] = None
    current_savings: Optional[float] = None
    annual_contribution: Optional[float] = None
    years: Optional[int] = None
    income: Optional[float] = None
    goal_amount: Optional[float] = None
    months: Optional[int] = None
    monthly_expenses: Optional[float] = None

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
    """
    Returns a welcome message for the FSD public API.

    Returns:
        Response: A JSON response containing a welcome message.
    """
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
    """
    Generates a line graph based on the provided data.

    Args:
        x (List[Union[int, float, str]]): Data for the x-axis.
        y (List[Union[int, float]]): Data for the y-axis.
        x_axis_title (str): Title for the x-axis.
        y_axis_title (str): Title for the y-axis.
        plot_title (str): Title for the plot.
        line_color (str): Color of the line.
        marker_style (str): Style of the markers.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
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
    """
    Generates a bar graph based on the provided data.

    Args:
        x (List[Union[int, float, str]]): Data for the x-axis.
        y (List[Union[int, float]]): Data for the y-axis.
        x_axis_title (str): Title for the x-axis.
        y_axis_title (str): Title for the y-axis.
        plot_title (str): Title for the plot.
        bar_color (str): Color of the bars.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
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
    """
    Generates a scatter plot based on the provided data.

    Args:
        x (List[Union[int, float, str]]): Data for the x-axis.
        y (List[Union[int, float]]): Data for the y-axis.
        x_axis_title (str): Title for the x-axis.
        y_axis_title (str): Title for the y-axis.
        plot_title (str): Title for the plot.
        point_color (str): Color of the points.
        marker_style (str): Style of the markers.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
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
    """
    Generates a histogram based on the provided data.

    Args:
        data (List[Union[int, float]]): Data to be plotted in the histogram.
        x_axis_title (str): Title for the x-axis.
        y_axis_title (str): Title for the y-axis.
        plot_title (str): Title for the plot.
        bar_color (str): Color of the bars.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
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
    """
    Generates a pie chart based on the provided data.

    Args:
        labels (List[str]): Labels for the pie chart segments.
        values (List[Union[int, float]]): Values for each segment of the pie chart.
        plot_title (str): Title for the plot.
        colors (List[str]): List of colors for the pie segments.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
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

@app.post('/box_plot')
async def plot_box_plot(
    data: List[Union[int, float]] = Body(...),
    x_axis_title: str = Body("X Axis"),
    y_axis_title: str = Body("Y Axis"),
    plot_title: str = Body("Simple Box Plot"),
    box_color: str = Body("blue"),
    html_embedding: bool = Body(False),
) -> Response:
    """
    Generates a box plot based on the provided data.

    Args:
        data (List[Union[int, float]]): Data to be plotted in the box plot.
        x_axis_title (str): Title for the x-axis.
        y_axis_title (str): Title for the y-axis.
        plot_title (str): Title for the plot.
        box_color (str): Color of the box plot.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
    logging.debug("Received request with data: %s", data)

    fig = go.Figure()
    fig.add_trace(go.Box(y=data, marker=dict(color=box_color)))

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

@app.post('/heatmap')
async def plot_heatmap(
    x: List[str] = Body(...),
    y: List[str] = Body(...),
    z: List[List[float]] = Body(...),
    plot_title: str = Body("Sample Heatmap"),
    html_embedding: bool = Body(False),
) -> Response:
    """
    Generates a heatmap based on the provided data.

    Args:
        x (List[str]): Data for the x-axis.
        y (List[str]): Data for the y-axis.
        z (List[List[float]]): Data for the heatmap values.
        plot_title (str): Title for the plot.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
    logging.debug("Received request with x: %s, y: %s", x, y)

    fig = go.Figure()
    fig.add_trace(go.Heatmap(x=x, y=y, z=z))

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

@app.post('/area_chart')
async def plot_area_chart(
    x: List[Union[int, float, str]] = Body(...),
    y: List[Union[int, float]] = Body(...),
    x_axis_title: str = Body("X Values"),
    y_axis_title: str = Body("Y Values"),
    plot_title: str = Body("Simple Area Chart"),
    fill_color: str = Body("lightblue"),
    html_embedding: bool = Body(False),
) -> Response:
    """
    Generates an area chart based on the provided data.

    Args:
        x (List[Union[int, float, str]]): Data for the x-axis.
        y (List[Union[int, float]]): Data for the y-axis.
        x_axis_title (str): Title for the x-axis.
        y_axis_title (str): Title for the y-axis.
        plot_title (str): Title for the plot.
        fill_color (str): Color for the filled area.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
    logging.debug("Received request with data: x=%s, y=%s", x, y)
    if len(x) != len(y):
        raise HTTPException(status_code=400, detail="Length of x and y must match.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        fill='tozeroy',
        line=dict(color=fill_color)
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

@app.post('/bubble_chart')
async def plot_bubble_chart(
    x: List[Union[int, float, str]] = Body(...),
    y: List[Union[int, float]] = Body(...),
    sizes: List[Union[int, float]] = Body(...),
    x_axis_title: str = Body("X Values"),
    y_axis_title: str = Body("Y Values"),
    plot_title: str = Body("Simple Bubble Chart"),
    html_embedding: bool = Body(False),
) -> Response:
    """
    Generates a bubble chart based on the provided data.

    Args:
        x (List[Union[int, float, str]]): Data for the x-axis.
        y (List[Union[int, float]]): Data for the y-axis.
        sizes (List[Union[int, float]]): Sizes of the bubbles.
        x_axis_title (str): Title for the x-axis.
        y_axis_title (str): Title for the y-axis.
        plot_title (str): Title for the plot.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
    logging.debug("Received request with data: x=%s, y=%s", x, y)
    if len(x) != len(y) or len(x) != len(sizes):
        raise HTTPException(status_code=400, detail="Length of x, y, and sizes must match.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker=dict(size=sizes)
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

@app.post('/candlestick_chart')
async def plot_candlestick_chart(
    dates: List[str] = Body(...),
    open: List[float] = Body(...),
    high: List[float] = Body(...),
    low: List[float] = Body(...),
    close: List[float] = Body(...),
    plot_title: str = Body("Simple Candlestick Chart"),
    html_embedding: bool = Body(False),
) -> Response:
    """
    Generates a candlestick chart based on the provided financial data.

    Args:
        dates (List[str]): Dates for the x-axis.
        open (List[float]): Opening prices.
        high (List[float]): Highest prices.
        low (List[float]): Lowest prices.
        close (List[float]): Closing prices.
        plot_title (str): Title for the plot.
        html_embedding (bool): If True, returns the plot as HTML.

    Returns:
        Response: The plot as JSON, HTML, or an error message.
    """
    logging.debug("Received request with dates: %s", dates)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dates,
        open=open,
        high=high,
        low=low,
        close=close
    ))

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

@app.post("/calculate_compound_interest")
def calculate_compound_interest(data: CalculationInput):
    """
    Calculate compound interest based on the given parameters.

    Parameters:
    - principal (float): The initial amount of money.
    - rate (float): The annual interest rate (decimal).
    - time (int): The time the money is invested for, in years.
    - n (int): The number of times that interest is compounded per year.

    Returns:
    - JSONResponse: The amount of money accumulated after the specified time, including interest.
    """
    if not all([data.principal, data.rate, data.time, data.n]):
        return JSONResponse(content={"error": "Missing required fields"}, status_code=400)
    
    A = data.principal * (1 + data.rate / data.n) ** (data.n * data.time)
    return JSONResponse(content={"amount": A})

@app.post("/calculate_loan_payments")
def calculate_loan_payments(data: CalculationInput):
    """
    Calculate monthly loan payments based on the given parameters.

    Parameters:
    - principal (float): The amount of the loan.
    - annual_rate (float): The annual interest rate (percentage).
    - num_payments (int): The number of monthly payments.

    Returns:
    - JSONResponse: The monthly payment amount.
    """
    if not all([data.principal, data.annual_rate, data.num_payments]):
        return JSONResponse(content={"error": "Missing required fields"}, status_code=400)
    
    monthly_rate = data.annual_rate / 12 / 100
    payment = (data.principal * monthly_rate) / (1 - (1 + monthly_rate) ** (-data.num_payments))
    return JSONResponse(content={"monthly_payment": payment})

@app.post("/calculate_savings_growth")
def calculate_savings_growth(data: CalculationInput):
    """
    Calculate the future value of savings based on the given parameters.

    Parameters:
    - deposit (float): The initial deposit amount.
    - rate (float): The annual interest rate (decimal).
    - periods (int): The number of periods.

    Returns:
    - JSONResponse: The future value of the savings.
    """
    if not all([data.deposit, data.rate, data.periods]):
        return JSONResponse(content={"error": "Missing required fields"}, status_code=400)
    
    future_value = data.deposit * (((1 + data.rate) ** data.periods - 1) / data.rate)
    return JSONResponse(content={"future_value": future_value})

@app.post("/calculate_retirement_savings")
def calculate_retirement_savings(data: CalculationInput):
    """
    Calculate total retirement savings based on the given parameters.

    Parameters:
    - current_savings (float): The current amount of retirement savings.
    - annual_contribution (float): The annual contribution to the retirement account.
    - rate (float): The annual interest rate (decimal).
    - years (int): The number of years the money is invested.

    Returns:
    - JSONResponse: The total amount of retirement savings.
    """
    if not all([data.current_savings, data.annual_contribution, data.rate, data.years]):
        return JSONResponse(content={"error": "Missing required fields"}, status_code=400)
    
    future_value = data.current_savings * (1 + data.rate) ** data.years
    future_value += data.annual_contribution * (((1 + data.rate) ** data.years - 1) / data.rate)
    return JSONResponse(content={"total_savings": future_value})

@app.post("/calculate_savings_rate")
def calculate_savings_rate(data: CalculationInput):
    """
    Calculate the savings rate required to reach a financial goal.

    Parameters:
    - income (float): The monthly income.
    - goal_amount (float): The savings goal amount.
    - months (int): The number of months to save.
    - rate (float): The annual interest rate (decimal).

    Returns:
    - JSONResponse: The required savings rate as a percentage of income.
    """
    if not all([data.income, data.goal_amount, data.months, data.rate]):
        return JSONResponse(content={"error": "Missing required fields"}, status_code=400)
    
    monthly_savings_needed = data.goal_amount / data.months
    savings_rate = (monthly_savings_needed / data.income) * 100
    return JSONResponse(content={"savings_rate": savings_rate})

@app.post("/estimate_emergency_fund")
def estimate_emergency_fund(data: CalculationInput):
    """
    Estimate the amount needed for an emergency fund.

    Parameters:
    - monthly_expenses (float): The monthly expenses.
    - months (int): The number of months to cover with the emergency fund.

    Returns:
    - JSONResponse: The estimated emergency fund amount.
    """
    if not all([data.monthly_expenses, data.months]):
        return JSONResponse(content={"error": "Missing required fields"}, status_code=400)
    
    emergency_fund = data.monthly_expenses * data.months
    return JSONResponse(content={"emergency_fund": emergency_fund})
    









