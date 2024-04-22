from rest_framework import serializers
from .models import Flight, SeatTypes, Ticket, FlightStates, CreateTicketDTO, Gender, BookTicketDTO, ChangeFlightStatusDTO, Passenger, PassengerList
from rest_enumfield import EnumField


class TicketSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    seat_type = EnumField(choices=SeatTypes)
    flight_id = serializers.UUIDField()
    seat_position = serializers.CharField()
    cost = serializers.IntegerField()
    available = serializers.BooleanField()
    passenger_id = serializers.UUIDField()


class TicketsListSerializer(serializers.Serializer):
    tickets = TicketSerializer(many=True)


class GetTicketsQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    seat_type = EnumField(choices=SeatTypes, required=False)


class NewTicketSerializer(serializers.Serializer):
    seat_type = EnumField(choices=SeatTypes)
    seat_position = serializers.CharField()
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


class NewChangeFlightStatusDTOSerializer(serializers.Serializer):
    status = EnumField(choices=FlightStates)
    departure_time = serializers.DateTimeField(required=False, default=None)
    arrival_time = serializers.DateTimeField(required=False, default=None)
    
    def create(self, validated_data):
        return ChangeFlightStatusDTO(**validated_data)


class FlightsSerializer(serializers.Serializer):
    flights = FlightDetailsSerializer(many=True)


class NewFlightSerializer(serializers.Serializer):
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()
    departure_point = serializers.CharField()
    destination_point = serializers.CharField()
    
    def create(self, validated_data):
        return Flight(**validated_data)


class GetMultipleItemsQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(min_value=10, max_value=50, default=20, required=False)
    offset = serializers.IntegerField(min_value=0, default=0, required=False)


class PassengerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    birthday = serializers.DateTimeField()
    gender = EnumField(choices=Gender)


class NewPassengerSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    birthday = serializers.DateTimeField()
    gender = EnumField(choices=Gender)

    def create(self, validated_data):
        return Passenger(**validated_data)


class PassengerListSerializer(serializers.Serializer):
    passengers = PassengerSerializer(many=True)


OPERATION_RESULTS_SERIALIZERS_MAP = {
    type(PassengerList(None)): PassengerListSerializer
}


class OperationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    done = serializers.BooleanField()
    result = serializers.SerializerMethodField(default={})

    def get_result(self, obj):
        serializer_class = OPERATION_RESULTS_SERIALIZERS_MAP[type(obj.result)]
        result = serializer_class(obj.result)
        return result.data