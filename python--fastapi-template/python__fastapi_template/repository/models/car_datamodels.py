from sqlalchemy import Column, Integer, String

from ...models.car_viewmodels import Car

from .base_model import BaseModel

class CarDataModel(BaseModel):
    __tablename__ = "cars"

    id = Column("id", Integer, primary_key=True)
    year = Column("year", Integer)
    make = Column("make", String(255))
    model = Column("model", String(255))

    def to_view_model(self) -> Car:
        return Car(
            year=self.year,
            make=self.make,
            model=self.model,
        )
