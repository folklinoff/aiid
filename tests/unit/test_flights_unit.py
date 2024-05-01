from datetime import datetime, timedelta
from .general import *
from project.applications.models import *
from pytest import raises


def test_new_flight():
    dep_time = datetime.now()
    arr_time = datetime.now() + timedelta(hours=14)

    flight = Flight(dep_time, arrival_time=arr_time, departure_point='Moscow', destination_point='Berlin')    
    assert flight.__dict__ == {
        'id': flight.id,
        'status': FlightStates.SCHEDULED,
        'departure_time': dep_time,
        'arrival_time': arr_time,
        'departure_point': 'Moscow',
        'destination_point': 'Berlin',
    }


def test_new_flight_in_flight_service():
    flights_count = len(flight_service.get_all_flights(10000, 0).flights)
    flight = flight_service.create(new_test_flight())
    assert flight.__dict__ == {
        'id': flight.id,
        'status': FlightStates.SCHEDULED,
        'departure_time': dep_time,
        'arrival_time': arr_time,
        'departure_point': 'Moscow',
        'destination_point': 'Berlin',
    }
    assert len(flight_service.get_all_flights(10000, 0).flights) == flights_count + 1


def test_change_status_correct():
    flight = flight_service.create(new_test_flight())
    flight = flight_service.change_status(flight.id, FlightStates.CANCELLED)
    assert flight.status == FlightStates.CANCELLED


def test_change_status_incorrect_status_transformation():
    flight = flight_service.create(new_test_flight())
    with raises(StatusChangeError):
        flight = flight_service.change_status(flight.id, FlightStates.FINISHED)


def test_change_status_incorrect_status():
    flight = flight_service.create(new_test_flight())
    with raises(TypeError):
        flight = flight_service.change_status(flight.id, "WHAT THE HEEELLLL BRUH")


def test_change_status_correct_time():
    flight = flight_service.create(new_test_flight())
    flight = flight_service.change_status(flight.id, FlightStates.DELAYED, dep_time + timedelta(hours=1), arr_time + timedelta(hours=1))
    assert flight.status == FlightStates.DELAYED


def test_change_status_correct_time():
    flight = flight_service.create(new_test_flight())
    with raises(InvalidFlightTimesError):
        flight = flight_service.change_status(flight.id, FlightStates.DELAYED, dep_time + timedelta(hours=1), arr_time + timedelta(hours=2))