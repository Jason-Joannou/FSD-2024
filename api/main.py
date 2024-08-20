from fastapi import FastAPI, Query, HTTPException, Response, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from contextlib import asynccontextmanager
import logging
from database.sql_connection_test import SQLiteConnection
from database.utility import run_query, run_updated_query
from typing import List, Dict, Optional
from src.analytics.data_reporting import coin_proportion, coin_summary_info
from src.analytics.analytical_functions import daily_price_change, daily_price_range, moving_average, find_peaks_and_valleys, correlation_analysis
from src.visualizations.plot_reporting import plot_piechart, plot_switch, plot_summary_table, plot_boxplots
from src.visualizations.plot_analytics import plot_line, plot_candlestick, plot_rsi, plot_bar # Importing the custom plot function
from ml.main import load_regression_model
from .validation import UserCreate, UserLogin, UsernameUpdate, EmailUpdate, PasswordUpdate
import requests
from bs4 import BeautifulSoup
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

@app.get('/get_coin_names')
async def get_coin_names():
    try:
        query = "SELECT DISTINCT Name FROM CoinsTable"
        df = run_query(query=query, connection=db_conn)
        json_response = df.to_json(orient="records")
        return {"transaction_state":200, "data":json_response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
async def get_daily_price_change(coin_names: List[str] = Query(...), start_date: str = Query(...), end_date: str = Query(...)) -> Response:
    try:
        # params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        # placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        # query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        # df = run_query(query=query, connection=db_conn, params=params)
        df = run_updated_query(coin_names=coin_names, start_date=start_date, end_date=end_date, connection=db_conn)
        df = daily_price_change(df)
        fig = plot_line(df=df, x_column_name='Date', y_column_name='DailyPriceChangeClosing')

        fig_json = fig.to_json()
        return Response(content=json.dumps({"transaction":200, "data":{"graph": fig_json}}), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/daily_price_range')
async def get_daily_price_range(coin_names: List[str] = Query(...), start_date: str = Query(...), end_date: str = Query(...)) -> Dict:
    try:
        # params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        # placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        # query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        # df = run_query(query=query, connection=db_conn, params=params)
        df = run_updated_query(coin_names=coin_names, start_date=start_date, end_date=end_date, connection=db_conn)
        df = daily_price_range(df)
        fig = plot_line(df=df, x_column_name='Date', y_column_name='DailyPriceRange')

        fig_json = fig.to_json()
        return Response(content=json.dumps({"transaction":200, "data":{"graph": fig_json}}), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get('/moving_averages')
async def get_moving_averages(coin_names: List[str] = Query(...), start_date: str = Query(...), end_date: str = Query(...), window: int = Query(5)) -> Dict:
    try:
        # params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        # placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        # query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        # df = run_query(query=query, connection=db_conn, params=params)
        df = run_updated_query(coin_names=coin_names, start_date=start_date, end_date=end_date, connection=db_conn)
        df = moving_average(df, window=window)
        fig = plot_line(df=df, x_column_name='Date', y_column_name=f'MovingAverage_{window}')
        fig_json = fig.to_json()
        return Response(content=json.dumps({"transaction":200, "data":{"graph": fig_json}}), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#need visualisation tool
@app.get('/correlation_analysis')
async def get_correlation_analysis(coin_names: List[str] = Query(...), start_date: str = Query(...), end_date: str = Query(...)) -> Dict:
    #TODO Fix correlation anaylsis endpoint
    try:
        # params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        # placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        # query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        # df = run_query(query=query, connection=db_conn, params=params)
        df = run_updated_query(coin_names=coin_names, start_date=start_date, end_date=end_date, connection=db_conn)
        correlation_matrix = correlation_analysis(df)
        fig = px.imshow(correlation_matrix, text_auto=True, title='Correlation Analysis')
        fig_json = fig.to_json()
        return Response(content=json.dumps({"transaction":200, "data":{"graph": fig_json}}), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/coin_reporting') # We will include pie chart with every response
async def coin_report(coin_name: str = Query("Bitcoin")) -> Response:
    query = f"SELECT * FROM CoinsTable WHERE NAME = '{coin_name}'"
    df = run_query(query=query, connection=db_conn)
    fig_other, fig_market, fig_volume = plot_boxplots(df=df, coin_name=coin_name)
    fig_other_json = fig_other.to_json()
    fig_market_json = fig_market.to_json()
    fig_volume_json = fig_volume.to_json()


    # Return the JSON responses
    # http://127.0.0.1:8000/coin_reporting?coin_name=Aave&graph_type=boxplot
    return Response(content=json.dumps({"transaction":200, "data":{"graph_other": fig_other_json, "graph_market": fig_market_json, "graph_volume": fig_volume_json}}), media_type="application/json")


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
async def register_user(user: UserCreate, db=Depends(get_db_session)):
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
async def login_user(user: UserLogin, db=Depends(get_db_session)):
    try:
        query = text("SELECT * FROM users WHERE username = :username")
        result = db.execute(query, {"username": user.username}).fetchone()
        
        if result and bcrypt.checkpw(user.password.encode('utf-8'), result[3].encode('utf-8')):  # Assuming password is the 4th column (index 3)
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/update_username/")
async def update_username(user_info: UsernameUpdate, db=Depends(get_db_session)):
    try:
        update_query = text("""
            UPDATE users
            SET username = :new_username
            WHERE username = :old_username
        """)
        db.execute(update_query, {"new_username": user_info.new_username, "old_username": user_info.old_username})
        db.commit()
        
        return {"message": "User information updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/update_useremail/")
async def update_useremail(user_info: EmailUpdate, db=Depends(get_db_session)):
    try:
        update_query = text("""
            UPDATE users
            SET email = :new_email
            WHERE username = :username
        """)
        db.execute(update_query, {"new_email": user_info.new_email, "username": user_info.username})
        db.commit()
        
        return {"message": "User information updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/update_password/")
async def update_password(user_info: PasswordUpdate, db=Depends(get_db_session)):
    try:
        # Authenticate user with the current password
        query = text("SELECT password FROM users WHERE username = :username")
        result = db.execute(query, {"username": user_info.username}).fetchone()
        if not result or not bcrypt.checkpw(user_info.current_password.encode('utf-8'), result[0].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid current password")
        
        if user_info.new_password != user_info.confirm_password:
            raise HTTPException(status_code=400, detail="New passwords do not match")
        
        # Hash the new password
        new_hashed_password = bcrypt.hashpw(user_info.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update the user's password in the database
        update_query = text("""
            UPDATE users
            SET password = :new_password
            WHERE username = :username
        """)
        db.execute(update_query, {"new_password": new_hashed_password, "username": user_info.username})
        db.commit()
        
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get('/available_analyses')
async def get_available_analyses() -> Dict:
    try:
        analyses = [
            {"name": "Daily Price Change", "endpoint": "/daily_price_change"},
            {"name": "Daily Price Range", "endpoint": "/daily_price_range"},
            {"name": "Moving Averages", "endpoint": "/moving_averages"},
            {"name": "Correlation Analysis", "endpoint": "/correlation_analysis"}
        ]
        return {"transaction_state": 200, "data": analyses}
    except Exception as e:
        return {"transaction_state": 500, "error": str(e)}

@app.get("/get_crypto_news")
def get_crypto_news():
    url = "https://crypto.news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    news_articles = []

    # Scraping the featured stories
    featured_stories = soup.find("div", class_="home-top-stories__featured")
    if featured_stories:
        articles = featured_stories.find_all("article", class_="post-top-story")
        for article in articles:
            title_tag = article.find("p", class_="post-top-story__title")
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            link_tag = title_tag.find("a") if title_tag else None
            link = link_tag["href"] if link_tag else "No Link"
            
            news_articles.append({
                "title": title,
                "link": link
            })

    # Scraping the list of additional top stories
    list_stories = soup.find("div", class_="home-top-stories__list")
    if list_stories:
        items = list_stories.find_all("div", class_="home-top-stories__item")
        for item in items:
            link_tag = item.find("a")
            title = link_tag.get_text(strip=True) if link_tag else "No Title"
            link = link_tag["href"] if link_tag else "No Link"
            news_articles.append({
                "title": title,
                "description": "No Description",
                "link": link
            })

    return news_articles

@app.post("/run_regression_model")
async def run_regression_model(
        start_date: Optional[str] = Body(None),
        end_date: Optional[str] = Body(None),
        coin_names: Optional[List[str]] = Body(None),
) -> Response:
    model_path = "./.models/ridge_model_test.pkl"
    query = "SELECT * FROM CoinsTable"
    df = run_query(query=query, connection=db_conn)
    fig = load_regression_model(file_path=model_path, df=df, coin_names=coin_names, start_date=start_date, end_date=end_date)

    return Response(content=json.dumps({"transaction":200, "data":{"graph": fig.to_json()}}), media_type="application/json")


    
@app.get("/get_top_5_crypto")
def get_top_5_crypto():
    # CoinGecko API URL for top coins
    url = "https://api.coingecko.com/api/v3/coins/markets"

    # Parameters for the API request
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1
    }

    # Making the API request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extracting relevant information
        top_5_crypto = []
        for coin in data:
            top_5_crypto.append({
                "name": coin["name"],
                "symbol": coin["symbol"],
                "price": coin["current_price"],
                "market_cap": coin["market_cap"],
                "volume": coin["total_volume"]
            })

        return top_5_crypto
    else:
        return {"error": "Unable to fetch data"}
    
@app.get('/volume_bar_graph')
async def volume_bar_graph(coin_names: List[str] = Query(...), start_date: str = Query(...), end_date: str = Query(...)) -> Response:
    try:
        # params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        # placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        # query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        df = run_updated_query(coin_names=coin_names, start_date=start_date, end_date=end_date, connection=db_conn)
        fig = plot_bar(df=df, x_column_name='Date', y_column_name='Volume')  # Updated line

        fig_json = fig.to_json()
        return Response(content=json.dumps({"transaction": 200, "data": {"graph": fig_json}}), media_type="application/json")
    except Exception as e:
        print(f"Error in /volume_bar_graph: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/candlestick_chart')
async def candlestick_chart(coin_names: List[str] = Query(...), start_date: str = Query(...), end_date: str = Query(...)) -> Response:
    try:
        # params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        # placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        # query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        # df = run_query(query=query, connection=db_conn, params=params)
        df = run_updated_query(coin_names=coin_names, start_date=start_date, end_date=end_date, connection=db_conn)
        fig = plot_candlestick(df=df)  # Updated line

        fig_json = fig.to_json()
        return Response(content=json.dumps({"transaction": 200, "data": {"graph": fig_json}}), media_type="application/json")
    except Exception as e:
        print(f"Error in /candlestick_chart: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/rsi_graph')
async def rsi_graph(coin_names: List[str] = Query(...), start_date: str = Query(...), end_date: str = Query(...)) -> Response:
    try:
        # params = {f"coin_{i}": coin_name for i, coin_name in enumerate(coin_names)}
        # placeholders = ', '.join([f':coin_{i}' for i in range(len(params))])
        # query = f"SELECT * FROM CoinsTable WHERE NAME IN ({placeholders})"
        # df = run_query(query=query, connection=db_conn, params=params)
        df = run_updated_query(coin_names=coin_names, start_date=start_date, end_date=end_date, connection=db_conn)
        #df['RSI'] = df.groupby('Name')[y_column_name].transform(lambda x: computeRSI(x, RSI_TIME_WINDOW))
        fig = plot_rsi(df=df, x_column_name='Date', y_column_name='RSI')  # Updated line

        fig_json = fig.to_json()
        return Response(content=json.dumps({"transaction": 200, "data": {"graph": fig_json}}), media_type="application/json")
    except Exception as e:
        print(f"Error in /rsi_graph: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Adjust api calls for dates 