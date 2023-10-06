from django.urls import path
from apps.election.views import index, get_city_ajax, election_details


app_name = "election"


urlpatterns = [
    path("homepage", index),
    path("", index),
    path("get-city-ajax/", get_city_ajax, name="get_city_ajax"),
    path("election-details/<int:city_id>", election_details, name="election_details"),
]
