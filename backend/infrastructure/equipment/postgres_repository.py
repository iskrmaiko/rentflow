from uuid import UUID
from decimal import Decimal
from psycopg2.extras import RealDictCursor
from ...domain.equipment.entities import Equipment, EquipmentCategory, EquipmentStatus
from ...domain.equipment.repositories import EquipmentRepository


def _row_to_entity(row) -> Equipment:
    return Equipment(
        id=UUID(str(row["id"])),
        name=row["name"],
        description=row["description"],
        category=EquipmentCategory(row["category"]),
        daily_rental_price=Decimal(str(row["daily_rental_price"])),
        status=EquipmentStatus(row["status"]),
    )


class PostgresEquipmentRepository(EquipmentRepository):
    def __init__(self, connection):
        self._connection = connection

    def list_all(self) -> list[Equipment]:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, name, description, category, daily_rental_price, status FROM equipment")
            rows = cur.fetchall()
        return [_row_to_entity(row) for row in rows]

    def get_by_id(self, equipment_id: UUID) -> Equipment | None:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, name, description, category, daily_rental_price, status FROM equipment WHERE id = %s",
                (str(equipment_id),),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return _row_to_entity(row)

    def save(self, equipment: Equipment) -> Equipment:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO equipment (id, name, description, category, daily_rental_price, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, name, description, category, daily_rental_price, status
                """,
                (
                    str(equipment.id),
                    equipment.name,
                    equipment.description,
                    equipment.category.value,
                    str(equipment.daily_rental_price),
                    equipment.status.value,
                ),
            )
            row = cur.fetchone()
            self._connection.commit()
        return _row_to_entity(row)

    def update(self, equipment: Equipment) -> Equipment:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE equipment
                SET name = %s, description = %s, category = %s,
                    daily_rental_price = %s, status = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING id, name, description, category, daily_rental_price, status
                """,
                (
                    equipment.name,
                    equipment.description,
                    equipment.category.value,
                    str(equipment.daily_rental_price),
                    equipment.status.value,
                    str(equipment.id),
                ),
            )
            row = cur.fetchone()
            self._connection.commit()
        return _row_to_entity(row)

    def delete(self, equipment_id: UUID) -> None:
        with self._connection.cursor() as cur:
            cur.execute(
                "DELETE FROM equipment WHERE id = %s",
                (str(equipment_id),),
            )
            self._connection.commit()
