from uuid import uuid4, UUID
from enum import Enum
from datetime import datetime


class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class SeatTypes(Enum):
    REGULAR = 'REGULAR'
    VIP = 'VIP'

class Ticket:
    def __init__(self, seatType: SeatTypes, flightId: UUID, seatPosition: str, cost: str, uuid: UUID=uuid4()) -> None:
        self.id: UUID = uuid if uuid is not None else uuid4()
        self.seatType: SeatTypes = seatType
        self.flightId: UUID = flightId
        self.seatPosition: str = seatPosition
        self.cost: int = cost
        self.available: bool = True
        self.passengerId: UUID = uuid4()
    
    def canBook(self) -> bool:
        return self.available

    def book(self, passengerId: UUID) -> None:
        if self.canBook():
            raise SeatNotAvailableException("cannot book ticket")
        self.available = False
        self.passengerId = passengerId
    
    def suits(self, neededType: SeatTypes) -> None:
        return self.seatType == neededType

class CreateTicketDTO:
    def __init__(self, seatType: SeatTypes, seatPosition: str, cost: str) -> None:
        self.seatType: SeatTypes = seatType
        self.seatPosition: str = seatPosition
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


class StatusChangeException(Exception):
    def __init__(self, message: object) -> None:
        self.message = message


class SeatNotAvailableException(Exception):
    def __init__(self, message: object) -> None:
        self.message = message


class TicketDoesntExistException(Exception):
    def __init__(self, message: object) -> None:
        self.message = message


class PassengerDoesntExistException(Exception):
    def __init__(self, message: object) -> None:
        self.message = message


class CannotBuyTicketException(Exception):
    def __init__(self, message: object) -> None:
        self.message = message


class CannotBookTicketOnThisFlight(Exception):
    def __init__(self, message: object) -> None:
        self.message = message


class Passenger:
    def __init__(self, firstName: str, middleName: str, lastName: str, birthday: datetime, gender: Gender) -> None:
        self.firstName: str = firstName
        self.middleName: str = middleName
        self.lastName: str = lastName
        self.birthday: datetime = birthday
        self.gender: Gender = gender
        self.id = uuid4()


class Flight:
    def __init__(self, departure_time: datetime, arrival_time: datetime, departure_point: str, destination_point: str) -> None:
        self.id: UUID = uuid4()
        self.status: FlightStates = FlightStates.SCHEDULED
        self.departure_time: datetime = departure_time
        self.arrival_time: datetime = arrival_time
        self.departure_point: str = departure_point
        self.destination_point: str = destination_point


    def canBeBooked(self) -> bool:
        return self.status == FlightStates.DELAYED or self.status == FlightStates.SCHEDULED


    def isStatusTransformationPossible(self, old: FlightStates, new: FlightStates) -> bool:        
        if old == new:
            return True
        
        availableStatusTranformations = {
            frozenset([FlightStates.SCHEDULED, FlightStates.DELAYED]),
            frozenset([FlightStates.SCHEDULED, FlightStates.READY]),
            frozenset([FlightStates.DELAYED, FlightStates.CANCELLED]),
            frozenset([FlightStates.DELAYED, FlightStates.READY]),
            frozenset([FlightStates.READY, FlightStates.IN_PROGRESS]),
            frozenset([FlightStates.IN_PROGRESS, FlightStates.FINISHED])
        }
        return {old, new} in availableStatusTranformations

    def setStatus(self, val: FlightStates) -> None:
        if not isinstance(val, FlightStates):
            raise TypeError('status must be an instance of flightStates Enum')
        if not self.isStatusTransformationPossible(self.status, val):
            raise StatusChangeException('changing to this status is illegal')
        # заглушка для оповещения о задержке
        if val == FlightStates.DELAYED:
            print(f'flight with id {self.id} has been delayed')
        self.status = val


class Flights:
    def __init__(self, flights: list[Flight]) -> None:
        self.flights = flights