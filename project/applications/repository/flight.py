from applications.models import Flight
from applications.models import Passenger
from uuid import uuid4, UUID

class FlightRepository:
    def __init__(self) -> None:
        pass

    def get_all_flights(self, limit: int, offset: int) -> list[Flight]:
        return list(flights.values())[offset: offset + limit]
    
    
    def get_flight_by_id(self, id: UUID) -> Flight | None:
        return flights[id]
    

    def add_passenger(self, id: UUID, passenger_id: UUID):
        if not passenger_id in flights_passengers[id]:
            flights_passengers[id].append(passenger_id)


    def get_all_passengers(self, id: UUID, limit: int, offset: int) -> list[UUID]:
        return sorted(flights_passengers[id])[offset: limit + offset]
    

    def create(self, flight: Flight) -> Flight:
        if flight.id is None:
            flight.id = uuid4()
        flights[flight.id] = flight
        flights_passengers[flight.id] = flights_passengers[flight.id] if flight.id in flights_passengers.keys() else []
        return flight

flights: dict[UUID, Flight] = {}
flights_passengers: dict[UUID, list[UUID]] = {}