from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name = 'home'),
    path('initialize/', views.initialize_elevators, name = 'initialize_elevators'),
    path('get_elevator_system/', views.get_elevator_system, name = 'get_elevator_system'),
    path('assign_elevator/', views.assign_elevator, name='assign_elevator')
]
