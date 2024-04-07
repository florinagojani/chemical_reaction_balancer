from django.urls import path
from . import views

urlpatterns = [
    path('', views.reaction_balancer, name='reaction_balancer'),
    path('validate/', views.validate_reaction, name='validate_reaction'),
]






