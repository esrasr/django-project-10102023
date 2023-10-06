from django.shortcuts import render
from django.http.response import HttpResponse
from apps.election.models import City, Country, Candidates, Election
from django.http import JsonResponse
import matplotlib
from django.db.models import (
    Sum,
    Count,
    Value,
    F,
    ExpressionWrapper,
    FloatField,
    DecimalField,
    IntegerField,
    Expression,
    Max,
)


def index(request):
    context = {
        "country": Country.objects.filter(deleted=0).all(),
        "candidates": Candidates.objects.filter(deleted=0).all(),
    }
    return render(request, "select.html", context)


def get_city_ajax(request):
    if request.method == "POST":
        instance_id = request.POST.get("instanceID")
        city = City.objects.filter(country_id=instance_id, deleted=0)
        # serialize data:
        return JsonResponse(list(city.values("id", "name")), safe=False)


def election_details(request, city_id):
    instance = Election.objects.filter(deleted=0, city_id=city_id)
    total_count = instance.aggregate(total_count=Sum("count"))["total_count"]
    print("total_count", total_count)
    election_group = (
        instance.select_related("candidate")
        .values("candidate")
        .annotate(
            candidate_total_count=Sum("count"),
            total_count=Value(total_count),
            percent=ExpressionWrapper(
                (F("candidate_total_count") * 100) / F("total_count"),
                output_field=IntegerField(),
            ),
        )
        .order_by("-percent")
        .values(
            "candidate__name",
            "candidate__party",
            "candidate",
            "candidate_total_count",
            "total_count",
            "percent",
        )
    )
    context = {"total_count": total_count, "election_group": election_group}
    return render(request, "detail.html", context)
