from django.urls import path
from apps.election.views import index

urlpatterns = [path("homepage", index), path("", index)]
