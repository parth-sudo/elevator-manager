from rest_framework.response import Response
from .models import Elevator, ElevatorSystem
from django.shortcuts import get_object_or_404
import random

#fetch elevator instance given its id in the params.
def get_elevator_instance(request):
        id = int(request.GET.get('id', -1))
        return get_object_or_404(Elevator, pk=id)
        
                