from pydantic import BaseModel, EmailStr, Field


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_id: str
    username: str
    full_name: str | None = None


class AdminResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: str | None
    is_active: bool

    model_config = {"from_attributes": True}


class AdminCreate(BaseModel):
    """Schema dùng nội bộ / script để tạo admin mới."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str | None = None
    password: str = Field(..., min_length=8)
