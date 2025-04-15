from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import AuthConfig
import jwt
from jwt.exceptions import InvalidTokenError
from app.utils.exceptions import UnauthorizedError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes plain text password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifies a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        """Generates a JWT access token."""
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=float(AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthConfig.SECRET_KEY, algorithm=AuthConfig.HASH_ALGORITHM)
    
    @staticmethod
    def decode_access_token(token: str):
        try:
            return jwt.decode(token, AuthConfig.SECRET_KEY, algorithms=[AuthConfig.HASH_ALGORITHM])
        except InvalidTokenError:
            raise UnauthorizedError("JWT Error, token invalid.")