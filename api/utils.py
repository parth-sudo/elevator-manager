from rest_framework.response import Response
from .models import Elevator, ElevatorSystem
from django.shortcuts import get_object_or_404
import random

def get_elevator_instance(request):
        id = int(request.GET.get('id', -1))
        return get_object_or_404(Elevator, pk=id)
        
def get_random_elevator_system():
        all_systems = ElevatorSystem.objects.all()
        random_index = random.randint(0, all_systems.count() - 1)
        elevator_system = all_systems[random_index]
        return elevator_system
                