from rest_framework import serializers
from .models import Elevator, ElevatorSystem, ElevatorRequest

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
    
class ElevatorRequestSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = ElevatorRequest
        fields = ['id', 'floor_number', 'timestamp', 'elevator'] 