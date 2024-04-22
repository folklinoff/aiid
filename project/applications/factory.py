from typing import Any
from applications.services.flight import FlightService
from applications.services.passenger import PassengerService
from applications.services.ticket import TicketService
from applications.services.operations import OperationsService
from applications.repository.flight import FlightRepository
from applications.repository.airport import AirportRepository
from applications.repository.ticket import TicketRepository
from applications.repository.passenger import PassengerRepository


flight_repository = FlightRepository()
airport_repository = AirportRepository()
ticket_repository = TicketRepository()
passenger_repository = PassengerRepository()


class FlightRepositoryFactory:
    @staticmethod
    def create_flight():
        return flight_repository


class AirportRepositoryFactory:
    @staticmethod
    def create_airport():
        return airport_repository
    

class PassengerRepositoryFactory:
    @staticmethod
    def create_passenger():
        return passenger_repository


class TicketRepositoryFactory:
    @staticmethod
    def create_ticket():
        return ticket_repository


operationService = OperationsService()
class OperationServiceFactory:
    @staticmethod
    def create_operation():
        return operationService


flight_service = FlightService(FlightRepositoryFactory.create_flight(), TicketRepositoryFactory.create_ticket(), PassengerRepositoryFactory.create_passenger(), OperationServiceFactory.create_operation())
passenger_service = PassengerService(PassengerRepositoryFactory.create_passenger())
ticket_service = TicketService(TicketRepositoryFactory.create_ticket(), FlightRepositoryFactory.create_flight(), PassengerRepositoryFactory.create_passenger())

class FlightServiceFactory:
    @staticmethod
    def create_flight():
        return flight_service


class PassengerServiceFactory:
    @staticmethod
    def create_passenger():
        return passenger_service


class TicketServiceFactory:
    @staticmethod
    def create_ticket():
        return ticket_service
