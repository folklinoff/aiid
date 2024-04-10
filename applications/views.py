from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket, Passenger
from rest_framework.decorators import action
from applications.factory import FlightServiceFactory, TicketServiceFactory, PassengerServiceFactory
from applications.serializers import GetFlightsQuerySerializer, FlightsSerializer, NewFlightSerializer, FlightDetailsSerializer, NewTicketSerializer, TicketSerializer, BookTicketDTOSerializer, TicketsListSerializer, PassengerListSerializer, PassengerSerializer, NewPassengerSerializer
from uuid import UUID

class FlightsViewSet(ViewSet):
    flightService = FlightServiceFactory.create_flight()
    ticketService = TicketServiceFactory.create_ticket()
    passengerService = PassengerServiceFactory.create_passenger()

    def list(self, request):
        query_ser = GetFlightsQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(query_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        print({**query_ser.data})
        flights = self.flightService.get_all_flights(**query_ser.data)
        return Response(FlightsSerializer(flights).data, status=status.HTTP_200_OK)
    
    
    def create(self, request):
        request_ser = NewFlightSerializer(data=request.data)
        if not request_ser.is_valid():
            return Response(request_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        flight = self.flightService.create(request_ser.save())
        return Response(FlightDetailsSerializer(flight).data, status=status.HTTP_201_CREATED)
    

    def retrieve(self, _, id=None):
        flight = self.flightService.get_flight_by_id(UUID(id))
        return Response(FlightDetailsSerializer(flight).data, status=status.HTTP_200_OK)


    def update(self, request):
        body_ser = NewFlightSerializer(data=request.data)
        if not body_ser.is_valid():
            return Response(body_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        flight = self.flightService.update(body_ser.save())
        return Response(FlightDetailsSerializer(flight).data, status=status.HTTP_200_OK)


    @action(detail=True)
    def create_ticket(self, request, id=None):
        body_ser = NewTicketSerializer(data=request.body)
        if not body_ser.is_valid():
            return Response(body_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        ticket = Ticket(**body_ser.data, flightId=UUID(id))
        ticket = self.ticketService.create(ticket)
        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)


    @action(detail=False)
    def list_tickets(self, _, id=None):
        tickets = self.ticketService.get_by_flight_id(UUID(id))
        return Response(TicketsListSerializer(tickets), status=status.HTTP_200_OK)
    

    @action(detail=False)
    def list_passengers(self, _, id=None):
        passengers = self.flightService.get_passengers(UUID(id))
        return Response(PassengerListSerializer(passengers).data, status=status.HTTP_200_OK)


class TicketsViewSet(ViewSet):
    ticketsService = TicketServiceFactory.create_ticket()

    @action(detail=True)
    def book(self, request, id=None):
        body_ser = BookTicketDTOSerializer(data=request.body)
        if not body_ser.is_valid():
            return Response(body_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        ticket = self.ticketsService.bookTicket(UUID(id), body_ser["passenger_id"])
        return Response(TicketSerializer(ticket).data, status=status.HTTP_200_OK)


class PassengerViewSet(ViewSet):
    passengerService = PassengerServiceFactory.create_passenger()

    def create(self, request):
        body_ser = NewPassengerSerializer(data=request.data)
        if not body_ser.is_valid():
            return Response(body_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        passenger = self.passengerService.create(Passenger(**body_ser.data))
        return Response(PassengerSerializer(passenger).data, status=status.HTTP_201_CREATED)