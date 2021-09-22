from typing import List

from ..repository.infrastructure.datastore import Datastore
from ..models.boat_viewmodels import Boat
from ..repository.models.boat_datamodels import BoatDataModel

class BoatService:
    def __init__(self, db: Datastore):
        self._db = db

    def get_boats(self) -> List[Boat]:
        boats = []

        # TODO: This is better managed via the datastore class
        with self._db._session_local() as connection:
            for boat in connection.query(BoatDataModel):
                boats.append(boat.to_view_model())

        return boats
