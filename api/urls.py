from django.urls import path
from . import views 
from rest_framework.routers import DefaultRouter
from .views import ElevatorSystemViewSet, ElevatorViewSet

router = DefaultRouter()
router.register(r'elevatorsystem', ElevatorSystemViewSet, basename='elevatorsystem')
router.register(r'elevator', ElevatorViewSet, basename='elevator')


urlpatterns = [
    path('', views.home, name = 'home'),
    # path('initialize/', views.initialize_elevators, name = 'initialize_elevators'),
    # path('get_elevator_system/', views.get_elevator_system, name = 'get_elevator_system'),
    # path('assign_elevator/', views.assign_elevator, name='assign_elevator'),
    # path('get_elevator_direction/', views.get_elevator_direction),
    # path('change_elevator_status/', views.change_elevator_status)
]

urlpatterns += router.urls 
