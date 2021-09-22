from sqlalchemy import Column, Integer, String

from ...models.boat_viewmodels import Boat

from .base_model import BaseModel

class BoatDataModel(BaseModel):
    __tablename__ = "boats"

    id = Column("id", Integer, primary_key=True)
    year = Column("year", Integer)
    make = Column("make", String(255))
    length_ft = Column("length_ft", Integer)

    def to_view_model(self) -> Boat:
        return Boat(
            year=self.year,
            make=self.make,
            length_ft=self.length_ft,
        )
