from app.sql_generator import generate_sql

intent = {
    "intent":"money_sent",
    "receiver":"Rahul"
}

result = generate_sql(intent)

print(result)