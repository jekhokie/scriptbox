from typing import Optional
from fastapi import FastAPI

from .endpoints import cars, boats
from .settings import get_settings

settings = get_settings()

ENDPOINTS = [
    cars.endpoint,
    boats.endpoint,
]

def create_app() -> FastAPI:
    """Create an instance of the application and set up routes, models, etc."""
    app = FastAPI(
        title="FastAPI Template",
        openapi_url="/api/spec",
        docs_url="/api/docs",
        description="Sample FastAPI Template",
    )

    @app.get("/", include_in_schema=False)
    async def return_default_hello():
        return {"Testing environment setting value": f"{settings.environment}"}

    configure_routers(app)

    return app

def configure_routers(app: FastAPI) -> None:
    """Configure desired routes"""
    for endpoint in ENDPOINTS:
        app.include_router(endpoint.router, prefix="/api" + endpoint.prefix)

app = create_app()
