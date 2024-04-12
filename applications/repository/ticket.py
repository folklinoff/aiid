from uuid import uuid4, UUID
from applications.models import Ticket


class TicketRepository:
    def __init__(self) -> None:
        pass

    
    def get_by_id(self, ticket_id: int) -> Ticket | None:
        return tickets[ticket_id] if ticket_id in tickets else None

    
    def get_by_flight_id(self, flight_id: int, limit: int, offset: int) -> list[Ticket]:
        return sorted([ticket for ticket in tickets if ticket.flightId == flight_id])[offset:offset+limit]


    def delete(self, ticket_id: int) -> None:
        tickets.pop(ticket_id)


    def create(self, ticket: Ticket) -> Ticket:
        if ticket.id is None:
            ticket.id = uuid4()
        tickets[ticket.id] = ticket
        return ticket


tickets: dict[UUID, Ticket] = {}