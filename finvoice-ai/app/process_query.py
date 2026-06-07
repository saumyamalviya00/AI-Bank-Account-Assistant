from app.sql_generator import generate_sql
from app.query_engine import run_query

def clean_sql(sql):
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()
    return sql

def process_query(intent_data):
    """
    Process the query and return raw database rows.
    Returns a dict with rows and metadata for proper formatting.
    """
    
    sql = generate_sql(intent_data)
    sql = clean_sql(sql)
    
    print("\nGenerated SQL:")
    print(sql)
    
    rows = run_query(sql)
    
    print("\nRAW DATABASE RESULT:")
    print(rows)
    
    # Return raw rows - don't stringify!
    return rows
