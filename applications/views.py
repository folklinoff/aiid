from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from applications.factory import FlightServiceFactory
from applications.serializers import GetFlightsQuerySerializer, FlightsSerializer, NewFlightSerializer, FlightDetailsSerializer

class FlightsViewSet(ViewSet):
    flightService = FlightServiceFactory.create_flight()

    def list(self, request):
        query_ser = GetFlightsQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(query_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        flights = self.flightService.get_all_flights(query_ser.validated_data['offset'], query_ser.validated_data['limit'])
        return Response(FlightsSerializer(flights).data)
    
    def create(self, request_ser):
        request_ser = NewFlightSerializer(data=request_ser.data)
        if not request_ser.is_valid():
            return Response(request_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        flight = self.flightService.create(request_ser.save())
        return Response(FlightDetailsSerializer(flight).data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, _, id=None):
        flight = self.flightService.get_flight(id)
        return Response(FlightDetailsSerializer(flight).data, status=status.HTTP_200_OK)

    def update(self, request, id=None):
        body_ser = NewFlightSerializer(data=request.data)
        if not body_ser.is_valid():
            return Response(body_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        flight = self.flightService.update(body_ser.save())
        return Response(FlightDetailsSerializer(flight).data, status=status.HTTP_200_OK)