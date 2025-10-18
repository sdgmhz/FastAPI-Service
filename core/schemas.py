from pydantic import BaseModel, Field, field_serializer, EmailStr, field_validator
from decimal import Decimal


class CostBaseSchema(BaseModel):
    description: str = Field(
        ...,
        max_length=50,
        min_length=5,
        pattern=r"^[^\d].*",
        example="enter the description",
    )
    amount: Decimal = Field(..., gt=0, decimal_places=2, max_digits=10)
    email: EmailStr

    @field_serializer("description")
    def serialize_description(value):
        return value.capitalize()

    @field_validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return value


class CostResponseSchema(CostBaseSchema):
    id: int = Field(..., gt=0)


class CostCreateSchema(CostBaseSchema):
    pass


class CostUpdateSchema(CostBaseSchema):
    pass
