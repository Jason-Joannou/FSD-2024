from fastapi import FastAPI, Query, HTTPException, Response
from contextlib import asynccontextmanager
import logging
from database.sql_connection_test import SQLiteConnection
from database.utility import run_query
from typing import List, Dict
from src.analytics.data_reporting import coin_proportion, coin_summary_info
from src.visualizations.plot_reporting import plot_piechart, plot_switch, plot_summary_table
import json



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
        df = run_query(query=query, connection=db_conn, params=params)
        json_response = df.to_json(orient="records")
        return {"transaction_state":200, "data":json_response}
    except Exception as e:
        main_error = "query_coin"
        sub_error = type(e).__name__  # Get the name of the error
        message = str(e)
        return {"transacation_state": 500, "error_state": {"error_loc": main_error, "sub_error": sub_error, "message": message}}
    

@app.get('/coin_reporting') # We will include pie chart with every response
async def coin_report(coin_name: str = Query(None), graph_type: str = Query(...)) -> Response:
    query = f"SELECT * FROM CoinsTable WHERE NAME = '{coin_name}'"
    df = run_query(query=query, connection=db_conn)
    fig = plot_switch(graph_type=graph_type, coin_name=coin_name, df=df)
    fig.show()
    fig_json = fig.to_json()

    # Return the JSON responses
    # http://127.0.0.1:8000/coin_reporting?coin_name=Aave&graph_type=boxplot
    return Response(content=json.dumps({"transaction":200, "data":{"graph": fig_json}}), media_type="application/json")


@app.get('/coin_proportion')
async def coin_proportions() -> Response:
    query = f"SELECT * FROM CoinsTable"
    df = run_query(query=query, connection=db_conn)
    coin_proportions = coin_proportion(df=df)
    summary_df = coin_summary_info(df=df)
    fig_summary = plot_summary_table(summary_df=summary_df)
    fig_pie = plot_piechart(coin_counts=coin_proportions)
    fig_summary.show()
    fig_pie.show()
    fig_pie_json = fig_pie.to_json()
    fig_summary_json = fig_summary.to_json()
    # http://127.0.0.1:8000/coin_proportion
    return Response(content=json.dumps({"transaction":200, "data":{"pie_graph": fig_pie_json, "summary_graph":fig_summary_json}}), media_type="application/json")


