import pytest
import requests
from rest_framework import status
from .base import *

def test_create_ticket():
    create_flight_response_body = create_flight_successfully()
    create_ticket_response_body = create_ticket_successfully(create_flight_response_body['id'], new_json_default_vip_ticket())
    get_tickets_response = requests.get(f'{base_url}/flights/{create_flight_response_body['id']}/tickets')
    assert get_tickets_response.status_code == status.HTTP_200_OK
    tickets = get_tickets_response.json()['tickets']
    assert len(tickets) == 1
    assert tickets[0] == create_ticket_response_body


def test_create_ticket_flight_does_not_exist():
    assert requests.post(f'{base_url}/flights/{uuid4()}/tickets', json=new_json_default_vip_ticket()).status_code == status.HTTP_404_NOT_FOUND


def test_create_ticket_invalid_seat_type():
    new_ticket = new_json_default_vip_ticket()
    new_ticket['seat_type'] = 'WRONG'
    assert requests.post(f'{base_url}/flights/{uuid4()}/tickets', json=new_ticket).status_code == status.HTTP_400_BAD_REQUEST


def test_create_ticket_invalid_field_type():
    new_ticket = new_json_default_vip_ticket()
    new_ticket['cost'] = 'lol'
    assert requests.post(f'{base_url}/flights/{uuid4()}/tickets', json=new_ticket).status_code == status.HTTP_400_BAD_REQUEST


def test_get_ticket():
    create_flight_response_body = create_flight_successfully()
    create_ticket_response_body = create_ticket_successfully(create_flight_response_body['id'], new_json_default_vip_ticket())
    get_ticket_response = requests.get(f'{base_url}/tickets/{create_ticket_response_body['id']}')
    assert get_ticket_response.status_code == status.HTTP_200_OK
    assert get_ticket_response.json() == create_ticket_response_body


def test_get_ticket_non_existent():
    assert requests.get(f'{base_url}/tickets/{uuid4()}').status_code == status.HTTP_404_NOT_FOUND


def test_book_ticket():
    create_flight_response_body = create_flight_successfully()
    create_ticket_response_body = create_ticket_successfully(create_flight_response_body['id'], new_json_default_vip_ticket())
    create_passenger_response_body = create_passenger_successfully(new_default_passenger())
    book_ticket_response = requests.post(f'{base_url}/tickets/{create_ticket_response_body['id']}:book', json={'passenger_id': create_passenger_response_body['id']})
    assert book_ticket_response.status_code == status.HTTP_200_OK
    assert book_ticket_response.json()['available'] == False
    passenger_list = get_flight_passengers(create_flight_response_body['id'])
    assert passenger_list is not None
    assert len(passenger_list['passengers']) == 1
    assert passenger_list['passengers'][0] == create_passenger_response_body


def test_book_ticket_twice():
    create_flight_response_body = create_flight_successfully()
    create_ticket_response_body = create_ticket_successfully(create_flight_response_body['id'], new_json_default_vip_ticket())
    passenger1_id = create_passenger_successfully(new_default_passenger())['id']
    passenger2_id = create_passenger_successfully(new_default_passenger())['id']
    book_ticket_response = requests.post(f'{base_url}/tickets/{create_ticket_response_body['id']}:book', json={'passenger_id': passenger1_id})
    assert book_ticket_response.status_code == status.HTTP_200_OK
    assert book_ticket_response.json()['available'] == False
    book_ticket_response = requests.post(f'{base_url}/tickets/{create_ticket_response_body['id']}:book', json={'passenger_id': passenger2_id})
    assert book_ticket_response.status_code == status.HTTP_400_BAD_REQUEST


def test_book_ticket_ticket_does_not_exist():
    create_passenger_response_body = create_passenger_successfully(new_default_passenger())
    book_ticket_response = requests.post(f'{base_url}/tickets/{uuid4()}:book', json={'passenger_id': create_passenger_response_body['id']})
    assert book_ticket_response.status_code == status.HTTP_404_NOT_FOUND


def test_book_ticket_passenger_does_not_exist():
    create_flight_response_body = create_flight_successfully()
    create_ticket_response_body = create_ticket_successfully(create_flight_response_body['id'], new_json_default_vip_ticket())
    book_ticket_response = requests.post(f'{base_url}/tickets/{create_ticket_response_body['id']}:book', json={'passenger_id': str(uuid4())})
    assert book_ticket_response.status_code == status.HTTP_404_NOT_FOUND
    get_ticket_response = requests.get(f'{base_url}/tickets/{create_ticket_response_body['id']}')
    assert get_ticket_response.status_code == status.HTTP_200_OK
    assert get_ticket_response.json()['available'] == True
    