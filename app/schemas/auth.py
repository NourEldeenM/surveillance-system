from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str # plain
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
