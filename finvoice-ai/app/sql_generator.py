from langchain_community.llms import Ollama

llm = Ollama(model="qwen2.5:0.5b")

def generate_sql(intent_json):

    prompt = f"""
You are a PostgreSQL SQL generator.

STRICT RULES:
1. Return ONLY SQL query.
2. Do NOT explain anything.
3. Do NOT use markdown.
4. Do NOT use ```sql
5. Use ONLY PostgreSQL syntax.
6. Use ONLY these tables:

users(
    id,
    name,
    account_number,
    balance
)

transactions(
    id,
    sender,
    receiver,
    amount,
    transaction_type,
    transaction_date
)

EXAMPLES:

Intent:
{{"intent":"balance_check","name":"Saumya"}}

SQL:
SELECT balance FROM users
WHERE name='Saumya';

Intent:
{{"intent":"money_sent","receiver":"Rahul"}}

SQL:
SELECT * FROM transactions
WHERE sender='Saumya'
AND receiver='Rahul';

Intent:
{{"intent":"transaction_history","limit":5}}

SQL:
SELECT * FROM transactions
ORDER BY transaction_date DESC
LIMIT 5;

NOW GENERATE SQL ONLY.

Intent:
{intent_json}

SQL:
"""

    response = llm.invoke(prompt)

    return response.strip()