from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from ..domain.equipment.exceptions import EquipmentNotFoundError
from .equipment.router import router as equipment_router


def create_app() -> FastAPI:
    app = FastAPI(title="RentFlow API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(EquipmentNotFoundError)
    async def equipment_not_found_handler(request: Request, exc: EquipmentNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.errors()},
        )

    app.include_router(equipment_router)
    return app


app = create_app()

