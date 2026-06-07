#!/usr/bin/env python
"""Quick test of SQL generation and response formatting."""

from app.sql_generator import generate_sql
from app.response_formatter import format_response
from datetime import datetime

print("\n" + "="*60)
print("TEST: SQL Generation")
print("="*60)

test_cases = [
    {"intent": "show_balance"},
    {"intent": "show_balance", "target_name": "Rahul"},
    {"intent": "last_transactions", "limit": 5},
]

for intent_data in test_cases:
    sql = generate_sql(intent_data)
    print(f"\nIntent: {intent_data}")
    print(f"SQL: {sql[:100]}..." if len(sql) > 100 else f"SQL: {sql}")

print("\n" + "="*60)
print("TEST: Response Formatting")
print("="*60)

# Test empty results
print("\nEmpty Results:")
response = format_response({"intent": "show_balance"}, [])
print(f"  Balance (empty): {response}")
assert "not found" in response.lower()

# Test balance result
print("\nWith Data:")
rows = [(1, "Rahul", "ACC123456", 50000)]
response = format_response({"intent": "show_balance", "target_name": "Rahul"}, rows)
print(f"  Balance: {response}")
assert "₹50000" in response

print("\n✅ All tests passed!")
