from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_election, name='create_election'),
    path('my/', views.my_elections, name='my_elections'),
    path('edit/<int:election_id>/', views.edit_election, name='edit_election'),
]
