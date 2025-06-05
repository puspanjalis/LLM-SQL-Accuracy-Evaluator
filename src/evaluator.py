
import json
from src.db_connector import run_query
import pandas as pd

GOLDEN_QUERY_PATH = 'golden_queries/benchmark.json'

def load_golden_query(question_id):
    with open(GOLDEN_QUERY_PATH) as f:
        data = json.load(f)
    for entry in data:
        if entry["question_id"] == question_id:
            return entry["sql"]
    return None

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

def evaluate_query_accuracy(question_id, generated_query, engine='sqlite', conn_params=None):
    golden_query = load_golden_query(question_id)
    try:
        df_golden = run_query(golden_query, engine, conn_params)
        df_generated = run_query(generated_query, engine, conn_params)
    except Exception as e:
        return {"accuracy": 0.0, "error": str(e), "success": False}

    row_score = row_match_score(df_golden, df_generated)
    column_score = column_match_score(df_golden, df_generated)
    accuracy = round((row_score + column_score) / 2, 2)
    return {
        "accuracy": accuracy,
        "row_score": round(row_score, 2),
        "column_score": round(column_score, 2),
        "success": True
    }

def evaluate_batch(test_cases_path, engine='sqlite', conn_params=None):
    with open(test_cases_path) as f:
        test_cases = json.load(f)

    results = []
    for case in test_cases:
        result = evaluate_query_accuracy(case["question_id"], case["generated_sql"], engine, conn_params)
        result.update(case)
        results.append(result)

    return pd.DataFrame(results)
