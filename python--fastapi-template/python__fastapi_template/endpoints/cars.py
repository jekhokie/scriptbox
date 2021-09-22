from typing import List

from ..endpoints import Endpoint
from ..models.car_viewmodels import Car
from ..settings import get_settings
from ..repository.infrastructure.datastore import Datastore
from ..services.car_service import CarService

_settings = get_settings()

endpoint = Endpoint(prefix="/cars")

@endpoint.router.get("/", response_model=List[Car], tags=["Cars"])
def get_cars():
    with Datastore(
        source=f"{__name__}.cars", settings=_settings
    ) as db:
        cars = CarService(db=db).get_cars()
        return cars
