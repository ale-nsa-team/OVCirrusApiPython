from pydantic import BaseModel
from typing import Generic, TypeVar

class AuthRequest(BaseModel):
    email: str
    password: str
    app_id: str
    app_secret: str

class AuthResponse(BaseModel):
    token_type: str
    expires_in: int  # seconds
    access_token: str


