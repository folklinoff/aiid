from uuid import uuid4, UUID
from applications.models import Ticket
from applications.repository.ticket import TicketRepository
from applications.repository.flight import FlightRepository
from applications.models import SeatNotAvailableException, TicketDoesntExistException, PassengerDoesntExistException, CannotBuyTicketException, CannotBookTicketOnThisFlight
from applications.models import FlightStates

class TicketService:
    def __init__(self, ticket_repository: TicketRepository, flight_repository: FlightRepository) -> None:
        self.ticket_repository: TicketRepository = ticket_repository
        self.flight_repository: FlightRepository = flight_repository
    
    
    def create(self, t: Ticket) -> Ticket:
        return self.ticket_repository.create(t)
    
    
    def get_by_id(self, id: UUID) -> Ticket:
        return self.ticket_repository.get_by_id(id)
    
    
    def get_by_flight_id(self, flight_id: UUID) -> list[Ticket]:
        return self.ticket_repository.get_by_flight_id(flight_id)
    

    def bookTicket(self, ticketId, passengerId) -> Ticket:
        ticket = self.ticket_repository.get_by_id(ticketId)

        if ticket is None:
            raise TicketDoesntExistException('ticket with this id doesn\'t exist')
        
        if not ticket.canBook():
            raise SeatNotAvailableException('this seat is already booked')
        
        if self.passenger_repo.get_by_id(passengerId) is None:
            raise PassengerDoesntExistException('passenger with this id doesn\'t exist')
        
        flight = self.flight_repository.getFlightById(ticket.flightId)
        if not flight.canBeBooked():
            raise CannotBuyTicketException('cannot buy ticket on this flight')

        ticket.book(passengerId)
        return ticket
    