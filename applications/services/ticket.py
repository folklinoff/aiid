from uuid import uuid4, UUID
from applications.models import Ticket
from applications.repository.ticket import TicketRepository
from applications.repository.flight import FlightRepository
from applications.repository.passenger import PassengerRepository
from applications.models import SeatNotAvailableException, TicketDoesntExistException, PassengerDoesntExistException, CannotBuyTicketException, CannotBookTicketOnThisFlight
from applications.models import FlightStates

class TicketService:
    def __init__(self, ticket_repository: TicketRepository, flight_repository: FlightRepository, passenger_repository: PassengerRepository) -> None:
        self.ticket_repository: TicketRepository = ticket_repository
        self.flight_repository: FlightRepository = flight_repository
        self.passenger_repository: PassengerRepository = passenger_repository
    
    
    def create(self, t: Ticket) -> Ticket:
        return self.ticket_repository.create(t)
    
    
    def get_by_id(self, id: UUID) -> Ticket:
        return self.ticket_repository.get_by_id(id)
    
    
    def get_by_flight_id(self, flight_id: UUID, limit: int, offset: int) -> list[Ticket]:
        return self.ticket_repository.get_by_flight_id(flight_id, limit, offset)
    

    def book_ticket(self, ticket_id, passenger_id) -> Ticket:
        ticket = self.ticket_repository.get_by_id(ticket_id)
        if ticket is None:
            raise TicketDoesntExistException('ticket with this id doesn\'t exist')
        
        if not ticket.can_book():
            raise SeatNotAvailableException('this seat is already booked')
        
        if self.passenger_repository.get_by_id(passenger_id) is None:
            raise PassengerDoesntExistException('passenger with this id doesn\'t exist')
        
        flight = self.flight_repository.get_flight_by_id(ticket.flight_id)
        if not flight.can_be_booked():
            raise CannotBuyTicketException('cannot buy ticket on this flight')

        ticket.book(passenger_id)
        self.ticket_repository.create(ticket)
        self.flight_repository.add_passenger(ticket)

        return ticket
    