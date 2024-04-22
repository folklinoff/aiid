from uuid import uuid4, UUID
from enum import Enum
from datetime import datetime, timedelta
import time


class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class SeatTypes(Enum):
    REGULAR = 'REGULAR'
    VIP = 'VIP'

class Ticket:
    def __init__(self, seat_type: SeatTypes, flight_id: UUID, seat_position: str, cost: str, uuid: UUID=None) -> None:
        self.id: UUID = uuid if uuid is not None else uuid4()
        self.seat_type: SeatTypes = SeatTypes(seat_type)
        self.flight_id: UUID = flight_id
        self.seat_position: str = seat_position
        self.cost: int = cost
        self.available: bool = True
        self.passenger_id: UUID = uuid4()
    
    def can_book(self) -> bool:
        return self.available

    def book(self, passenger_id: UUID) -> None:
        if not self.can_book():
            raise SeatNotAvailableError("cannot book ticket")
        self.available = False
        self.passenger_id = passenger_id
    
    def suits(self, needed_type: SeatTypes) -> None:
        return self.seat_type == needed_type


class TicketList:
    def __init__(self, tickets: list[Ticket]):
        self.tickets = tickets


class CreateTicketDTO:
    def __init__(self, seat_type: SeatTypes, seat_position: str, cost: str, flight_id: UUID) -> None:
        self.seat_type: SeatTypes = seat_type
        self.seat_position: str = seat_position
        self.cost: int = cost


class BookTicketDTO:
    def __init__(self, passenger_id):
        self.passenger_id = passenger_id


class FlightStates(Enum):
    SCHEDULED = 'SCHEDULED'
    READY = 'READY'
    IN_PROGRESS = 'IN_PROGRESS'
    CANCELLED = 'CANCELLED'
    DELAYED = 'DELAYED'
    FINISHED = 'FINISHED'


class StatusChangeError(BaseException):
    def __init__(self, message: object) -> None:
        self.message = message


class InvalidFlightTimesError(BaseException):
    def __init__(self, message: object) -> None:
        self.message = message


class SeatNotAvailableError(BaseException):
    def __init__(self, message: object) -> None:
        self.message = message

class CannotBuyTicketError(BaseException):
    def __init__(self, message: object) -> None:
        self.message = message


class CannotBookTicketError(BaseException):
    def __init__(self, message: object) -> None:
        self.message = message


class Passenger:
    def __init__(self, first_name: str, middle_name: str, last_name: str, birthday: datetime, gender: Gender) -> None:
        self.first_name: str = first_name
        self.middle_name: str = middle_name
        self.last_name: str = last_name
        self.birthday: datetime = birthday
        self.gender: Gender = Gender(gender)
        self.id = uuid4()


class PassengerList:
    def __init__(self, passengers: list[Passenger]):
        self.passengers = passengers


class Flight:
    def __init__(self, departure_time: datetime, arrival_time: datetime, departure_point: str, destination_point: str) -> None:
        if departure_time > arrival_time:
            raise InvalidFlightTimesError('departure time should be later then arrival time')
        self.id: UUID = uuid4()
        self.status: FlightStates = FlightStates.SCHEDULED
        self.departure_time: datetime = departure_time
        self.arrival_time: datetime = arrival_time
        self.departure_point: str = departure_point
        self.destination_point: str = destination_point


    def can_be_booked(self) -> bool:
        return self.status == FlightStates.DELAYED or self.status == FlightStates.SCHEDULED


    def is_status_transformation_possible(self, old: FlightStates, new: FlightStates) -> bool:        
        if old == new:
            return True
        
        available_status_tranformations = {
            frozenset([FlightStates.SCHEDULED, FlightStates.DELAYED]),
            frozenset([FlightStates.SCHEDULED, FlightStates.READY]),
            frozenset([FlightStates.DELAYED, FlightStates.CANCELLED]),
            frozenset([FlightStates.DELAYED, FlightStates.READY]),
            frozenset([FlightStates.READY, FlightStates.IN_PROGRESS]),
            frozenset([FlightStates.IN_PROGRESS, FlightStates.FINISHED])
        }
        return {old, new} in available_status_tranformations


    def setStatus(self, val: FlightStates) -> None:
        if not isinstance(val, FlightStates):
            raise TypeError('status must be an instance of flightStates Enum')
        if not self.is_status_transformation_possible(self.status, val):
            raise StatusChangeError('changing to this status is illegal')
        # заглушка для оповещения о задержке
        if val == FlightStates.DELAYED:
            print(f'flight with id {self.id} has been delayed')
        self.status = val
    

    def reschedule(self, departure_time: datetime = None, arrival_time: datetime = None):
        arrival_time = self.arrival_time if arrival_time is None else arrival_time
        departure_time = self.departure_time if departure_time is None else departure_time
        if self.departure_time > departure_time:
            raise InvalidFlightTimesError("new departure time should be later then the current")
        if departure_time > arrival_time:
            raise InvalidFlightTimesError("departure time should be earlier")
        new_duration = arrival_time - departure_time
        old_duration = self.arrival_time - self.departure_time
        if new_duration != old_duration:
            raise InvalidFlightTimesError(f'''flight duration cannot be changed 
                            (old: {self.arrival_time} - {self.departure_time} = {old_duration}; 
                            new: {arrival_time} - {departure_time} = {new_duration})''')
        self.departure_time = departure_time
        self.arrival_time = arrival_time


class ChangeFlightStatusDTO:
    def __init__(self, status, departure_time=None, arrival_time=None):
        self.status: FlightStates = FlightStates(status)
        self.departure_time: datetime = departure_time
        self.arrival_time: datetime = arrival_time


class FlightList:
    def __init__(self, flights: list[Flight]) -> None:
        self.flights = flights


class Operation:
    id: UUID
    done: bool

    def __init__(self, id: UUID, done: bool = False, result = None) -> None:
        self.id = id
        self.done = done
        self.result = result