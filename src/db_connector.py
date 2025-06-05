
import pandas as pd
import sqlite3

def run_query(query, engine='sqlite', conn_params=None):
    conn_params = conn_params or {}
    if engine == 'sqlite':
        conn = sqlite3.connect(conn_params.get("path", "data/db.sqlite"))
    elif engine == 'snowflake':
        import snowflake.connector
        conn = snowflake.connector.connect(**conn_params)
    else:
        raise ValueError("Unsupported engine type")

    return pd.read_sql(query, conn)
