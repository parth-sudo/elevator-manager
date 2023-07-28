Elevator Manager
=

## A backend project built to simulate an elevator system.

## Tech Stack – Python, Django, sqlite3
 

**Elevator Manager**

**A backend project built to simulate an elevator system.**

**Tech Stack – Python, Django, sqlite3**

**Table of Contents –**

-   Overview

-   Models

-   Serializers

-   Urls

-   Views.

-   Utils

**Overview**

This is a backend project built in Django which simulates the movement
of elevators, user requests to reach a floor and the elevator system.
Some of the api endpoint include initialize elevators, assign elevator,
move elevators etc.

\*\* Insert video here. \*\*

Project Structure – The project has one app, called ‘api’ and a starter
project called ‘Elevator Manager. ‘api’ includes all the business logic
for this app.  
Important files– Models.py, Serializers.py, urls.py, views.py, utils.py

**Models**

There are 3 model classes in the models.py file. Each model class maps
to some entity. The models are as follows:

**<u>Elevator</u>** - This model is used for creating elevator
instances. The schema for this is similar to the real-world elevator. It
has the following attributes and class functions:

-   id: An auto-generated primary key to uniquely identify each elevator
    instance.

-   position: A positive integer field representing the current
    position/floor of the elevator. It defaults to 0.

-   status: A choice field representing the status of the elevator,
    which can be 'available', 'busy', or 'not\_working'. It defaults to
    'available'.

-   is\_open: A boolean field representing whether the elevator door is
    open or closed. It defaults to False.

-   direction: A choice field representing the direction in which the
    elevator is moving, either 'up' or 'down'. It defaults to 'up'.

-   next\_destination: An integer field representing the next floor to
    which the elevator is heading. It defaults to -1, indicating no next
    destination set.

Class Functions:

1.  move(self, direction, floor): A method to update the direction and
    position of the elevator to the specified direction and floor.

2.  open(self): A method to open the elevator door if it is currently
    closed.

3.  close(self): A method to close the elevator door if it is currently
    open.

4.  change\_status(self, status): A method to change the status of the
    elevator to the specified status.

5.  assign\_next\_destination(self, floor): A method to set the next
    destination floor of the elevator to the specified floor.

**<u>ElevatorSystem</u>** - This model represents the elevator system
and its associated elevators. It has the following attribute:

-   elevators: A ManyToManyField to associate multiple Elevator
    instances with the ElevatorSystem.

Class Functions:

1.  create\_elevators(cls, num\_elevators): A class method to create
    num\_elevators Elevator instances and associate them with the
    ElevatorSystem instance. It returns the created ElevatorSystem.

2.  assign\_elevator\_to\_user(self, request\_floor): A method to assign
    the most optimal available elevator to handle a user request to the
    specified request\_floor.

3.  get\_status(self): A method to fetch the status of all elevators
    associated with the ElevatorSystem.

**<u>ElevatorRequest</u>** - This model is used to store user requests
to the elevator. It has the following attributes:

-   floor\_number: A positive integer field representing the floor
    number to which the user has requested the elevator.

-   timestamp: A DateTimeField representing the timestamp when the
    request was made. The default value is set to the current time in
    the current timezone.

-   elevator: A ForeignKey field linking the ElevatorRequest to the
    associated Elevator that has been assigned to handle the request. It
    allows for a many-to-one relationship.

This concludes the overview of the models and their functionalities.

**Serializers**

**<u>ElevatorSerializer</u>** - This serializer is used to
serialize/deserialize Elevator model instances. The fields that will be
included in the serialized representation are:

-   id: The primary key of the elevator instance.

-   position: The current position/floor of the elevator.

-   status: The status of the elevator, which can be 'available',
    'busy', or 'not\_working'.

-   is\_open: A boolean field representing whether the elevator door is
    open or closed.

-   direction: The direction in which the elevator is moving, either
    'up' or 'down'.

-   next\_destination: The next destination floor of the elevator.

**<u>ElevatorSystemSerializer</u>** - This serializer is used to
serialize the ElevatorSystem model instances. It includes a custom
method get\_elevators that fetches all elevators associated with the
ElevatorSystem and serializes them using the ElevatorSerializer. The
serialized representation includes the list of elevators associated with
the ElevatorSystem.

**<u>ElevatorRequestSerializer</u>** - This serializer is used to
serialize/deserialize ElevatorRequest model instances. The fields that
will be included in the serialized representation are:

-   floor\_number: The floor number to which the user has requested the
    elevator.

-   timestamp: The timestamp when the request was made.

-   elevator: The primary key of the associated Elevator instance
    (linked through a ForeignKey).

These serializer classes help in converting complex data into JSON
format, making it easy to render the data as API responses and handle
data coming in from API requests.

**URLs** - the urlpatterns will include the URLs generated by the router
for the ElevatorSystemViewSet and ElevatorViewSet. The router
automatically handles URL patterns for various actions defined in the
viewsets.

**Views  
**

This file includes two viewsets, ElevatorSystemViewSet and
ElevatorViewSet, each containing several action methods that handle
different API endpoints.

**<u>ElevatorSystemViewSet</u>:**

-   initialize\_elevators: Initializes a specified number of elevators
    and returns a success message along with the serialized elevator
    system.

-   get\_elevator\_system: Retrieves the elevator system details,
    assuming there is only one elevator system.

-   assign\_elevator: Assigns an available elevator to a user request
    for a specific floor. Creates a new ElevatorRequest object to store
    the request details and returns the serialized assigned elevator.

-   get\_elevator\_requests: Retrieves all elevator requests or requests
    for a specific elevator (if provided), and returns the serialized
    data.

**<u>ElevatorViewSet:</u>**

-   get\_elevator\_details: Retrieves details of a specific elevator
    based on the provided elevator ID and returns the serialized data.

-   move\_elevators: Simulates elevator actions for elevators with
    assigned next destinations. It moves elevators to their next
    destinations and updates their status. Returns the serialized data
    for the affected elevators.

-   get\_elevator\_direction: Retrieves the direction of a specific
    elevator based on the provided elevator ID and returns the
    serialized data.

-   get\_next\_destination: Retrieves the next destination floor for a
    specific elevator based on the provided elevator ID and returns the
    serialized data.

-   change\_elevator\_status: Changes the status of a specific elevator
    based on the provided elevator ID and the desired status. Returns
    the serialized data for the updated elevator.

-   handle\_door: Opens or closes the door of a specific elevator based
    on the provided elevator ID and the user query. Returns the
    serialized data for the updated elevator.

**Utils**

-   get\_elevator\_instance(request): This utility function takes a
    request as input and retrieves an Elevator instance based on the
    provided id parameter in the request's query parameters. If no id is
    provided or the provided id does not match any Elevator instance, it
    returns a 404 response using the get\_object\_or\_404 function. If a
    valid id is provided, it returns the corresponding Elevator
    instance.









