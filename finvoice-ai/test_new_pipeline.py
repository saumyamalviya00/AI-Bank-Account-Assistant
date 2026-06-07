"""
Test script for the improved SQL query generation pipeline.
Tests the new structured intent parsing and deterministic SQL generation.
"""

from app.intent_parser import parse_intent
from app.sql_generator import generate_sql
from app.response_formatter import format_response

def test_intent_parsing():
    """Test that intent parser extracts entities correctly."""
    print("\n" + "="*60)
    print("TEST: Intent Parsing with Entity Extraction")
    print("="*60)
    
    test_cases = [
        ("What is my balance?", {"intent": "show_balance"}),
        ("Show last 5 transactions", {"intent": "last_transactions", "limit": 5}),
        ("What's the balance for Rahul?", {"intent": "show_balance", "target_name": "Rahul"}),
        ("How much did I send to Rahul?", {"intent": "money_sent", "target_name": "Rahul"}),
    ]
    
    for query, expected_keys in test_cases:
        print(f"\nQuery: {query}")
        try:
            result = parse_intent(query)
            print(f"Result: {result}")
            # Check if all expected keys are present
            for key in expected_keys:
                if key in result:
                    print(f"  ✓ {key}: {result[key]}")
                else:
                    print(f"  ✗ Missing key: {key}")
        except Exception as e:
            print(f"  ERROR: {e}")

def test_sql_generation():
    """Test that SQL generator creates proper queries."""
    print("\n" + "="*60)
    print("TEST: SQL Generation (Deterministic)")
    print("="*60)
    
    test_cases = [
        {"intent": "show_balance"},
        {"intent": "show_balance", "target_name": "Rahul"},
        {"intent": "last_transactions", "limit": 5},
        {"intent": "money_sent", "target_name": "Rahul"},
        {"intent": "monthly_spending", "time_range": "this month"},
    ]
    
    for intent_data in test_cases:
        print(f"\nIntent: {intent_data}")
        sql = generate_sql(intent_data)
        print(f"SQL:\n{sql}")

def test_response_formatting():
    """Test that response formatter handles different data shapes."""
    print("\n" + "="*60)
    print("TEST: Response Formatting")
    print("="*60)
    
    # Test empty results
    print("\n[Empty Results]")
    test_cases = [
        ({"intent": "show_balance"}, []),
        ({"intent": "last_transactions"}, []),
        ({"intent": "money_sent", "target_name": "Rahul"}, []),
    ]
    
    for intent_data, rows in test_cases:
        print(f"\nIntent: {intent_data}")
        response = format_response(intent_data, rows)
        print(f"Response: {response}")
    
    # Test with mock data
    print("\n\n[With Mock Data]")
    
    # Balance query result: (id, name, account_number, balance)
    print("\nBalance Query:")
    intent = {"intent": "show_balance", "target_name": "Rahul"}
    rows = [(1, "Rahul", "ACC123456", 50000)]
    response = format_response(intent, rows)
    print(f"Response: {response}")
    
    # Transaction query result: (id, sender, receiver, amount, type, date)
    print("\nTransaction Query:")
    from datetime import datetime
    intent = {"intent": "last_transactions"}
    rows = [
        (1, "Rahul", "You", 5000, "received", datetime(2024, 1, 15)),
        (2, "You", "Saumya", 10000, "sent", datetime(2024, 1, 10)),
    ]
    response = format_response(intent, rows)
    print(f"Response:\n{response}")
    
    # Money sent query result
    print("\nMoney Sent Query (single):")
    intent = {"intent": "money_sent", "target_name": "Rahul"}
    rows = [(5, "You", "Rahul", 5000, "sent", datetime(2024, 1, 20))]
    response = format_response(intent, rows)
    print(f"Response: {response}")
    
    # Monthly spending query result: (total_spent, transaction_count)
    print("\nMonthly Spending Query:")
    intent = {"intent": "monthly_spending", "time_range": "this month"}
    rows = [(45000, 8)]  # aggregate result
    response = format_response(intent, rows)
    print(f"Response: {response}")

def test_pipeline_flow():
    """Test the complete pipeline flow with a sample query."""
    print("\n" + "="*60)
    print("TEST: Complete Pipeline Flow (Simulation)")
    print("="*60)
    
    user_queries = [
        "What's my balance?",
        "Show my last 5 transactions",
        "How much money did I send to Rahul?",
    ]
    
    for query in user_queries:
        print(f"\n{'='*40}")
        print(f"USER QUERY: {query}")
        print('='*40)
        
        try:
            # Step 1: Parse intent
            print("\n[STEP 1] Intent Parsing:")
            intent_data = parse_intent(query)
            print(f"Parsed Intent: {intent_data}")
            
            # Step 2: Generate SQL
            print("\n[STEP 2] SQL Generation:")
            sql = generate_sql(intent_data)
            print(f"Generated SQL:\n{sql}")
            
            # Step 3: Format response (with mock data)
            print("\n[STEP 3] Response Formatting (with empty mock result):")
            formatted = format_response(intent_data, [])
            print(f"Formatted Response: {formatted}")
            
        except Exception as e:
            print(f"ERROR in pipeline: {e}")

if __name__ == "__main__":
    print("\n" + "🧪 TESTING IMPROVED SQL QUERY GENERATION PIPELINE 🧪".center(60))
    
    try:
        test_intent_parsing()
    except Exception as e:
        print(f"\n⚠️  Intent parsing tests require LLM API: {e}")
    
    test_sql_generation()
    test_response_formatting()
    
    try:
        test_pipeline_flow()
    except Exception as e:
        print(f"\n⚠️  Pipeline flow tests require LLM API: {e}")
    
    print("\n" + "="*60)
    print("✅ Test suite completed!")
    print("="*60)
