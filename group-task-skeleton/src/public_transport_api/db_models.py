from typing import NamedTuple


class TripBasicInfo(NamedTuple):
    route_id: str
    trip_headsign: str


class StopInfo(NamedTuple):
    stop_name: str
    stop_lat: float
    stop_lon: float
    arrival_time: str
    departure_time: str