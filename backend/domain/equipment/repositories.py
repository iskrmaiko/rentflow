from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Equipment


class EquipmentRepository(ABC):
    @abstractmethod
    def list_all(self) -> list[Equipment]: ...

    @abstractmethod
    def get_by_id(self, equipment_id: UUID) -> Equipment | None: ...

    @abstractmethod
    def save(self, equipment: Equipment) -> Equipment: ...

    @abstractmethod
    def update(self, equipment: Equipment) -> Equipment: ...

    @abstractmethod
    def delete(self, equipment_id: UUID) -> None: ...
