import os
import getpass

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Allow overriding the DB URL via environment for local/CI differences.
# Default to the current macOS user so a fresh local Postgres install works
# even when DATABASE_URL is not exported in the shell running uvicorn.
current_user = getpass.getuser()
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{current_user}@localhost/bank_ai",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
