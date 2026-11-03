from pydantic import BaseModel, field_serializer  
from decimal import Decimal

class ServiceCreate(BaseModel):
    name: str
    duration_min: int
    price: Decimal
    
class ServiceRead(BaseModel):
    id: int
    name: str
    duration_min: int
    price: Decimal
    
    model_config = {"from_attributes": True}

    @field_serializer("price")
    def serialize_price(self, price: Decimal) -> float:
        return float(price)