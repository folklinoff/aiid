import pytest
import requests
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


def test_new_flight_malformed_time():
    new_flight = test_json_flight_berlin_moscow.copy()
    new_flight['departure_time'] = 12345
    create_response = requests.post(f'{base_url}/flights/', json=new_flight)
    assert create_response.status_code == status.HTTP_400_BAD_REQUEST


def test_new_flight_departure_later_than_arrival():
    new_flight = test_json_flight_berlin_moscow.copy()
    new_flight['departure_time'] = format_time(datetime.now() + timedelta(hours=2))
    new_flight['arrival_time'] = format_time(datetime.now() - timedelta(hours=2))
    create_response = requests.post(f'{base_url}/flights/', json=new_flight)
    assert create_response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_flight():
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_json_flight_berlin_moscow)
    
    get_response = requests.get(f'{base_url}/flights/{create_response_body['id']}')
    assert get_response.status_code == status.HTTP_200_OK
    
    get_response_body = get_response.json()
    assert create_response_body == get_response_body


def test_get_flight_does_not_exist():
    get_response = requests.get(f'{base_url}/flights/{uuid4()}')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_change_status():
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_json_flight_berlin_moscow)
    
    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'status': 'DELAYED'},
    )
    assert change_status_response.status_code == status.HTTP_200_OK
    
    change_status_response_body = change_status_response.json()
    expected_change_status_response_body = create_response_body
    expected_change_status_response_body['status'] = 'DELAYED'
    assert change_status_response_body == expected_change_status_response_body


def test_change_status_and_time():
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_json_flight_berlin_moscow)
    
    new_dep_time = datetime.now() + timedelta(hours=12)
    new_status_and_times = {
        'status': 'DELAYED',
        'departure_time': format_time(new_dep_time),
        'arrival_time': format_time(new_dep_time + flight_time),
    }
    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json=new_status_and_times,
    )
    assert change_status_response.status_code == status.HTTP_200_OK
    
    change_status_response_body = change_status_response.json()
    expected_change_status_response_body = create_response_body
    for key, val in new_status_and_times.items():
        expected_change_status_response_body[key] = val
        
    assert change_status_response_body == expected_change_status_response_body


def test_change_status_invalid_status_transformation():
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_json_flight_berlin_moscow)
    
    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'status': 'FINISHED'},
    )
    assert change_status_response.status_code == status.HTTP_400_BAD_REQUEST


def test_change_status_invalid_status():
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_json_flight_berlin_moscow)
    
    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'status': 'WHAAAAT'},
    )
    assert change_status_response.status_code == status.HTTP_400_BAD_REQUEST


def test_change_status_invalid_time():
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_json_flight_berlin_moscow)
    
    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'departure_time': format_time(datetime.now() - timedelta(hours=2))},
    )
    assert change_status_response.status_code == status.HTTP_400_BAD_REQUEST


def test_change_status_invalid_duration():
    create_response = requests.post(f'{base_url}/flights/', json=test_json_flight_berlin_moscow)
    assert create_response.status_code == status.HTTP_201_CREATED
    create_response_body = create_response.json()
    check_create_flight_response(create_response_body, test_json_flight_berlin_moscow)
    
    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'departure_time': format_time(datetime.now() + timedelta(hours=2)),
              'arrival_time': format_time(datetime.now() + timedelta(hours=1))},
    )
    assert change_status_response.status_code == status.HTTP_400_BAD_REQUEST


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