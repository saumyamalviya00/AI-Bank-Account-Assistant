from datetime import datetime, timedelta

from sqlalchemy import text

from app.database import engine


USERS = [
    ("Saumya", "ACC1001", 85000),
    ("Rahul", "ACC1002", 42000),
    ("Priya", "ACC1003", 92000),
    ("Aman", "ACC1004", 61000),
]


TRANSACTIONS = [
    ("Saumya", "Rahul", 5000, "sent", datetime.now() - timedelta(days=2)),
    ("Rahul", "Saumya", 2000, "received", datetime.now() - timedelta(days=1, hours=3)),
    ("Priya", "Saumya", 12000, "sent", datetime.now() - timedelta(days=4)),
    ("Saumya", "Aman", 3500, "sent", datetime.now() - timedelta(days=6)),
    ("Aman", "Priya", 8000, "sent", datetime.now() - timedelta(days=8)),
]


def seed_users(connection):
    existing = connection.execute(text("SELECT COUNT(*) FROM users")).scalar_one()
    if existing == 0:
        connection.execute(
            text(
                """
                INSERT INTO users (name, account_number, balance)
                VALUES (:name, :account_number, :balance)
                """
            ),
            [
                {"name": name, "account_number": account_number, "balance": balance}
                for name, account_number, balance in USERS
            ],
        )
        print(f"Inserted {len(USERS)} users")
    else:
        print(f"Skipped users; table already has {existing} row(s)")


def seed_transactions(connection):
    existing = connection.execute(text("SELECT COUNT(*) FROM transactions")).scalar_one()
    if existing == 0:
        connection.execute(
            text(
                """
                INSERT INTO transactions (
                    sender,
                    receiver,
                    amount,
                    transaction_type,
                    transaction_date
                )
                VALUES (
                    :sender,
                    :receiver,
                    :amount,
                    :transaction_type,
                    :transaction_date
                )
                """
            ),
            [
                {
                    "sender": sender,
                    "receiver": receiver,
                    "amount": amount,
                    "transaction_type": transaction_type,
                    "transaction_date": transaction_date,
                }
                for sender, receiver, amount, transaction_type, transaction_date in TRANSACTIONS
            ],
        )
        print(f"Inserted {len(TRANSACTIONS)} transactions")
    else:
        print(f"Skipped transactions; table already has {existing} row(s)")


def main():
    with engine.begin() as connection:
        seed_users(connection)
        seed_transactions(connection)


if __name__ == "__main__":
    main()