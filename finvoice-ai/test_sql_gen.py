#!/usr/bin/env python
"""Validate SQL generation."""

from app.sql_generator import generate_sql

print("\nTesting SQL Generation:\n")

# Test show_balance
sql = generate_sql({"intent": "show_balance"})
assert "balance" in sql.lower() and "users" in sql.lower()
print("OK show_balance")

# Test with target name
sql = generate_sql({"intent": "show_balance", "target_name": "Rahul"})
assert "Rahul" in sql and "balance" in sql.lower()
print("OK show_balance (Rahul)")

# Test transactions
sql = generate_sql({"intent": "last_transactions", "limit": 5})
assert "LIMIT 5" in sql and "transactions" in sql.lower()
print("OK last_transactions")

# Test money_sent
sql = generate_sql({"intent": "money_sent", "target_name": "Rahul"})
assert "Rahul" in sql and "sent" in sql.lower()
print("OK money_sent")

# Test account_info
sql = generate_sql({"intent": "account_info"})
assert "users" in sql.lower() and "balance" in sql.lower()
print("OK account_info")

# Test monthly_spending
sql = generate_sql({"intent": "monthly_spending"})
assert "transactions" in sql.lower()
print("OK monthly_spending")

print("\nAll SQL generation tests passed!")
