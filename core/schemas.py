from pydantic import BaseModel, Field, field_serializer
from decimal import Decimal



class CostBaseSchema(BaseModel):
    description: str = Field(..., max_length=50, min_length=5, regex= r'^[^\d].*')
    amount: Decimal = Field(..., ge=0, decimal_places=2, max_digits=10)

    @field_serializer("description")
    def serialize_description(value):
        return value.title()



class CostResponseSchema(CostBaseSchema):
    id : int



class CostCreateSchema(CostBaseSchema):
    pass

class CostUpdateSchema(CostBaseSchema):
    pass





