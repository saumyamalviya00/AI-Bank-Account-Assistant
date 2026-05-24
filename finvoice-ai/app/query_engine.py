from sqlalchemy import text
from app.database import engine

def run_query(sql_query):

    with engine.connect() as conn:

        result = conn.execute(
            text(sql_query)
        )

        rows = result.fetchall()

        return rows