from applications.models import Flight
from uuid import uuid4, UUID

class FlightRepository:
    def __init__(self) -> None:
        pass

    def getAllFlights(self, limit: int, offset: int) -> list[Flight]:
        return list(flights.values())[offset: offset + limit]
    
    
    def getFlightById(self, id: UUID) -> Flight | None:
        return flights.get(id)
    

    def getAllPassengers(self, id) -> list[UUID]:
        return flightsPassengers[id]
    

    def create(self, flight: Flight) -> Flight:
        if flight.id is None:
            flight.id = uuid4()
        flights[flight.id] = flight
        return flight

flights: dict[UUID, Flight] = {}
flightsPassengers: dict[UUID, list[UUID]] = {}