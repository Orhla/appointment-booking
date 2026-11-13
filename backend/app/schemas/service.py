from pydantic import BaseModel, Field
from decimal import Decimal

class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=1000)
    duration_min: int = Field(..., gt=0)
    price: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    
class ServiceRead(BaseModel):
    id: int
    name: str
    duration_min: int
    price: Decimal
    
    model_config = {"from_attributes": True}