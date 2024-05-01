from uuid import UUID
from typing import Callable

from applications.models import *

from applications.repository.flight import FlightRepository
from applications.repository.ticket import TicketRepository
from applications.repository.passenger import PassengerRepository

from applications.scheduler import scheduler, DateTrigger

from .operations import OperationsService

class FlightService:
    def __init__(self, flight_repository: FlightRepository, ticket_repository: TicketRepository, passenger_repository: PassengerRepository, ops_service: OperationsService):
        self.ops_service: OperationsService = ops_service
        self.flight_repository: FlightRepository = flight_repository
        self.ticket_repository: TicketRepository = ticket_repository
        self.passenger_repo: PassengerRepository = passenger_repository
    

    def get_flight_by_id(self, flight_id: UUID) -> Flight:
        return self.flight_repository.get_flight_by_id(flight_id)
    
    
    def get_all_flights(self, limit: int, offset: int) -> FlightList:
        return FlightList(self.flight_repository.get_all_flights(limit=limit, offset=offset))


    def list_passengers(self, id: UUID, limit: int, offset: int):
        if self.flight_repository.get_flight_by_id(id) is None:
            raise KeyError('Flight not found')
        operation_id = self.ops_service.create_operation()
        scheduler.add_job(self._list_passengers(id, limit, offset),
                          trigger=DateTrigger(), args=(operation_id, ),)
        return operation_id


    def _list_passengers(self, id: UUID, limit: int, offset: int) -> Callable[[UUID], None]:
        def real_list_passengers(operation_id: UUID):
            passenger_ids = self.flight_repository.get_all_passengers(id, limit, offset)
            passengers = self.passenger_repo.get_by_ids(passenger_ids)
            self.ops_service.finish_operation(operation_id, PassengerList(passengers))
        return real_list_passengers


    def create(self, flight) -> Flight:
        return self.flight_repository.create(flight)
    

    def change_status(self, flight_id: UUID, status: FlightStates, departure_time: datetime = None, arrival_time: datetime = None) -> Flight:
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if flight is None:
            raise KeyError('Flight not found')
        
        flight.set_status(status)
        flight.reschedule(departure_time, arrival_time)
        self.flight_repository.create(flight)

        return self.flight_repository.get_flight_by_id(flight_id)


    def list_tickets(self, flight_id, limit: int, offset: int) -> list[Ticket]:
        return self.ticket_repository.get_by_flight_id(flight_id, limit, offset)
