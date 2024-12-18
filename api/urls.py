from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_gravitational_force_problem),

]