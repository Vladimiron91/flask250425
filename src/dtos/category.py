from pydantic import Field

from src.dtos.base import BaseDTO, IDMixin


class CategoryCreateUpdateDTO(BaseDTO):
    name: str = Field(max_length=25)


class CategoryResponseDTO(BaseDTO, IDMixin):
    name: str
