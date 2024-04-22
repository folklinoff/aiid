from uuid import UUID

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Ticket, Passenger, PassengerList, TicketList
from applications.factory import *
from applications.serializers import *

@extend_schema_view(
    list=extend_schema(summary='Flights list', 
                    parameters=[GetMultipleItemsQuerySerializer], auth=False,
                    responses={
                        status.HTTP_200_OK: FlightsSerializer,
                    }),
    create=extend_schema(summary='New flight', 
                    request=NewFlightSerializer,
                    responses={
                        status.HTTP_201_CREATED: FlightDetailsSerializer,
                    }),
    retrieve=extend_schema(summary='One flight', 
                    description='Allows to get one flight by it\'s ID or returns error',
                    responses={
                        status.HTTP_200_OK: FlightDetailsSerializer,
                    }),
    update=extend_schema(summary='New flight', 
                    request=NewChangeFlightStatusDTOSerializer,
                    responses={
                        status.HTTP_200_OK: FlightDetailsSerializer,
                    }),
    create_ticket=extend_schema(summary='New ticket boom', 
                    request=NewTicketSerializer,
                    responses={
                        status.HTTP_201_CREATED: TicketSerializer,
                    }),
    list_tickets=extend_schema(summary='Get all tickets', 
                    request=GetMultipleItemsQuerySerializer,
                    responses={
                        status.HTTP_200_OK: TicketsListSerializer,
                    }),
    list_passengers=extend_schema(summary='Get all passenger for the flight', 
                    request=GetMultipleItemsQuerySerializer,
                    responses={
                        status.HTTP_200_OK: PassengerListSerializer,
                    }),
)
class FlightsViewSet(ViewSet):
    flight_service = FlightServiceFactory.create_flight()
    ticket_service = TicketServiceFactory.create_ticket()
    passenger_service = PassengerServiceFactory.create_passenger()

    def list(self, request):
        query_ser = GetMultipleItemsQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(query_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        flights = self.flight_service.get_all_flights(**query_ser.data)
        return Response(FlightsSerializer(flights).data, status=status.HTTP_200_OK)
    
    
    def create(self, request):
        request_ser = NewFlightSerializer(data=request.data)
        if not request_ser.is_valid():
            return Response(request_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        flight = self.flight_service.create(request_ser.save())
        return Response(FlightDetailsSerializer(flight).data, status=status.HTTP_201_CREATED)
    

    def retrieve(self, _, id=None):
        flight = self.flight_service.get_flight_by_id(id)
        return Response(FlightDetailsSerializer(flight).data, status=status.HTTP_200_OK)


    @action(detail=True)
    def change_status(self, request, id):
        body_ser = NewChangeFlightStatusDTOSerializer(data=request.data)
        if not body_ser.is_valid():
            return Response(body_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        flight = self.flight_service.change_status(flight_id=id, **body_ser.data)
        return Response(FlightDetailsSerializer(flight).data, status=status.HTTP_200_OK)


    @action(detail=True)
    def create_ticket(self, request, id=None):
        body_ser = NewTicketSerializer(data=request.data)
        if not body_ser.is_valid():
            return Response(body_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        ticket = self.ticket_service.create(Ticket(**body_ser.data, flight_id=id))
        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)


    @action(detail=False)
    def list_tickets(self, request, id=None):
        query_ser = GetMultipleItemsQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(query_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        tickets = self.ticket_service.get_by_flight_id(id, **query_ser.data)
        return Response(TicketsListSerializer(TicketList(tickets)).data, status=status.HTTP_200_OK)
    

    @action(detail=False)
    def list_passengers(self, request, id=None):
        query_ser = GetMultipleItemsQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(query_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        operation_id = self.flight_service.list_passengers(id, **query_ser.data)
        return Response({'operation_id': operation_id})


@extend_schema_view(
    book=extend_schema(summary='Flights list', 
                    request=BookTicketDTOSerializer, auth=False, 
                    responses={
                        status.HTTP_200_OK: TicketSerializer,
                    }),
)
class TicketsViewSet(ViewSet):
    ticketsService = TicketServiceFactory.create_ticket()

    @action(detail=True)
    def book(self, request, id=None):
        body_ser = BookTicketDTOSerializer(data=request.data)
        if not body_ser.is_valid():
            return Response(body_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        ticket = self.ticketsService.book_ticket(id, UUID(body_ser.data["passenger_id"]))
        return Response(TicketSerializer(ticket).data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(summary='Passenger list', 
                    parameters=[GetMultipleItemsQuerySerializer], auth=False,
                    responses={
                        status.HTTP_200_OK: PassengerListSerializer,
                    }),
    create=extend_schema(summary='New passenger', 
                    request=NewPassengerSerializer,
                    responses={
                        status.HTTP_201_CREATED: PassengerSerializer,
                    }),
)
class PassengerViewSet(ViewSet):
    passenger_service = PassengerServiceFactory.create_passenger()

    def create(self, request):
        body_ser = NewPassengerSerializer(data=request.data)
        if not body_ser.is_valid():
            return Response(body_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        passenger = self.passenger_service.create(Passenger(**body_ser.data))
        return Response(PassengerSerializer(passenger).data, status=status.HTTP_201_CREATED)
    

    def list(self, request):
        query_ser = GetMultipleItemsQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(query_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        passengers = self.passenger_service.get_all(**query_ser.data)
        return Response(PassengerListSerializer(PassengerList(passengers)).data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(summary='Get information about operation',
                      responses=OperationSerializer, auth=False)
)
class OperationsViewSet(ViewSet):
    ops_service = OperationServiceFactory.create_operation()

    def get(self, _, id: UUID):
        try:
            operation = self.ops_service.get_operation(id)
            return Response(OperationSerializer(operation).data)
        except KeyError as e:
            raise NotFound(e)
        except ValueError as e:
            raise ValidationError(e)