import requests
from rest_framework import status
from .base import *

def test_create_passenger():
    prev_passengers_response = requests.get(f'{base_url}/passengers')
    assert prev_passengers_response.status_code == status.HTTP_200_OK
    prev_passengers = prev_passengers_response.json()
    create_passenger_successfully(new_default_passenger())
    new_passengers_response = requests.get(f'{base_url}/passengers')
    assert new_passengers_response.status_code == status.HTTP_200_OK
    assert len(new_passengers_response.json()['passengers']) == len(prev_passengers['passengers'])+1


def test_create_passenger_invalid_field_type():
    passenger = new_default_passenger()
    passenger['birthday'] = 'this is TOTALLY AND UTTERLY WRONG'
    assert requests.post(f'{base_url}/passengers', json=passenger).status_code == status.HTTP_400_BAD_REQUEST


def test_create_passenger_invalid_gender():
    passenger = new_default_passenger()
    passenger['gender'] = 'there are more than 2 genders'
    assert requests.post(f'{base_url}/passengers', json=passenger).status_code == status.HTTP_400_BAD_REQUEST
    