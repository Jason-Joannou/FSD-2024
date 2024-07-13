from fastapi import FastAPI, Query, HTTPException, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from contextlib import asynccontextmanager
import logging
from database.sql_connection_test import SQLiteConnection
from database.utility import run_query
from typing import List, Dict
from src.analytics.data_reporting import coin_proportion, coin_summary_info
from src.analytics.analytical_functions import daily_price_change, daily_price_range, moving_average, find_peaks_and_valleys, correlation_analysis
from src.visualizations.plot_reporting import plot_piechart, plot_switch, plot_summary_table, plot_boxplots
from src.visualizations.plot_analytics import plot_line  # Importing the custom plot function
from .validation import UserCreate, UserLogin
import bcrypt
import json
import plotly.express as px



db_conn = SQLiteConnection(database="./test_db.db")

def get_db_session():
    db = db_conn.get_session()
    try:
        yield db
    finally:
        db.close()

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

# Add CORS middleware
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # All origins allowed for dev purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    


@app.get('/daily_price_change')
async def get_daily_price_change(coin_names: List[str] = Query(...)) -> Dict:
    try:
        params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        df = run_query(query=query, connection=db_conn, params=params)
        df = daily_price_change(df)
        fig = plot_line(df=df, x_column_name='Date', y_column_name='DailyPriceChangeClosing')

        fig_json = fig.to_json()
        return {"transaction_state": 200, "data": fig_json}
    except Exception as e:
        return {"transaction_state": 500, "error": str(e)}


@app.get('/daily_price_range')
async def get_daily_price_range(coin_names: List[str] = Query(...)) -> Dict:
    try:
        params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        df = run_query(query=query, connection=db_conn, params=params)
        df = daily_price_range(df)
        fig = plot_line(df=df, x_column_name='Date', y_column_name='DailyPriceRange')

        fig_json = fig.to_json()
        return {"transaction_state": 200, "data": fig_json}
    except Exception as e:
        return {"transaction_state": 500, "error": str(e)}
    
@app.get('/moving_averages')
async def get_moving_averages(coin_names: List[str] = Query(...), window: int = Query(5)) -> Dict:
    try:
        params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        df = run_query(query=query, connection=db_conn, params=params)
        df = moving_average(df, window=window)
        fig = plot_line(df=df, x_column_name='Date', y_column_name=f'MovingAverage_{window}')
        fig_json = fig.to_json()
        return {"transaction_state": 200, "data": fig_json}
    except Exception as e:
        return {"transaction_state": 500, "error": str(e)}

#need visualisation tool
@app.get('/correlation_analysis')
async def get_correlation_analysis(coin_names: List[str] = Query(...)) -> Dict:
    #TODO Fix correlation anaylsis endpoint
    try:
        params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        df = run_query(query=query, connection=db_conn, params=params)
        correlation_matrix = correlation_analysis(df)
        fig = px.imshow(correlation_matrix, text_auto=True, title='Correlation Analysis')
        fig.show()
        fig_json = fig.to_json()
        return {"transaction_state": 200, "data": fig_json}
    except Exception as e:
        return {"transaction_state": 500, "error": str(e)}


@app.get('/coin_reporting') # We will include pie chart with every response
async def coin_report(coin_name: str = Query("Bitcoin")) -> Response:
    query = f"SELECT * FROM CoinsTable WHERE NAME = '{coin_name}'"
    df = run_query(query=query, connection=db_conn)
    fig = plot_boxplots(df=df, coin_name=coin_name)
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
    fig_pie_json = fig_pie.to_json()
    fig_summary_json = fig_summary.to_json()
    # http://127.0.0.1:8000/coin_proportion
    return Response(content=json.dumps({"transaction":200, "data":{"pie_graph": fig_pie_json, "summary_graph":fig_summary_json}}), media_type="application/json")

@app.post("/register/")
def register_user(user: UserCreate, db=Depends(get_db_session)):
    try:
        # Start a transaction
        with db.begin():
            # Check if the username already exists
            query_username = text("SELECT id FROM users WHERE username = :username")
            result_username = db.execute(query_username, {"username": user.username}).fetchone()
            if result_username:
                raise HTTPException(status_code=400, detail="Username already exists")
            
            # Check if the email already exists
            query_email = text("SELECT id FROM users WHERE email = :email")
            result_email = db.execute(query_email, {"email": user.email}).fetchone()
            if result_email:
                raise HTTPException(status_code=400, detail="Email already exists")
            
            # Hash the password
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert the user into the database
            query_insert = text("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)")
            db.execute(query_insert, {"username": user.username, "email": user.email, "password": hashed_password})
            
            db.commit()
        
        return {"message": "User registered successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/login/")
def login_user(user: UserLogin, db=Depends(get_db_session)):
    try:
        query = text("SELECT * FROM users WHERE username = :username")
        result = db.execute(query, {"username": user.username}).fetchone()
        
        if result and bcrypt.checkpw(user.password.encode('utf-8'), result[3].encode('utf-8')):  # Assuming password is the 4th column (index 3)
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
