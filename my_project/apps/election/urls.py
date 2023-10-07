from django.urls import path
from apps.election.views import index, get_city_ajax, get_city_chart_ajax, get_chart_ajax, election_details, pie_chart


app_name = "election"


urlpatterns = [
    path("homepage", index, name="homepage"),
    path("", index, name="homepage"),
    path("get-city-ajax/", get_city_ajax, name="get_city_ajax"),
    path("get-chart-ajax/", get_chart_ajax, name="get_chart_ajax"),
    path("get-city-chart-ajax/", get_city_chart_ajax, name="get_city_chart_ajax"),
    path("election-details/<int:city_id>", election_details, name="election_details"),
    path("charts/", pie_chart, name="charts"),
]
