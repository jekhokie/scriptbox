from typing import List

from ..endpoints import Endpoint
from ..models.boat_viewmodels import Boat
from ..settings import get_settings
from ..repository.infrastructure.datastore import Datastore
from ..services.boat_service import BoatService

_settings = get_settings()

endpoint = Endpoint(prefix="/boats")

@endpoint.router.get("/", response_model=List[Boat], tags=["Boats"])
def get_boats():
    with Datastore(
        source=f"{__name__}.boats", settings=_settings
    ) as db:
        boats = BoatService(db=db).get_boats()
        return boats
