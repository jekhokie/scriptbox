from typing import List

from ..repository.infrastructure.datastore import Datastore
from ..models.car_viewmodels import Car
from ..repository.models.car_datamodels import CarDataModel

class CarService:
    def __init__(self, db: Datastore):
        self._db = db

    def get_cars(self) -> List[Car]:
        cars = []

        # TODO: This is better managed via the datastore class
        with self._db._session_local() as connection:
            for car in connection.query(CarDataModel):
                cars.append(car.to_view_model())

        return cars
