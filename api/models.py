from django.db import models
from django.db.models import F
from django.db.models.functions import Abs
from django.utils import timezone

status_choices = [('available', 'available'), ('busy', 'busy'), ('not_working', 'not_working')]
direction_choices = [('up', 'up'), ('down', 'down')]

class Elevator(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.PositiveIntegerField(verbose_name="position", default = 0)
    status = models.CharField(max_length=20, choices = status_choices, default='available')
    is_open = models.BooleanField(default=False)
    direction = models.CharField(max_length=4, choices = direction_choices, default = 'up')
    next_destination = models.IntegerField(verbose_name="next", default=-1)

    def __str__(self):
        return f"Elevator {self.id} - Position: {self.position}"
    
    def move(self, direction, floor):
        self.direction = direction
        self.position = floor
    
    def open(self):
        if not self.is_open:
            self.is_open = True

    def close(self):
        if self.is_open:
            self.is_open = False

    def change_status(self, status):
        self.status = status

    def assign_next_destination(self, floor):
        self.next_destination = floor

        
class ElevatorSystem(models.Model):
    elevators = models.ManyToManyField(Elevator, related_name='elevators')
    
    @classmethod
    def create_elevators(cls, num_elevators):
        # Create N elevator instances and associate them with the ElevatorSystem instance
        elevator_system = cls.objects.create()
        elevators = []
        for _ in range(num_elevators):
            obj = Elevator.objects.create()
            obj.save()
            elevators.append(obj)
        elevator_system.elevators.set(elevators)
        return elevator_system

    def assign_elevator_to_user(self, request_floor):
        available_elevators = self.elevators.filter(status='available')
        if not available_elevators:
            return None
        
        # Get the closest elevator to the requested floor (regardless of direction)
        closest_elevator = available_elevators.annotate(
            distance_to_floor=Abs(F('position') - request_floor)
        ).order_by('distance_to_floor', 'id').first()

        if closest_elevator is None:
            return None

        return closest_elevator
    
    def get_status(self):
        status_report = []
        elevators = self.elevators.all()
        for elevator in elevators:
            obj = {'id': elevator.id, 'current_floor': elevator.position, 'status' : elevator.status}
            status_report.append(obj)

        return status_report


#a model for storing user requests to the elevator.
class ElevatorRequest(models.Model):
    floor_number = models.PositiveIntegerField(verbose_name="Floor Number")
    timestamp = models.DateTimeField(default=timezone.now)
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name='requests', null=True, blank=True)

    def __str__(self):
        return f"Request for Elevator: {self.elevator} - Floor Number: {self.floor_number}"
