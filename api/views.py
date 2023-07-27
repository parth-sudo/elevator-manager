from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Elevator, ElevatorSystem
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializers import ElevatorSystemSerializer, ElevatorSerializer
import random
from rest_framework import viewsets
from rest_framework import status


# Create your views here.
class ElevatorSystemViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def initialize_elevators(self, request):
        num_elevators = int(request.GET.get('num_elevators', 2))

        if num_elevators <= 0:
            return Response({'error': 'Invalid number of elevators. Must be greater than 0.'}, status=400)

        elevator_system = ElevatorSystem.create_elevators(num_elevators)
        serializer = ElevatorSystemSerializer(elevator_system)
        return Response({'message': f'{num_elevators} elevators initialized successfully.', 'data': serializer.data})
        
    @action(detail=False, methods=['get'])
    def get_elevator_system(self, request):
        system_id = int(request.GET.get('id', -1))
        try:
            if system_id == -1:
                elevator_system = ElevatorSystem.objects.first()
            else:
                elevator_system = ElevatorSystem.objects.get(id=system_id)
        except ElevatorSystem.DoesNotExist:
            return Response({"Elevator System not found"}, status=404)

        serializer = ElevatorSystemSerializer(elevator_system)
        return Response(serializer.data)


class ElevatorViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def assign_elevator(self, request):
        floor = int(request.GET.get('floor', -1))

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

        #simulating elevator actions.
        assigned_elevator.assign_next_destination(floor)
        assigned_elevator.close()
        assigned_elevator.change_status('busy')
        assigned_elevator.move('up' if assigned_elevator.position < floor else 'down', floor)
        assigned_elevator.change_status('available') # this is because the changes are reflected immediately
        assigned_elevator.open()

        assigned_elevator.save()

        serializer = ElevatorSerializer(assigned_elevator)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_elevator_direction(self, request):
        id = int(request.GET.get('id', -1))
        if id == -1:
            return Response({"Elevator not found"}, status=404)

        try:
            elevator = Elevator.objects.get(id=id)
        except Elevator.DoesNotExist:
            return Response({f"Elevator with id = {id} not found"}, status=404)

        serializer = ElevatorSerializer(elevator)
        message = f"Elevator with id {id} is going {serializer.data['direction']}"
        return Response(message)
    
    @action(detail=False, methods=['get'])
    def get_next_destination(self, request):
        id = int(request.GET.get('id', -1))
        if id == -1:
            return Response({"Elevator not found"}, status=404)
        
        try:
            elevator = Elevator.objects.get(id=id)
        except Elevator.DoesNotExist:
            return Response({f"Elevator with id = {id} not found"}, status=404)
        
        serializer = ElevatorSerializer(elevator)
        message = f"Elevator with id {id} is going {serializer.data['next_destination']}"
        return Response(message)

    @action(detail=False, methods=['get'])
    def change_elevator_status(self, request):
        id = int(request.GET.get('id', -1))
        status = str(request.GET.get('status', "available"))
        status_arr = ['available', 'busy', 'under_maintainance']
        if id == -1:
            return Response({"Elevator not found"}, status=404)
        elif status not in status_arr:
            return Response({"Invalid request"}, status=400)

        try:
            elevator = Elevator.objects.get(id=id)
        except Elevator.DoesNotExist:
            return Response({f"Elevator with id = {id} not found"}, status=404)

        elevator.status = status
        elevator.save()
        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def handle_door(self, request):
        id = int(request.GET.get('id', -1))
        query = str(request.GET.get('query', 'open'))
        if id == -1:
            return Response({"Elevator not found"}, status=404)
        elif query != 'open' and query != 'close':
            return Response({'Invalid Request'}, status = 400)

        try:
            elevator = Elevator.objects.get(id=id)
        except Elevator.DoesNotExist:
            return Response({f"Elevator with id = {id} not found"}, status=404)
        
        if query == 'open':
            elevator.open()
        elif query == 'close':
            elevator.close()
        elevator.save()

        bool_dict = {'close' : 'Closed', 'open' : 'Opened'}
        serializer = ElevatorSerializer(elevator)
        message = f"Elevator with id {id} has been {bool_dict[query]}"
        return Response(message)



def home(request):
    return HttpResponse("Home")