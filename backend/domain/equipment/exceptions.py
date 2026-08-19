from uuid import UUID


class EquipmentNotFoundError(Exception):
    def __init__(self, equipment_id: UUID):
        self.equipment_id = equipment_id
        super().__init__(f"Equipment with id {equipment_id} not found.")
