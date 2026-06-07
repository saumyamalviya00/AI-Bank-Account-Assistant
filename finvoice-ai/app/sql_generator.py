from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def generate_sql(intent_data):
    """
    Deterministic SQL generator based on structured intent and entities.
    No LLM calls - pure Python SQL building.
    """
    
    intent = intent_data.get("intent")
    target_name = intent_data.get("target_name")
    time_range = intent_data.get("time_range", "").lower()
    limit = intent_data.get("limit", 5)
    
    # BALANCE QUERIES
    if intent == "show_balance":
        if target_name:
            return f"SELECT id, name, account_number, balance FROM users WHERE name = '{target_name}';"
        else:
            # Assuming "current user" is the authenticated user (in production, get from context)
            # For now, query for a default user or return generic query
            return "SELECT id, name, account_number, balance FROM users LIMIT 1;"
    
    # ACCOUNT INFO
    elif intent == "account_info":
        if target_name:
            return f"SELECT id, name, account_number, balance FROM users WHERE name = '{target_name}';"
        else:
            return "SELECT id, name, account_number, balance FROM users LIMIT 1;"
    
    # LAST TRANSACTIONS - sorted by date descending
    elif intent == "last_transactions":
        return f"SELECT id, sender, receiver, amount, transaction_type, transaction_date FROM transactions ORDER BY transaction_date DESC LIMIT {limit};"
    
    # MONEY SENT TO SOMEONE
    elif intent == "money_sent":
        if target_name:
            return f"SELECT id, sender, receiver, amount, transaction_type, transaction_date FROM transactions WHERE receiver = '{target_name}' AND transaction_type = 'sent' ORDER BY transaction_date DESC LIMIT {limit};"
        else:
            return "SELECT id, sender, receiver, amount, transaction_type, transaction_date FROM transactions WHERE transaction_type = 'sent' ORDER BY transaction_date DESC LIMIT 5;"
    
    # MONEY RECEIVED FROM SOMEONE
    elif intent == "money_received":
        if target_name:
            return f"SELECT id, sender, receiver, amount, transaction_type, transaction_date FROM transactions WHERE sender = '{target_name}' AND transaction_type = 'received' ORDER BY transaction_date DESC LIMIT {limit};"
        else:
            return "SELECT id, sender, receiver, amount, transaction_type, transaction_date FROM transactions WHERE transaction_type = 'received' ORDER BY transaction_date DESC LIMIT 5;"
    
    # MONTHLY SPENDING
    elif intent == "monthly_spending":
        # Calculate date range for "this month"
        now = datetime.now()
        month_start = now.replace(day=1)
        
        if "last month" in time_range:
            month_start = now.replace(day=1) - relativedelta(months=1)
        
        month_end = month_start + relativedelta(months=1) - timedelta(days=1)
        
        return f"""
SELECT 
    SUM(amount) as total_spent,
    COUNT(*) as transaction_count
FROM transactions
WHERE transaction_type = 'sent'
AND transaction_date >= '{month_start.strftime('%Y-%m-%d')}'
AND transaction_date <= '{month_end.strftime('%Y-%m-%d')}';
"""
    
    # Fallback
    return "SELECT * FROM transactions LIMIT 5;"
