import os
from uuid import UUID

import psycopg2
from fastapi import APIRouter, Depends, HTTPException

from ...domain.equipment.exceptions import EquipmentNotFoundError
from ...application.equipment.use_cases import (
    ListEquipmentUseCase,
    GetEquipmentByIdUseCase,
    CreateEquipmentUseCase,
    UpdateEquipmentUseCase,
    ToggleEquipmentStatusUseCase,
    DeleteEquipmentUseCase,
)
from ...infrastructure.equipment.postgres_repository import PostgresEquipmentRepository
from .schemas import EquipmentResponse, CreateEquipmentRequest, UpdateEquipmentRequest


router = APIRouter()


def get_db_connection():
    database_url = os.environ.get(
        "DATABASE_URL", "postgresql://rentflow:rentflow@db:5432/rentflow"
    )
    conn = psycopg2.connect(database_url)
    try:
        yield conn
    finally:
        conn.close()


def get_repository(conn=Depends(get_db_connection)):
    return PostgresEquipmentRepository(conn)


@router.get("/equipment", response_model=list[EquipmentResponse])
def list_equipment(repo=Depends(get_repository)):
    use_case = ListEquipmentUseCase(repo)
    entities = use_case.execute()
    return [EquipmentResponse.model_validate(e.__dict__) for e in entities]


@router.get("/equipment/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(equipment_id: UUID, repo=Depends(get_repository)):
    use_case = GetEquipmentByIdUseCase(repo)
    try:
        entity = use_case.execute(equipment_id)
        return EquipmentResponse.model_validate(entity.__dict__)
    except EquipmentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/equipment", response_model=EquipmentResponse, status_code=201)
def create_equipment(body: CreateEquipmentRequest, repo=Depends(get_repository)):
    use_case = CreateEquipmentUseCase(repo)
    entity = use_case.execute(
        name=body.name,
        description=body.description,
        category=body.category,
        daily_rental_price=body.daily_rental_price,
    )
    return EquipmentResponse.model_validate(entity.__dict__)


@router.put("/equipment/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: UUID, body: UpdateEquipmentRequest, repo=Depends(get_repository)
):
    use_case = UpdateEquipmentUseCase(repo)
    try:
        entity = use_case.execute(
            equipment_id=equipment_id,
            name=body.name,
            description=body.description,
            category=body.category,
            daily_rental_price=body.daily_rental_price,
        )
        return EquipmentResponse.model_validate(entity.__dict__)
    except EquipmentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch("/equipment/{equipment_id}/toggle-status", response_model=EquipmentResponse)
def toggle_status(equipment_id: UUID, repo=Depends(get_repository)):
    use_case = ToggleEquipmentStatusUseCase(repo)
    try:
        entity = use_case.execute(equipment_id)
        return EquipmentResponse.model_validate(entity.__dict__)
    except EquipmentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.delete("/equipment/{equipment_id}", status_code=204)
def delete_equipment(equipment_id: UUID, repo=Depends(get_repository)):
    use_case = DeleteEquipmentUseCase(repo)
    try:
        use_case.execute(equipment_id)
    except EquipmentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
