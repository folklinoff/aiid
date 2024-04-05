from rest_framework import serializers
from .models import Flight, SeatTypes, Ticket, FlightStates
from rest_enumfield import EnumField

class TicketSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    seat_type = EnumField(choices=SeatTypes, required=False)


class GetTicketsQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    seat_type = EnumField(choices=SeatTypes, required=False)

    def create(self, validated_data):
        return Ticket(validated_data['id'], validated_data['seat_type'])


class FlightSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    status = EnumField(choices=FlightStates)
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()
    # tickets = TicketSerializer(many=True, required=False)


class FlightDetailsSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = EnumField(choices=FlightStates)
    
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()


class FlightsSerializer(serializers.Serializer):
    flights = FlightDetailsSerializer(many=True)


class NewFlightSerializer(serializers.Serializer):
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()
    
    def create(self, validated_data):
        return Flight(
            validated_data['departure_time'], 
            validated_data['arrival_time']
        )

class GetFlightsQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(min_value=10, max_value=50, default=20, required=False)
    offset = serializers.IntegerField(min_value=0, default=0, required=False)