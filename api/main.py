from fastapi import FastAPI, Query,Response
from contextlib import asynccontextmanager
import logging
from database.sql_connection_test import SQLiteConnection
from database.utility import run_query
from typing import List, Dict
from src.visualizations.Vis2 import update_figure, data, coins, START_DATE, RSI_TIME_WINDOW
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots




db_conn = SQLiteConnection(database="./test_db.db")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    response = db_conn.test_connection()
    if response["connection_status"] == "incomplete":
        raise Exception(response["message"])
    yield
    # Shutdown
    if db_conn._engine:
        db_conn._engine.dispose()
        logging.info("Database connection closed.")

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def root(): # Need to establish connection to database on connection to site
    return {"connection_status": 200}

@app.get('/query_coin')
async def query_coin(coin_names: List[str] = Query(...)) -> Dict:
    try:
        params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        print(query)
        df = run_query(query=query, connection=db_conn, params=params)
        json_response = df.to_json(orient="records")
        return {"transaction_state":200, "data":json_response}
    except Exception as e:
        main_error = "query_coin"
        sub_error = type(e).__name__  # Get the name of the error
        message = str(e)
        return {"transacation_state": 500, "error_state": {"error_loc": main_error, "sub_error": sub_error, "message": message}}



@app.get('/test')
async def visualize():
    try:
        # Define constants
        start_date = START_DATE

        # Plotting with Plotly
        fig = make_subplots(rows=2, cols=2, subplot_titles=(
            "Candlestick Chart", "Volume Traded", "Price Chart", "Relative Strength Index (RSI)"))

        # Initial empty traces
        fig.add_trace(go.Candlestick(), row=1, col=1)
        fig.add_trace(go.Bar(), row=1, col=2)
        fig.add_trace(go.Scatter(), row=2, col=1)
        fig.add_trace(go.Scatter(), row=2, col=1)
        fig.add_trace(go.Scatter(), row=2, col=1)
        fig.add_trace(go.Scatter(), row=2, col=2)
        fig.add_trace(go.Scatter(), row=2, col=2)
        fig.add_trace(go.Scatter(), row=2, col=2)

        # Initial plot
        initial_traces = update_figure(coins[0], start_date)
        for i, trace in enumerate(initial_traces):
            fig.data[i].update(trace)

        # Add dropdown menus for coins
        coin_buttons = []
        for coin in coins:
            new_traces = update_figure(coin, start_date)
            button = dict(
                label=coin,
                method="update",
                args=[{
                    "x": [trace.x for trace in new_traces],
                    "y": [trace.y if hasattr(trace, 'y') else None for trace in new_traces],
                    "open": [trace.open if hasattr(trace, 'open') else None for trace in new_traces],
                    "high": [trace.high if hasattr(trace, 'high') else None for trace in new_traces],
                    "low": [trace.low if hasattr(trace, 'low') else None for trace in new_traces],
                    "close": [trace.close if hasattr(trace, 'close') else None for trace in new_traces],
                }]
            )
            coin_buttons.append(button)

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=coin_buttons,
                    direction="down",
                    showactive=True,
                    x=0.0,
                    y=1.15,
                    xanchor='left',
                    yanchor='top'
                )
            ],
            title_text="Interactive Crypto Dashboard",
            showlegend=False,
            autosize=True,
            height=800
        )

        fig.add_annotation(
            text=f"Start Date: {START_DATE}",
            xref="paper", yref="paper",
            x=0.5, y=1.08,
            showarrow=False,
            font=dict(size=12, color="black")
        )

        fig_json = fig.to_json()

        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Plotly Graph</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                #plot {{
                    width: 90%;
                    height: 90%;
                }}
            </style>
        </head>
        <body>
            <div id="plot"></div>
            <script>
                var plot_data = {fig_json};
                Plotly.newPlot('plot', plot_data.data, plot_data.layout, {{responsive: true}});

                // Function to update the plot
                function updatePlot(coin) {{
                    Plotly.relayout('plot', {{
                        'yaxis.autorange': true,
                        'xaxis.autorange': true,
                        'yaxis2.autorange': true,
                        'xaxis2.autorange': true,
                        'yaxis3.autorange': true,
                        'xaxis3.autorange': true,
                        'yaxis4.autorange': true,
                        'xaxis4.autorange': true
                    }});
                }}

                // Handle dropdown change
                document.querySelector('select').addEventListener('change', function(e) {{
                    var coin = e.target.value;
                    updatePlot(coin);
                }});

                window.onresize = function() {{
                    Plotly.Plots.resize(document.getElementById('plot'));
                }};
            </script>
        </body>
        </html>
        """

        return Response(content=html_content, media_type="text/html")
    except Exception as e:
        logging.error(f"Exception: {e}")
        return {"error": str(e)}



