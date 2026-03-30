from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Candidate Management (Host)
    path('election/<int:election_id>/candidates/', views.add_candidate, name='add_candidate'),
    path('candidate/delete/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),

    # 🔹 Voting (Voter)
    path('elections/', views.voter_elections, name='voter_elections'),
    path('vote/<int:election_id>/', views.vote, name='vote'),

    # 🔹 Results
    path('results/<int:election_id>/', views.election_results, name='election_results'),

]