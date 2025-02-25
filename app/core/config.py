import os
from dotenv import load_dotenv
load_dotenv()
class DatabaseConfig:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables or .env file!")

# Singleton instance of Config
DATABASE = DatabaseConfig()
