from applications.models import Ticket
from applications.repository.flight import FlightRepository
from applications.repository.ticket import TicketRepository
from applications.repository.passenger import PassengerRepository
from applications.models import Passenger
from applications.models import Flight, Flights
from uuid import UUID


class FlightService:
    def __init__(self, flightRepo: FlightRepository, ticketRepo: TicketRepository, passengerRepo: PassengerRepository):
        self.flight_repository: FlightRepository = flightRepo
        self.ticket_repository: TicketRepository = ticketRepo
        self.passenger_repo: PassengerRepository = passengerRepo
    

    def get_flight_by_id(self, flight_id: UUID) -> Flight:
        return self.flight_repository.getFlightById(flight_id)
    
    
    def get_all_flights(self, limit, offset) -> Flights:
        return Flights(self.flight_repository.getAllFlights(limit=limit, offset=offset))


    def get_passengers(self, id):
        if self.flight_repository.getFlightById(id) is None:
            raise Exception('Flight not found')
        passenger_ids = self.flight_repository.getAllPassengers(id)
        passengers = self.passenger_repo.get_by_ids(passenger_ids)
        return passengers


    def create(self, flight) -> Flight:
        return self.flight_repository.create(flight)
    

    def update(self, flight) -> Flight:
        return self.flight_repository.create(flight)
    

    def changeStatus(self, flight_id, status) -> Flight:
        flight = self.flight_repository.getFlightById(flight_id)
        if flight is None:
            raise Exception('Flight not found')
        
        flight.setStatus(status)
        self.flight_repository.create(flight)

        return self.flight_repository.getFlightById(flight_id)


    def listPassengers(self, flight_id) -> list[Passenger]:
        return [self.passenger_repo.get_by_id(ticket.passenger_id) for ticket in self.listTickets(flight_id)]


    def listTickets(self, flight_id) -> list[Ticket]:
        return self.ticket_repository.get_by_flight_id(flight_id)
