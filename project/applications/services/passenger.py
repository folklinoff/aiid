from uuid import uuid4, UUID
from applications.models import Passenger
from applications.repository.passenger import PassengerRepository

class PassengerService:
    def __init__(self, repo: PassengerRepository):
        self.passenger_repository: PassengerRepository = repo 


    def create(self, passenger: Passenger):
        return self.passenger_repository.create(passenger)


    def get_by_id(self, id: UUID):
        return self.passenger_repository.get_by_id(id)


    def get_all(self, limit: int, offset: int):
        return self.passenger_repository.get_all(limit, offset)