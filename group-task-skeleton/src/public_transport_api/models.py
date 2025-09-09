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


class QueryParameters(TypedDict):
    trip_id: str
    city: str


class Metadata(TypedDict):
    self: str
    city: str
    query_parameters: QueryParameters


class TripResponse(TypedDict):
    metadata: Metadata
    trip_details: Optional[TripDetails]