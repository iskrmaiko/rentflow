from enum import Enum
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


class EquipmentCategory(str, Enum):
    POWER_TOOLS    = "POWER_TOOLS"
    HAND_TOOLS     = "HAND_TOOLS"
    CONSTRUCTION   = "CONSTRUCTION"
    LANDSCAPING    = "LANDSCAPING"
    LIGHTING       = "LIGHTING"
    AUDIO_VISUAL   = "AUDIO_VISUAL"
    CLEANING       = "CLEANING"
    SAFETY         = "SAFETY"
    TRANSPORTATION = "TRANSPORTATION"
    OTHER          = "OTHER"


class EquipmentStatus(str, Enum):
    ACTIVE   = "ACTIVE"
    INACTIVE = "INACTIVE"


@dataclass
class Equipment:
    id:                 UUID
    name:               str
    description:        str
    category:           EquipmentCategory
    daily_rental_price: Decimal
    status:             EquipmentStatus

    def toggle_status(self) -> None:
        """Pure domain behaviour — flip ACTIVE ↔ INACTIVE."""
        if self.status == EquipmentStatus.ACTIVE:
            self.status = EquipmentStatus.INACTIVE
        else:
            self.status = EquipmentStatus.ACTIVE
