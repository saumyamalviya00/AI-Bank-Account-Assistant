from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def parse_intent(user_query):

    prompt = f"""
You are a banking intent classifier.

Return ONLY valid JSON.

Do NOT explain.
Do NOT add markdown.
Do NOT add extra text.

Examples:

Query: What is my balance?
Response:
{{"intent":"show_balance"}}

Query: Show last 5 transactions
Response:
{{"intent":"last_transactions"}}

Query: How much did I spend this month?
Response:
{{"intent":"monthly_spending"}}

Now classify this query:

Query:
{user_query}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)