from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def parse_intent(user_query):
    """
    Enhanced intent parser that extracts both intent and relevant entities.
    Returns structured JSON with intent, target_name, time_range, limit, etc.
    """

    prompt = f"""
You are a banking intent classifier and entity extractor.

Return ONLY valid JSON with intent and extracted entities.

Do NOT explain.
Do NOT add markdown.
Do NOT add extra text.

Supported intents: show_balance, last_transactions, account_info, money_sent, money_received, monthly_spending

Entity fields (include only if present):
- target_name: name of the person mentioned (e.g., "Rahul", "Saumya")
- time_range: period mentioned (e.g., "this month", "last week", "today")
- limit: number of records to fetch (default 5 for transactions)

Examples:

Query: What is my balance?
Response:
{{"intent":"show_balance"}}

Query: Show last 5 transactions
Response:
{{"intent":"last_transactions","limit":5}}

Query: What's the balance for Rahul?
Response:
{{"intent":"show_balance","target_name":"Rahul"}}

Query: How much money did I send to Rahul?
Response:
{{"intent":"money_sent","target_name":"Rahul"}}

Query: How much did I spend this month?
Response:
{{"intent":"monthly_spending","time_range":"this month"}}

Now classify and extract entities from this query:

Query:
{user_query}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    result = json.loads(content)
    
    # Normalize extracted names - extract capitalized words
    if 'target_name' not in result and result.get('intent') in ['money_sent', 'money_received', 'show_balance']:
        names = re.findall(r'\b[A-Z][a-z]+\b', user_query)
        if names:
            result['target_name'] = names[0]
    
    # Extract limit if not explicitly set
    if 'limit' not in result and 'transaction' in result.get('intent', ''):
        limit_match = re.search(r'\b(\d+)\s+(?:transaction|record)', user_query)
        if limit_match:
            result['limit'] = int(limit_match.group(1))
        else:
            result['limit'] = 5
    
    return result