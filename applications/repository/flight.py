from applications.models import Flight
from uuid import uuid4, UUID

class FlightRepository:
    def __init__(self) -> None:
        # все пассажиры
        pass

    def getAllFlights(self, offset: int, limit: int) -> list[Flight]:
        return list(flights.values())[offset: offset + limit]
    
    def getFlightById(self, id: UUID) -> Flight | None:
        return flights[id] if id in flights else None
    
    def create(self, flight: Flight) -> Flight:
        if flight.id is None:
            flight.id = uuid4()
        flights[flight.id] = flight
        return flight

flights: dict[UUID, Flight] = {}