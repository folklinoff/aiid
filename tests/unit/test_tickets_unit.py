from pytest import raises
from .general import *
from project.applications.models import SeatNotAvailableError


def test_new_ticket():
    flight = flight_service.create(new_test_flight())
    test_ticket = new_test_ticket(flight.id)
    ticket = ticket_service.create(new_test_ticket(flight.id))
    test_ticket.id = ticket.id
    test_ticket.passenger_id = ticket.passenger_id
    assert ticket.__dict__ == test_ticket.__dict__
    assert len(flight_service.list_tickets(flight.id, 1000000, 0)) == 1


def test_book_ticket():
    flight = flight_service.create(new_test_flight())
    test_ticket = new_test_ticket(flight.id)
    ticket = ticket_service.create(new_test_ticket(flight.id))
    test_ticket.id = ticket.id
    test_ticket.passenger_id = ticket.passenger_id
    assert ticket.__dict__ == test_ticket.__dict__
    assert len(flight_service.list_tickets(flight.id, 1000000, 0)) == 1
    passenger = passenger_service.create(new_test_passenger())
    ticket_service.book_ticket(ticket.id, passenger.id)


def test_book_ticket_not_available():
    flight = flight_service.create(new_test_flight())
    test_ticket = new_test_ticket(flight.id)
    ticket = ticket_service.create(new_test_ticket(flight.id))
    test_ticket.id = ticket.id
    test_ticket.passenger_id = ticket.passenger_id
    assert ticket.__dict__ == test_ticket.__dict__
    assert len(flight_service.list_tickets(flight.id, 1000000, 0)) == 1
    passenger = passenger_service.create(new_test_passenger())
    ticket_service.book_ticket(ticket.id, passenger.id)
    passenger = passenger_service.create(new_test_passenger())
    with raises(SeatNotAvailableError):
        ticket_service.book_ticket(ticket.id, passenger.id)
