from pydantic import BaseModel

class LoginRequest(BaseModel):
    tenant_id: str
    user_id: str
    password: str

class LoginResponse(BaseModel):
    token: str