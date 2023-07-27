from django.db import models
from django.db.models import F
from django.db.models.functions import Abs
# Create your models here.
status_choices = [('available', 'available'), ('busy', 'busy')]
direction_choices = [('up', 'up'), ('down', 'down')]

class Elevator(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.PositiveIntegerField(verbose_name="position", default = 0)
    status = models.CharField(max_length=10, choices = status_choices, default='available')
    open = models.BooleanField(default=False)
    direction = models.CharField(max_length=4, choices = direction_choices, default = 'up')

    def __str__(self):
        return self.id
    
    def move(self, direction):
        if direction == 'up':
            self.position += 1
        elif direction == 'down':
            self.position = self.position - 1 if self.position > 0 else self.position
        
        self.direction = direction

        
class ElevatorSystem(models.Model):
    elevators = models.ManyToManyField(Elevator, related_name='elevators')
    
    @classmethod
    def create_elevators(cls, num_elevators):
        # Create N elevator instances and associate them with the ElevatorSystem instance
        elevator_system = cls.objects.create()
        elevators = [Elevator() for _ in range(num_elevators)]
        Elevator.objects.bulk_create(elevators)
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
