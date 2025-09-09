from typing import List, Optional
from typing_extensions import TypedDict


class Coordinates(TypedDict):
    latitude: float
    longitude: float


class Stop(TypedDict):
    name: str
    coordinates: Coordinates
    arrival_time: str
    departure_time: str


class TripDetails(TypedDict):
    trip_id: str
    route_id: str
    trip_headsign: str
    stops: List[Stop]

class Metadata(TypedDict):
    self: str
    city: str
    query_parameters: dict | None


class TripResponse(TypedDict):
    metadata: Metadata
    trip_details: Optional[TripDetails]