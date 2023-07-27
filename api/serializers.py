from rest_framework import serializers
from .models import Elevator, ElevatorSystem

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = ['id', 'position', 'status', 'is_open', 'direction', 'next_destination']

class ElevatorSystemSerializer(serializers.Serializer):
    elevators = serializers.SerializerMethodField()

    def get_elevators(self, obj):
        elevators = obj.elevators.all()
        elevator_serializer = ElevatorSerializer(elevators, many=True)
        return elevator_serializer.data