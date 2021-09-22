from typing import Optional
from fastapi import FastAPI

from .settings import get_settings

settings = get_settings()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Environment from Settings": f"{settings.environment}"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
