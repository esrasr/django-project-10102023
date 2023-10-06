from django.contrib import admin
from django.contrib import admin
from apps.election.models import City, Country, Candidates, Election


class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "deleted"]


class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "deleted"]
    ordering = ["country", "name"]


class CandidatesAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "party", "deleted"]

class ElectionAdmin(admin.ModelAdmin):
    list_display = ["id", "candidate", "city", "count", "deleted"]
    ordering = ["candidate", "city"]


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Candidates, CandidatesAdmin)
admin.site.register(Election, ElectionAdmin)