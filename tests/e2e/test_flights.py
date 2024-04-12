import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

base_url = 'http://localhost:8000/api'

def test_get_apps_empty():
    assert requests.get(f'{base_url}/flights').json() == {'flights':[]}


def test_new_flight_success():
    dep_time = str(datetime.now().isoformat())
    arr_time = str(datetime.now().isoformat())
    resp = requests.post(f'{base_url}/flights/', json={
        'departure_time': dep_time,
        'arrival_time': arr_time,
        'departure_point': 'Berlin',
        'destination_point': 'Moscow',
    }).json()
    print(resp)
    UUID(resp['id'])
    assert resp['status'] == 'SCHEDULED'
    assert resp['arrival_time'] == arr_time + 'Z'
    assert resp['departure_time'] == dep_time + 'Z'
    assert resp['destination_point'] == 'Moscow'
    assert resp['departure_point'] == 'Berlin'


def test_get_flights_success():
    resp = requests.get(f'{base_url}/flights/').json()