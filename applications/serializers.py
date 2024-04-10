from rest_framework import serializers
from .models import Flight, SeatTypes, Ticket, FlightStates, CreateTicketDTO, Gender, BookTicketDTO
from rest_enumfield import EnumField


class TicketSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    seat_type = EnumField(choices=SeatTypes)
    flight_id = serializers.UUIDField()
    seat_position = serializers.StringRelatedField()
    cost = serializers.IntegerField()
    available = serializers.BooleanField()
    passenger_id = serializers.UUIDField()


class TicketsListSerializer(serializers.Serializer):
    tickets = TicketSerializer()


class GetTicketsQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    seat_type = EnumField(choices=SeatTypes, required=False)


class NewTicketSerializer(serializers.Serializer):
    seat_type = EnumField(choices=SeatTypes)
    seat_position = serializers.StringRelatedField()
    cost = serializers.IntegerField()

    def create(self, validated_data):
        return CreateTicketDTO(**validated_data)


class BookTicketDTOSerializer(serializers.Serializer):
    passenger_id = serializers.UUIDField()

    def create(self, validated_data):
        return BookTicketDTO(**validated_data)


class FlightSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    status = EnumField(choices=FlightStates)
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()
    tickets = TicketSerializer(many=True, required=False)
    departure_point = serializers.CharField()
    destination_point = serializers.CharField()


class FlightDetailsSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = EnumField(choices=FlightStates)
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()
    departure_point = serializers.CharField()
    destination_point = serializers.CharField()


class FlightsSerializer(serializers.Serializer):
    flights = FlightDetailsSerializer(many=True)


class NewFlightSerializer(serializers.Serializer):
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()
    departure_point = serializers.CharField()
    destination_point = serializers.CharField()
    
    def create(self, validated_data):
        return Flight(**validated_data)


class GetFlightsQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(min_value=10, max_value=50, default=20, required=False)
    offset = serializers.IntegerField(min_value=0, default=0, required=False)


class PassengerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.StringRelatedField()
    middle_name = serializers.StringRelatedField()
    last_name = serializers.StringRelatedField()
    birthday = serializers.DateTimeField()
    gender = EnumField(choices=Gender)


class NewPassengerSerializer(serializers.Serializer):
    first_name = serializers.StringRelatedField()
    middle_name = serializers.StringRelatedField()
    last_name = serializers.StringRelatedField()
    birthday = serializers.DateTimeField()
    gender = EnumField(choices=Gender)

    def create(self, validated_data):
        return CreateTicketDTO(**validated_data)


class PassengerListSerializer(serializers.Serializer):
    passengers = PassengerSerializer(many=True)