from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    tenant_name: str
    user_id: str
    password: str
