from fastapi import FastAPI, Query, HTTPException, Response, Depends
from sqlalchemy import text
from contextlib import asynccontextmanager
import logging
from database.sql_connection_test import SQLiteConnection
from database.utility import run_query
from typing import List, Dict
from src.analytics.data_reporting import coin_proportion, coin_summary_info
from src.visualizations.plot_reporting import plot_piechart, plot_switch, plot_summary_table
from .validation import UserCreate, UserLogin
import bcrypt
import json



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



