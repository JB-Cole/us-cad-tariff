# db_utils.py
import pandas as pd
from sqlalchemy import create_engine

def create_db_engine(user, password, host, database, port=5432):
    conn_string = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
    return create_engine(conn_string)

def save_table(df, table_name, engine, mode='replace'):
    df.to_sql(table_name, engine, if_exists=mode, index=False)

def query_table(engine, sql_query):
    return pd.read_sql(sql_query, engine)
