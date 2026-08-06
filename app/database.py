import sqlite3
import pandas as pd


DB_PATH = "database/northwind2000.sqlite"


def execute_query(sql_query):
    try:
        conn = sqlite3.connect(DB_PATH)

        df = pd.read_sql_query(sql_query, conn)

        conn.close()

        return df, None

    except Exception as e:
        return None, str(e)