from pydantic import BaseModel
class MessageResponse(BaseModel):  # Used for creating users
    message: str