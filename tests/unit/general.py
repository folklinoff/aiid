from datetime import datetime, timedelta
from project.applications.factory import *
from project.applications.models import Flight, Ticket, SeatTypes, Passenger, Gender
from uuid import UUID

flight_service = FlightServiceFactory.create_flight()
ticket_service = TicketServiceFactory.create_ticket()
passenger_service = PassengerRepositoryFactory.create_passenger()

dep_time = datetime.now()
arr_time = datetime.now() + timedelta(hours=14)
birthday = datetime.now() - timedelta(days=365*20)

def new_test_flight():
    return Flight(dep_time, arrival_time=arr_time, departure_point='Moscow', destination_point='Berlin')


def new_test_passenger():
    return Passenger("Alex", "Alex", "Alex", birthday, Gender.MALE)


def new_test_ticket(flight_id: UUID) -> Ticket:
    return Ticket(SeatTypes.REGULAR, flight_id, "A3", 1000)

