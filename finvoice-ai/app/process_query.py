from app.sql_generator import generate_sql
from app.query_engine import run_query

def clean_sql(sql):

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql

def process_query(intent_data):

    sql = generate_sql(intent_data)

    sql = clean_sql(sql)

    print("\nGenerated SQL:")
    print(sql)

    result = run_query(sql)

    return str(result)

