def format_response(intent_data, db_rows):
    """
    Format raw database rows into human-readable response.
    Handles empty results gracefully.
    """
    
    intent = intent_data.get("intent")
    target_name = intent_data.get("target_name")
    
    # Handle empty results
    if not db_rows:
        if intent == "show_balance":
            return "No balance information found."
        elif intent == "last_transactions":
            return "No transactions found."
        elif intent == "account_info":
            return "User account not found."
        elif intent == "money_sent":
            name_str = f" to {target_name}" if target_name else ""
            return f"No money sent{name_str} found."
        elif intent == "money_received":
            name_str = f" from {target_name}" if target_name else ""
            return f"No money received{name_str} found."
        elif intent == "monthly_spending":
            return "No spending data available for this period."
        else:
            return "No results found."
    
    # BALANCE - returns user record (id, name, account_number, balance)
    if intent == "show_balance":
        row = db_rows[0]
        balance = row[3] if len(row) > 3 else row[0]
        name = row[1] if len(row) > 1 else "your"
        
        if target_name:
            return f"{name}'s current account balance is ₹{balance}"
        else:
            return f"Your current account balance is ₹{balance}"
    
    # ACCOUNT INFO - returns user record (id, name, account_number, balance)
    elif intent == "account_info":
        row = db_rows[0]
        name = row[1]
        account = row[2]
        balance = row[3]
        
        return (
            f"{name}'s account number is {account} "
            f"with balance ₹{balance}."
        )
    
    # LAST TRANSACTIONS - returns transaction records (id, sender, receiver, amount, type, date)
    elif intent == "last_transactions":
        if len(db_rows) == 1:
            tx = db_rows[0]
            sender = tx[1]
            receiver = tx[2]
            amount = tx[3]
            tx_type = tx[4]
            tx_date = tx[5]
            
            return (
                f"Your latest transaction was ₹{amount} "
                f"{tx_type} from {sender} to {receiver} "
                f"on {tx_date.strftime('%d %B %Y') if hasattr(tx_date, 'strftime') else tx_date}."
            )
        else:
            # Multiple transactions
            response = f"Your last {len(db_rows)} transactions:\n"
            for i, tx in enumerate(db_rows, 1):
                sender = tx[1]
                receiver = tx[2]
                amount = tx[3]
                tx_type = tx[4]
                tx_date = tx[5]
                date_str = tx_date.strftime('%d %B %Y') if hasattr(tx_date, 'strftime') else tx_date
                response += f"{i}. ₹{amount} {tx_type} from {sender} to {receiver} on {date_str}\n"
            return response.strip()
    
    # MONEY SENT TO SOMEONE - returns transaction records
    elif intent == "money_sent":
        if len(db_rows) == 1:
            tx = db_rows[0]
            amount = tx[3]
            receiver = tx[2]
            tx_date = tx[5]
            date_str = tx_date.strftime('%d %B %Y') if hasattr(tx_date, 'strftime') else tx_date
            
            return f"You sent ₹{amount} to {receiver} on {date_str}."
        else:
            total = sum(tx[3] for tx in db_rows)
            receiver = db_rows[0][2]
            return (
                f"You sent a total of ₹{total} to {receiver} "
                f"across {len(db_rows)} transactions."
            )
    
    # MONEY RECEIVED FROM SOMEONE - returns transaction records
    elif intent == "money_received":
        if len(db_rows) == 1:
            tx = db_rows[0]
            amount = tx[3]
            sender = tx[1]
            tx_date = tx[5]
            date_str = tx_date.strftime('%d %B %Y') if hasattr(tx_date, 'strftime') else tx_date
            
            return f"You received ₹{amount} from {sender} on {date_str}."
        else:
            total = sum(tx[3] for tx in db_rows)
            sender = db_rows[0][1]
            return (
                f"You received a total of ₹{total} from {sender} "
                f"across {len(db_rows)} transactions."
            )
    
    # MONTHLY SPENDING - returns aggregated result (total_spent, transaction_count)
    elif intent == "monthly_spending":
        row = db_rows[0]
        total_spent = row[0] if len(row) > 0 else 0
        tx_count = row[1] if len(row) > 1 else 0
        
        if total_spent is None:
            return "No spending this period."
        
        time_range = intent_data.get("time_range", "this month")
        return (
            f"Your total spending {time_range} is ₹{total_spent} "
            f"across {tx_count} transactions."
        )
    
    # Fallback
    return f"Result: {str(db_rows)}"
