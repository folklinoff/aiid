import pytest
import requests
import time
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from rest_framework import status

base_url = 'http://localhost:8000/api'

flight_time = timedelta(days=1)

def format_time(time: datetime):
    return str(time.isoformat()) + 'Z'

current_time = datetime.now()

dep_time = format_time(current_time)
arr_time = format_time(current_time + flight_time)
test_flight_json_flight_berlin_moscow = {
    'departure_time': dep_time,
    'arrival_time': arr_time,
    'departure_point': 'Berlin',
    'destination_point': 'Moscow',
}

test_flight_json_flight_moscow_berlin = {
    'departure_time': dep_time,
    'arrival_time': arr_time,
    'departure_point': 'Moscow',
    'destination_point': 'Berlin',
}

def new_json_ticket(seat_type, seat_position, cost):
    return {
        'seat_type': seat_type,
        'seat_position': seat_position,
        'cost': cost,
    }


def new_json_default_vip_ticket():
    return new_json_ticket('VIP', 'A5', 69420)


def new_json_default_regular_ticket():
    return new_json_ticket('REGULAR', 'B1', 42069)


def new_json_passenger(first_name: str, middle_name: str, last_name: str, birthday: datetime, gender):
    return {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'birthday': birthday,
        'gender': gender,
    }


def new_default_passenger():
    return new_json_passenger(
        'Alex',
        'Alex',
        'Alex',
        format_time(datetime(year=2000, month=1, day=1)),
        'MALE',
    )


def check_create_flight_response(resp, sent):
    assert is_valid_uuid(resp['id'])
    assert resp['status'] == 'SCHEDULED'
    assert resp['arrival_time'] == sent['arrival_time']
    assert resp['departure_time'] == sent['departure_time']
    assert resp['destination_point'] == sent['destination_point']
    assert resp['departure_point'] == sent['departure_point']


def check_create_ticket_response(resp, sent, flight_id):
    assert is_valid_uuid(resp['id'])
    assert resp['seat_type'] == sent['seat_type']
    assert is_valid_uuid(resp['passenger_id'])
    assert resp['flight_id'] == flight_id
    assert resp['seat_position'] == sent['seat_position']
    assert resp['cost'] == sent['cost']
    assert resp['available'] == True


def check_create_passenger_response(resp: dict, sent: dict):
    assert is_valid_uuid(resp['id'])
    assert resp['first_name'] == sent['first_name']
    assert resp['middle_name'] == sent['middle_name']
    assert resp['last_name'] == sent['last_name']
    assert resp['birthday'] == sent['birthday']
    assert resp['gender'] == sent['gender']


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def create_flight_successfully():
    create_response = requests.post(f'{base_url}/flights/', json=test_flight_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_flight_json_flight_berlin_moscow)
    tickets_response = requests.get(f'{base_url}/flights/{create_response.json()['id']}/tickets')
    assert tickets_response.status_code == status.HTTP_200_OK
    assert len(tickets_response.json()['tickets']) == 0
    return create_response_body


def create_ticket_successfully(flight_id: UUID, ticket: dict):
    create_response = requests.post(f'{base_url}/flights/{flight_id}/tickets', json=ticket)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_ticket_response(create_response_body, ticket, flight_id)
    return create_response_body


def create_passenger_successfully(passenger: dict):
    create_response = requests.post(f'{base_url}/passengers', json=passenger)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_passenger_response(create_response_body, passenger)
    return create_response_body

def get_flight_passengers(flight_id: UUID):
    passengers_response = requests.get(f'{base_url}/flights/{flight_id}/passengers')
    assert passengers_response.status_code == status.HTTP_200_OK
    operation_id = passengers_response.json()['operation_id']
    assert is_valid_uuid(operation_id)
    interval = 0.005
    deadline = datetime.now() + timedelta(minutes=10)
    while datetime.now() < deadline:
        get_operation_response = requests.get(f'{base_url}/operations/{operation_id}')
        assert get_operation_response.status_code == status.HTTP_200_OK
        operation_body = get_operation_response.json()
        if operation_body['done'] == False:
            time.sleep(interval)
            interval *= 2
        else:
            return operation_body['result']
    return None