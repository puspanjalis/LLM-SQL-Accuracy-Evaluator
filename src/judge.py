
import openai

def llm_judge_score(question, generated_query, golden_query, mode="simple"):
    prompt = f"""
You are an expert SQL reviewer. A user asked: "{question}"
Here is the correct SQL: {golden_query}
Here is the generated SQL: {generated_query}
Rate the generated SQL on a scale of 0 to 100 based on how close it is to the correct SQL.
{ "Also explain your reasoning." if mode == "explainable" else "" }
Only return the number and explanation if applicable.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content'].strip()
