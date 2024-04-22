import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from rest_framework import status
from .base import *


def test_new_flight_success():
    prev_flights_response = requests.get(f'{base_url}/flights')
    assert prev_flights_response.status_code == status.HTTP_200_OK
    prev_flights = prev_flights_response.json()
    create_flight_successfully()
    new_flights_response = requests.get(f'{base_url}/flights')
    assert new_flights_response.status_code == status.HTTP_200_OK
    assert len(new_flights_response.json()['flights']) == len(prev_flights['flights'])+1


def test_new_flight_malformed_time():
    new_flight = test_flight_json_flight_berlin_moscow.copy()
    new_flight['departure_time'] = 12345
    create_response = requests.post(f'{base_url}/flights/', json=new_flight)
    assert create_response.status_code == status.HTTP_400_BAD_REQUEST


def test_new_flight_departure_later_than_arrival():
    new_flight = test_flight_json_flight_berlin_moscow.copy()
    new_flight['departure_time'] = format_time(datetime.now() + timedelta(hours=2))
    new_flight['arrival_time'] = format_time(datetime.now() - timedelta(hours=2))
    create_response = requests.post(f'{base_url}/flights/', json=new_flight)
    assert create_response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_flight():
    create_response_body = create_flight_successfully()
    get_response = requests.get(f'{base_url}/flights/{create_response_body['id']}')
    assert get_response.status_code == status.HTTP_200_OK
    
    get_response_body = get_response.json()
    assert create_response_body == get_response_body


def test_get_flight_does_not_exist():
    get_response = requests.get(f'{base_url}/flights/{uuid4()}')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_change_status():
    create_response_body = create_flight_successfully()

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
    create_response_body = create_flight_successfully()
    
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
    create_response_body = create_flight_successfully()

    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'status': 'FINISHED'},
    )
    assert change_status_response.status_code == status.HTTP_400_BAD_REQUEST


def test_change_status_invalid_status():
    create_response_body = create_flight_successfully()
    
    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'status': 'WHAAAAT'},
    )
    assert change_status_response.status_code == status.HTTP_400_BAD_REQUEST


def test_change_status_invalid_time():
    create_response_body = create_flight_successfully()
    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'departure_time': format_time(datetime.now() - timedelta(hours=2))},
    )
    assert change_status_response.status_code == status.HTTP_400_BAD_REQUEST


def test_change_status_invalid_duration():
    create_response_body = create_flight_successfully()

    change_status_response = requests.post(
        f'{base_url}/flights/{create_response_body['id']}:change_status', 
        json={'departure_time': format_time(datetime.now() + timedelta(hours=2)),
              'arrival_time': format_time(datetime.now() + timedelta(hours=1))},
    )
    assert change_status_response.status_code == status.HTTP_400_BAD_REQUEST
