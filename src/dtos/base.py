from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # Для работы с SQLAlchemy моделями
        validate_assignment=True,  # Валидация при присваивании
        str_strip_whitespace=True,  # Удаление пробелов
        use_enum_values=True,  # Использование значений enum
        populate_by_name=True,  # Поддержка алиасов полей
        arbitrary_types_allowed=False,  # Запрещаем произвольные типы
        extra='forbid'  # Запрещаем лишние поля
    )


class TimestampMixin(BaseModel):
    created_at: datetime = Field(
        description="Дата и время создания",
        examples=["2025-06-24T10:30:00Z"]
    )
    updated_at: datetime = Field(
        description="Дата и время последнего обновления",
        examples=["2025-06-24T12:45:00Z"]
    )


class IDMixin(BaseModel):
    id: int = Field(
        gt=0,
        description="Уникальный идентификатор",
        examples=[1, 42, 123]
    )
