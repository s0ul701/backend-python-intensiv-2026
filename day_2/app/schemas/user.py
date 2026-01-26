from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """Схема для создания пользователя."""

    email: EmailStr = Field(
        description="Email адрес пользователя",
        examples=["user@example.com", "john.doe@company.org"],
    )
    name: str = Field(
        description="Полное имя пользователя",
        min_length=1,
        max_length=100,
        examples=["Иван Иванов", "John Doe"],
    )
    age: int = Field(
        description="Возраст пользователя (от 0 до 150)",
        ge=0,
        le=150,
        examples=[25, 30, 42],
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Имя не может быть пустым")
        return v.strip()


class UserResponse(BaseModel):
    """Схема ответа с данными пользователя."""

    id: int = Field(
        description="Уникальный идентификатор пользователя", examples=[1, 42, 100]
    )
    email: str = Field(
        description="Email адрес пользователя", examples=["user@example.com"]
    )
    name: str = Field(description="Полное имя пользователя", examples=["Иван Иванов"])
    age: int = Field(description="Возраст пользователя", examples=[25, 30])
    created_at: datetime = Field(
        description="Дата и время создания пользователя",
        examples=["2024-01-15T10:30:00"],
    )
    is_active: bool = Field(
        default=True,
        description="Активен ли аккаунт пользователя",
        examples=[True, False],
    )


class UserUpdate(BaseModel):
    """Схема для частичного обновления пользователя.

    Все поля опциональны — можно обновить только нужные.
    """

    email: Optional[EmailStr] = Field(
        default=None,
        description="Новый email адрес",
        examples=["new.email@example.com"],
    )
    name: Optional[str] = Field(
        default=None,
        description="Новое имя пользователя",
        min_length=1,
        max_length=100,
        examples=["Новое Имя"],
    )
    age: Optional[int] = Field(
        default=None,
        description="Новый возраст пользователя",
        ge=0,
        le=150,
        examples=[28],
    )
    is_active: Optional[bool] = Field(
        default=None,
        description="Новый статус активности аккаунта",
        examples=[True, False],
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Имя не может быть пустым")
        return v.strip() if v else None
