def format_response(intent_data, db_result):

    intent = intent_data.get("intent")

    # BALANCE
    if intent == "show_balance":

        if not db_result:

            return "No balance information found."

        balance = db_result[0][0]

        return f"Your current account balance is ₹{balance}"


    # LAST TRANSACTION
    elif intent == "last_transactions":

        if not db_result:

            return "No transactions found."

        tx = db_result[0]

        sender = tx[1]
        receiver = tx[2]
        amount = tx[3]
        tx_type = tx[4]
        tx_date = tx[5]

        return (
            f"Your latest transaction was ₹{amount} "
            f"{tx_type} from {sender} to {receiver} "
            f"on {tx_date.strftime('%d %B %Y')}."
        )


    # ACCOUNT INFO
    elif intent == "account_info":

        if not db_result:

            return "User account not found."

        user = db_result[0]

        name = user[1]
        account = user[2]
        balance = user[3]

        return (
            f"{name}'s account number is {account} "
            f"with balance ₹{balance}."
        )


    return str(db_result)