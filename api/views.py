from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Elevator, ElevatorSystem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ElevatorSystemSerializer, ElevatorSerializer

# Create your views here.
def initialize_elevators(request):
    num_elevators = int(request.GET.get('num_elevators', 2))  # Get the number of elevators from the request parameter (default to 1 if not provided)

    if num_elevators <= 0:
        return JsonResponse({'error': 'Invalid number of elevators. Must be greater than 0.'}, status=400)

    elevator_system = ElevatorSystem.create_elevators(num_elevators)
    return JsonResponse({'message': f'{num_elevators} elevators initialized successfully.'})


@api_view(['GET'])
def get_elevator_system(request):
    try:
        elevator_system = ElevatorSystem.objects.get(pk = 1)
    except ElevatorSystem.DoesNotExist:
        return Response({"System not found"}, status=404)
    
    serializer = ElevatorSystemSerializer(elevator_system)
    return Response(serializer.data)
    
@api_view(['GET'])
def assign_elevator(request):
    floor = int(request.GET.get('floor'))

    try:
        floor = int(floor)
    except ValueError:
        return Response({"error": "Invalid floor number"}, status=400)
    
    if floor < 0:
        return Response({"error": "Invalid floor floor number"}, status=400)

    elevator_system = ElevatorSystem.objects.first()
    assigned_elevator = elevator_system.assign_elevator_to_user(floor)
    if not assigned_elevator:
        return Response({"error": "No available elevators to handle the request"}, status=404)

    assign_elevator.close()
    assign_elevator.change_status('busy')
    assign_elevator.move('up' if assigned_elevator.position < floor else 'down')
    # this is because the elevator reflects the changes immediately (i.e no time gap in changing floors)
    assign_elevator.change_status('available')
    assign_elevator.open()

    serializer = ElevatorSerializer(assigned_elevator)
    
    return Response(serializer.data)
    



def home(request):
    return HttpResponse("Home")