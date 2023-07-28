from django.urls import path
from . import views 
from rest_framework.routers import DefaultRouter
from .views import ElevatorSystemViewSet, ElevatorViewSet

router = DefaultRouter()
router.register(r'elevator_system', ElevatorSystemViewSet, basename='elevatorsystem')
router.register(r'elevator', ElevatorViewSet, basename='elevator')

urlpatterns = [
    path('', views.home, name = 'home'),
]

urlpatterns += router.urls 
