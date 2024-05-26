import pandas as pd
import sqlite3

def push_to_sqlite(df: pd.DataFrame, table_name: str, db_name: str = "./test_db.db") -> None:
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"DataFrame successfully pushed to table '{table_name}' in database '{db_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def push_to_azure(df: pd.DataFrame) -> None:
    pass

def write_to_csv(df: pd.DataFrame, file_name: str = ".data/coins.csv") -> None:
    df.to_csv(file_name, index=False)
