from pydantic import BaseModel

class Car(BaseModel):
    year: int
    make: str
    model: str
