
def mock_llm_sql_generator(question):
    if "salary" in question:
        return "SELECT employee_name, employee_id FROM employees WHERE salary > 50000"
    return "SELECT * FROM employees"
