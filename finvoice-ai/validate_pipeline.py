#!/usr/bin/env python
"""Comprehensive tests for the improved pipeline."""

from app.sql_generator import generate_sql
from app.response_formatter import format_response
from datetime import datetime

print("\n" + "="*60)
print("TEST: Response Formatter")
print("="*60)

# Empty result
result = format_response({"intent": "show_balance"}, [])
assert "found" in result.lower() and "information" in result.lower()
print(f"✓ Empty result: {result}")

# Balance result
rows = [(1, "Rahul", "ACC123456", 50000)]
result = format_response({"intent": "show_balance", "target_name": "Rahul"}, rows)
assert "50000" in result and "Rahul" in result
print(f"✓ Balance result: {result}")

# Own balance
rows = [(1, "You", "ACC123456", 75000)]
result = format_response({"intent": "show_balance"}, rows)
assert "75000" in result and "Your" in result
print(f"✓ Own balance: {result}")

# Single transaction
rows = [(1, "Rahul", "You", 5000, "received", datetime(2024, 1, 15))]
result = format_response({"intent": "last_transactions"}, rows)
assert "5000" in result and "received" in result
print(f"✓ Single transaction: {result}")

# Multiple transactions  
rows = [
    (1, "Rahul", "You", 5000, "received", datetime(2024, 1, 15)),
    (2, "You", "Saumya", 10000, "sent", datetime(2024, 1, 10)),
]
result = format_response({"intent": "last_transactions"}, rows)
assert "2 transactions" in result
print(f"✓ Multiple transactions formatted")

# Money sent
rows = [(5, "You", "Rahul", 5000, "sent", datetime(2024, 1, 20))]
result = format_response({"intent": "money_sent", "target_name": "Rahul"}, rows)
assert "5000" in result and "Rahul" in result
print(f"✓ Money sent: {result}")

# Monthly spending
rows = [(45000, 8)]
result = format_response({"intent": "monthly_spending", "time_range": "this month"}, rows)
assert "45000" in result and "8 transactions" in result
print(f"✓ Monthly spending: {result}")

print("\n" + "="*60)
print("TEST: SQL Generation")
print("="*60)

# Test various intent types
tests = [
    ({"intent": "show_balance"}, "show_balance"),
    ({"intent": "show_balance", "target_name": "Rahul"}, "target_name"),
    ({"intent": "last_transactions", "limit": 5}, "LIMIT 5"),
    ({"intent": "money_sent", "target_name": "Rahul"}, "Rahul"),
    ({"intent": "account_info"}, "users"),
]

for intent, expected in tests:
    sql = generate_sql(intent)
    assert expected in sql, f"Expected '{expected}' in SQL: {sql}"
    print(f"✓ {intent['intent']}: SQL generated correctly")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
