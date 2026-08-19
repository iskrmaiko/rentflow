import uuid
from decimal import Decimal
from uuid import UUID

from ...domain.equipment.entities import Equipment, EquipmentCategory, EquipmentStatus
from ...domain.equipment.exceptions import EquipmentNotFoundError
from ...domain.equipment.repositories import EquipmentRepository


class ListEquipmentUseCase:
    def __init__(self, repository: EquipmentRepository):
        self._repo = repository

    def execute(self) -> list[Equipment]:
        return self._repo.list_all()


class GetEquipmentByIdUseCase:
    def __init__(self, repository: EquipmentRepository):
        self._repo = repository

    def execute(self, equipment_id: UUID) -> Equipment:
        entity = self._repo.get_by_id(equipment_id)
        if entity is None:
            raise EquipmentNotFoundError(equipment_id)
        return entity


class CreateEquipmentUseCase:
    def __init__(self, repository: EquipmentRepository):
        self._repo = repository

    def execute(
        self,
        name: str,
        description: str,
        category: EquipmentCategory,
        daily_rental_price: Decimal,
    ) -> Equipment:
        entity = Equipment(
            id=uuid.uuid4(),
            name=name,
            description=description,
            category=category,
            daily_rental_price=daily_rental_price,
            status=EquipmentStatus.ACTIVE,
        )
        return self._repo.save(entity)


class UpdateEquipmentUseCase:
    def __init__(self, repository: EquipmentRepository):
        self._repo = repository

    def execute(
        self,
        equipment_id: UUID,
        name: str,
        description: str,
        category: EquipmentCategory,
        daily_rental_price: Decimal,
    ) -> Equipment:
        entity = self._repo.get_by_id(equipment_id)
        if entity is None:
            raise EquipmentNotFoundError(equipment_id)
        entity.name = name
        entity.description = description
        entity.category = category
        entity.daily_rental_price = daily_rental_price
        return self._repo.update(entity)


class ToggleEquipmentStatusUseCase:
    def __init__(self, repository: EquipmentRepository):
        self._repo = repository

    def execute(self, equipment_id: UUID) -> Equipment:
        entity = self._repo.get_by_id(equipment_id)
        if entity is None:
            raise EquipmentNotFoundError(equipment_id)
        entity.toggle_status()
        return self._repo.update(entity)


class DeleteEquipmentUseCase:
    def __init__(self, repository: EquipmentRepository):
        self._repo = repository

    def execute(self, equipment_id: UUID) -> None:
        entity = self._repo.get_by_id(equipment_id)
        if entity is None:
            raise EquipmentNotFoundError(equipment_id)
        self._repo.delete(equipment_id)
