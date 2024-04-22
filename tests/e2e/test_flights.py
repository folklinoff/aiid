import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime
from rest_framework import status

base_url = 'http://localhost:8000/api'

dep_time = str(datetime.now().isoformat())+'Z'
arr_time = str(datetime.now().isoformat())+'Z'
test_json_flight_berlin_moscow = {
    'departure_time': dep_time,
    'arrival_time': arr_time,
    'departure_point': 'Berlin',
    'destination_point': 'Moscow',
}

test_json_flight_moscow_berlin = {
    'departure_time': dep_time,
    'arrival_time': arr_time,
    'departure_point': 'Moscow',
    'destination_point': 'Berlin',
}


def test_new_flight_success():
    prev_flights_response = requests.get(f'{base_url}/flights')
    assert prev_flights_response.status_code == status.HTTP_200_OK
    prev_flights = prev_flights_response.json()
    
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    check_create_flight_response(create_response.json(), test_json_flight_berlin_moscow)
    
    new_flights_response = requests.get(f'{base_url}/flights')
    assert new_flights_response.status_code == status.HTTP_200_OK
    assert len(new_flights_response.json()['flights']) == len(prev_flights['flights'])+1


def test_get_flight():
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_json_flight_berlin_moscow)
    
    get_response = requests.get(f'{base_url}/flights/{create_response_body['id']}')
    assert get_response.status_code == status.HTTP_200_OK
    
    get_response_body = get_response.json()
    assert create_response_body == get_response_body


def test_get_flight_change_status():
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_json_flight_berlin_moscow)
    get_resp = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'status': 'DELAYED'},
    ).json()
    


def check_create_flight_response(resp, sent):
    assert is_valid_uuid(resp['id'])
    assert resp['status'] == 'SCHEDULED'
    assert resp['arrival_time'] == sent['arrival_time']
    assert resp['departure_time'] == sent['departure_time']
    assert resp['destination_point'] == sent['destination_point']
    assert resp['departure_point'] == sent['departure_point']


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
    