from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Elevator, ElevatorSystem, ElevatorRequest
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializers import ElevatorSystemSerializer, ElevatorSerializer, ElevatorRequestSerializer
from rest_framework import viewsets
from .utils import get_elevator_instance
from django.utils import timezone


#viewset for elevator system. It has several action methods serving as api endpoints.
class ElevatorSystemViewSet(viewsets.ViewSet):

    #initializes an elevator system with N elevators in it.
    @action(detail=False, methods=['get'])
    def initialize_elevators(self, request):
        num_elevators = int(request.GET.get('num_elevators', 2))
        if num_elevators <= 0:
            return Response({'error': 'Invalid number of elevators. Must be greater than 0.'}, status=400)

        elevator_system = ElevatorSystem.create_elevators(num_elevators) #class method
        serializer = ElevatorSystemSerializer(elevator_system)
        return Response({'message': f'{num_elevators} elevators initialized successfully.', 'data': serializer.data})

    #fetches details of all elevators.    
    @action(detail=False, methods=['get'])
    def get_elevator_system(self, request):
        try:
            # for simplicity, we assume there is only one Elevator System.
            elevator_system = ElevatorSystem.objects.first()
        except ElevatorSystem.DoesNotExist:
            return Response({"Elevator System not found"}, status=404)

        serializer = ElevatorSystemSerializer(elevator_system)
        return Response(serializer.data)
    
    #assign elevator the floor in the most optimal way.
    @action(detail=False, methods=['get'])
    def assign_elevator(self, request):
        floor = int(request.GET.get('floor', -1))
        try:
            floor = int(floor)
        except ValueError:
            return Response({"error": "Invalid floor number"}, status=400)
        
        if floor < 0:
            return Response({"error": "Invalid floor number"}, status=400)
        
        try:
            # for simplicity, we assume there is only one Elevator System.
            elevator_system = ElevatorSystem.objects.first()
        except ElevatorSystem.DoesNotExist:
            return Response({"Elevator System not found"}, status=404)
        
        assigned_elevator = elevator_system.assign_elevator_to_user(floor)
        if not assigned_elevator:
            return Response({"error": "No available elevators to handle the request"}, status=404)

        assigned_elevator.assign_next_destination(floor)
        assigned_elevator.save()
        # creating user requests made for a specific elevator
        elevator_request = ElevatorRequest.objects.create(floor_number=floor, elevator=assigned_elevator)
        elevator_request.save()      
        serializer = ElevatorSerializer(assigned_elevator)
        return Response({'message' : f"Elevator with id {assigned_elevator.id} assigned to floor number {floor}", 'data' : serializer.data})

    #get all the user elevator requests.
    @action(detail=False, methods=['get'])
    def get_elevator_requests(self, request):
        id = int(request.GET.get('id', -1))
        if id == -1:
            user_requests = ElevatorRequest.objects.all()
        else:
            user_requests = ElevatorRequest.objects.filter(elevator=id)
            if not user_requests:
                return Response({'message' : 'Invalid request'}, status = 400)
        
        serializer_data = []
        for user_request in user_requests:
            serializer = ElevatorRequestSerializer(user_request)
            serializer_data.append(serializer.data)

        return Response(serializer_data)


#viewset for elevator. It has several action methods serving as api endpoints.
class ElevatorViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def get_elevator_details(self, request):
        elevator = get_elevator_instance(request) #utility function
        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data)
    
    #move assigned elevators to their next destination.
    @action(detail=False, methods=['get'])
    def move_elevators(self, request):
        try:
            # for simplicity, we assume there is only one Elevator System.
            elevator_system = ElevatorSystem.objects.first()
        except ElevatorSystem.DoesNotExist:
            return Response({"Elevator System not found"}, status=404)
        
        elevators = elevator_system.elevators.exclude(next_destination=-1)
        if len(elevators) == 0:
            return Response("No Elevator assigned to a floor.")  
        serializer_data = []

        for elevator in elevators:

            # Simulating elevator actions.
            floor = elevator.next_destination
            elevator.close()
            elevator.change_status('busy')
            elevator.move('up' if elevator.position < floor else 'down', floor)
            elevator.change_status('available')  # Changes are reflected immediately
            elevator.open()

            elevator.assign_next_destination(-1)  # This signifies no next destination.
            elevator.save()

            serializer = ElevatorSerializer(elevator)
            serializer_data.append(serializer.data)

        return Response(serializer_data)

    #get direction (up or down)
    @action(detail=False, methods=['get'])
    def get_elevator_direction(self, request):
        elevator = get_elevator_instance(request)
        serializer = ElevatorSerializer(elevator)
        message = f"Elevator with id {elevator.id} is going {serializer.data['direction']}"
        return Response({'message' : message, 'data' : serializer.data})
    

    @action(detail=False, methods=['get'])
    def get_next_destination(self, request):
        elevator = get_elevator_instance(request)
        serializer = ElevatorSerializer(elevator)
        if serializer.data['next_destination'] == -1:
            message = "No Next Destination for this elevator."
        else:
            message = f"Next destination for elevator with id = {elevator.id} is floor {serializer.data['next_destination']}"
        return Response({'message' : message, 'data' : serializer.data})


    @action(detail=False, methods=['get'])
    def change_elevator_status(self, request):
        elevator = get_elevator_instance(request)
        status = str(request.GET.get('status', "available"))
        status_arr = ['available', 'busy', 'not working', 'not_working', 'Not working']
        if status not in status_arr:
            return Response({"Invalid request"}, status=400)
        
        elevator.status = status
        elevator.save()
        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data)
    
    #open or close the door.
    @action(detail=False, methods=['get'])
    def handle_door(self, request):
        elevator = get_elevator_instance(request) 
        query = str(request.GET.get('query', 'open'))
        if query != 'open' and query != 'close':
            return Response({'Invalid Request'}, status = 400)
        
        if query == 'open':
            elevator.open()
        elif query == 'close':
            elevator.close()
        elevator.save()

        bool_dict = {'close' : 'Closed', 'open' : 'Opened'}
        serializer = ElevatorSerializer(elevator)
        message = f"Elevator with id {elevator.id} has been {bool_dict[query]}"
        return Response({'message' : message, 'data' : serializer.data})

