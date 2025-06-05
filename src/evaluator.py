
import sqlite3
import pandas as pd
import json

DB_PATH = 'data/db.sqlite'
GOLDEN_QUERY_PATH = 'golden_queries/benchmark.json'

def load_golden_query(question_id):
    with open(GOLDEN_QUERY_PATH) as f:
        data = json.load(f)
    return data[question_id]["sql"]

def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    return pd.read_sql_query(query, conn)

def row_match_score(df1, df2):
    df1_set = set(df1.apply(tuple, axis=1))
    df2_set = set(df2.apply(tuple, axis=1))
    match_count = len(df1_set.intersection(df2_set))
    total_count = len(df1_set.union(df2_set))
    return (match_count / total_count) * 100 if total_count > 0 else 0

def column_match_score(df1, df2):
    common_cols = set(df1.columns).intersection(set(df2.columns))
    total_cols = set(df1.columns).union(set(df2.columns))
    return (len(common_cols) / len(total_cols)) * 100 if total_cols else 0

def evaluate_query_accuracy(question_id, generated_query):
    golden_query = load_golden_query(question_id)
    try:
        df_golden = run_query(golden_query)
        df_generated = run_query(generated_query)
    except Exception as e:
        return 0.0

    row_score = row_match_score(df_golden, df_generated)
    column_score = column_match_score(df_golden, df_generated)
    return round((row_score + column_score) / 2, 2)
