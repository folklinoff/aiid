from uuid import uuid4, UUID
from applications.models import Passenger

class PassengerRepository:
    def __init__(self) -> None:
        pass


    def get_all(self, limit: int, offset: int) -> Passenger:
        return passengers.items()[offset: offset + limit]


    def get_by_id(self, passenger_id) -> Passenger:
        if passenger_id in passengers:
            return passengers[passenger_id]
        return None 


    def get_by_ids(self, passenger_ids: list[UUID]) -> list[Passenger]:
        passenger_list = []
        for passenger_id in passenger_ids:
            passenger = passengers.get(passenger_id)
            if passenger is None:
                raise Exception()
            passenger_list.append(passenger)
        return passenger_list

    
    def delete(self, passenger_id) -> None:
        passengers.pop(passenger_id)
    

    def create(self, passenger: Passenger) -> Passenger:
        if passenger.id is None:
            passenger.id = uuid4()
        passengers[passenger.id] = passenger
        return passenger


passengers: dict[UUID, Passenger] = {}