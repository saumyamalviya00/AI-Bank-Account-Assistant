from langchain_community.llms import Ollama

llm = Ollama(model="qwen2.5:0.5b")

def parse_intent(user_query):

    prompt = f"""
    Extract banking intent from this query.

    Return ONLY valid JSON.

    Query:
    {user_query}

    Examples:

    Query: What is my balance?
    {{
      "intent":"balance_check"
    }}

    Query: Show my last 5 transactions
    {{
      "intent":"transaction_history",
      "limit":5
    }}

    Query: How much money did I send Rahul?
    {{
      "intent":"money_sent",
      "receiver":"Rahul"
    }}
    """

    response = llm.invoke(prompt)

    return response

