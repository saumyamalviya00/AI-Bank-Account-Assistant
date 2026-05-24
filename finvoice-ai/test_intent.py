from app.intent_parser import parse_intent

query = "How much money did I send Rahul?"

result = parse_intent(query)

print(result)