import os
from dotenv import load_dotenv
load_dotenv(override=True)

class DatabaseConfig:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables or .env file!")

# Singleton instance of Config
DATABASE = DatabaseConfig()

class AuthConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in environment variables or .env file!")
    if not HASH_ALGORITHM:
        raise ValueError("HASH_ALGORITHM is not set in environment variables or .env file!")
    if not ACCESS_TOKEN_EXPIRE_MINUTES:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES is not set in environment variables or .env file!")
    
# Tracking model configuration
class TrackingConfig:
    TRACKING_MODEL_PATH: str = os.getenv("TRACKING_MODEL_PATH", "")
    if not TRACKING_MODEL_PATH:
        raise ValueError("TRACKING_MODEL_PATH is not set in environment variables or .env file!")

TRACKING = TrackingConfig()

# Redis configuration
class RedisConfig:
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

REDIS = RedisConfig()