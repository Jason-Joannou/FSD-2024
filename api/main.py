from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
import logging
from src.analytics.functions import test_function
from database.sql_connection_test import SQLiteConnection
from database.utility import run_query
from typing import List, Dict



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
        