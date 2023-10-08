from django.contrib import admin
from django.urls import path, include
from apps.election.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.election.urls", namespace='election')),
]
