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
