from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    is_active: bool | None = None

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> "UserUpdate":
        if self.name is None and self.email is None and self.is_active is None:
            raise ValueError("At least one field must be provided.")
        return self


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
