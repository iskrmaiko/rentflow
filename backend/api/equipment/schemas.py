from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
from ...domain.equipment.entities import EquipmentCategory, EquipmentStatus


class EquipmentResponse(BaseModel):
    id: UUID
    name: str
    description: str
    category: EquipmentCategory
    daily_rental_price: Decimal
    status: EquipmentStatus

    model_config = {"from_attributes": True}


class CreateEquipmentRequest(BaseModel):
    name: str = Field(..., min_length=1, strip_whitespace=True)
    description: str = Field(default="")
    category: EquipmentCategory
    daily_rental_price: Decimal = Field(..., ge=0)


class UpdateEquipmentRequest(BaseModel):
    name: str = Field(..., min_length=1, strip_whitespace=True)
    description: str = Field(default="")
    category: EquipmentCategory
    daily_rental_price: Decimal = Field(..., ge=0)
