import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

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
    resp = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow).json()
    check_create_flight_response(resp, test_json_flight_berlin_moscow)


def test_new_flight_success():
    resp = requests.post(f'{base_url}/flights/', json=test_json_flight_moscow_berlin).json()
    check_create_flight_response(resp, test_json_flight_moscow_berlin)
    resp = requests.get(f'{base_url}/flights/{resp['id']}').json()
    assert is_valid_uuid(resp['id'])
    resp['id'] = ''
    test_json_flight_moscow_berlin['id'] = ''
    test_json_flight_moscow_berlin['status'] = 'SCHEDULED'
    assert resp == test_json_flight_moscow_berlin


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
    