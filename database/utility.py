import pandas as pd
from sqlalchemy import text
from .sql_connection_test import SQLiteConnection
from .exceptions import DataBaseQueryException
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional

def run_query(query: str, connection: SQLiteConnection, params: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Executes the given SQL query on the provided database connection
    and returns the result as a Pandas DataFrame.
    
    Args:
        query (str): The SQL query to execute.
        connection (sqlalchemy.engine.Connection): The database connection.
        params (dict, optional): Parameters to bind to the SQL query (e.g., for parameterized queries).
    
    Returns:
        pd.DataFrame: The result of the query as a DataFrame.
    """
    try:
        # Execute the query with optional parameters
        # with connection.connect() as conn:
        #     pass
        result = connection.connect().execute(text(query), params)
        
        # Convert the result to a Pandas DataFrame
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        # Close the result proxy
        result.close()
        
        return df
    except SQLAlchemyError as e:
        raise DataBaseQueryException(f"Error running database query: {e}")
    except Exception as e:
        raise DataBaseQueryException(f"Logic error: {e}")

def run_updated_query(coin_names: List[str], start_date: str, end_date: str, connection: SQLiteConnection) -> pd.DataFrame:
    """
    Retrieves data from the database for the specified coins within the given date range.

    Args:
        coin_names (List[str]): A list of coin names to retrieve data for.
        start_date (str): The start date of the date range (inclusive).
        end_date (str): The end date of the date range (inclusive).
        connection (sqlalchemy.engine.Connection): The database connection to use.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the retrieved data.
    """
    df = pd.DataFrame()
    for coin in coin_names:
        # Create the params dictionary for the current coin
        params = {"coin_name": coin, "start_date": start_date, "end_date": end_date}

        # Query with date filtering
        query = """
        SELECT * FROM CoinsTable 
        WHERE Name = :coin_name 
        AND strftime('%Y-%m-%d', Date) BETWEEN :start_date AND :end_date
        """
        df_temp = run_query(query=query, connection=connection, params=params)

        if df_temp.empty:
            # If no data is found within the date range, fetch all data for that coin
            query = "SELECT * FROM CoinsTable WHERE Name = :coin_name"
            df_temp = run_query(query=query, connection=connection, params={"coin_name": coin})

        # Concatenate the results
        df = pd.concat([df, df_temp], ignore_index=True)

    return df