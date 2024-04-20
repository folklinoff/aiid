from typing import Any
from applications.services.flight import FlightService
from applications.services.passenger import PassengerService
from applications.services.ticket import TicketService
from applications.services.operations import OperationsService
from applications.repository.flight import FlightRepository
from applications.repository.airport import AirportRepository
from applications.repository.ticket import TicketRepository
from applications.repository.passenger import PassengerRepository


flightRepository = FlightRepository()
airportRepository = AirportRepository()
ticketRepository = TicketRepository()
passengerRepository = PassengerRepository()


class FlightRepositoryFactory:
    @staticmethod
    def create_flight():
        return flightRepository


class AirportRepositoryFactory:
    @staticmethod
    def create_airport():
        return airportRepository
    

class PassengerRepositoryFactory:
    @staticmethod
    def create_passenger():
        return passengerRepository


class TicketRepositoryFactory:
    @staticmethod
    def create_ticket():
        return ticketRepository


operationService = OperationsService()
class OperationServiceFactory:
    @staticmethod
    def create_operation():
        return operationService


flightService = FlightService(FlightRepositoryFactory.create_flight(), TicketRepositoryFactory.create_ticket(), PassengerRepositoryFactory.create_passenger(), OperationServiceFactory.create_operation())
passengerService = PassengerService(PassengerRepositoryFactory.create_passenger())
ticketService = TicketService(TicketRepositoryFactory.create_ticket(), FlightRepositoryFactory.create_flight(), PassengerRepositoryFactory.create_passenger())

class FlightServiceFactory:
    @staticmethod
    def create_flight():
        return flightService


class PassengerServiceFactory:
    @staticmethod
    def create_passenger():
        return passengerService


class TicketServiceFactory:
    @staticmethod
    def create_ticket():
        return ticketService
