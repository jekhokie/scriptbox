from pydantic import BaseModel

class Boat(BaseModel):
    year: int
    make: str
    length_ft: int
