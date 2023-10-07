from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from apps.election.models import City, Country, Candidates, Election
from django.http import JsonResponse
from django.contrib import messages
from apps.election.utils import get_pie_chart
from django.template.loader import render_to_string
from django.db.models import Sum, Count, F


def index(request):
    date = request.GET.get("date")
    date_list = list(map(str, list(Election.objects.distinct("date").order_by("date").values_list("date", flat=True))))
    if not date:
        date = date_list[-1]
    context = {"country": Country.objects.filter(deleted=0).all(), "candidates": Candidates.objects.filter(deleted=0, date=date).all(), "date_list": date_list, "date": date}
    return render(request, "select.html", context)


def get_city_ajax(request):
    if request.method == "POST":
        instance_id = request.POST.get("instanceID")
        city = City.objects.filter(country_id=instance_id, deleted=0)
        return JsonResponse(list(city.values("id", "name")), safe=False)


def get_chart_ajax(request):
    if request.method == "POST":
        date = request.POST.get("date")
        country_id = request.POST.get("instanceID")
        total_count = Election.objects.country_total_count(country_id=country_id, date=date)
        if total_count == 0:
            return JsonResponse({"template_content": ""})
        election_group = Election.objects.get_country_percent(country_id=country_id, total_count=total_count, date=date)
        labels = []
        sizes = []
        for item in election_group:
            labels.append(item["candidate__name"])
            sizes.append(item["percent"])

        image = get_pie_chart(labels, sizes)
        template_content = render_to_string("pie_chart.html", {"img_base64": image, "winner_name": election_group[0], "result": election_group[1:]})

        return JsonResponse({"template_content": template_content})


def get_city_chart_ajax(request):
    if request.method == "POST":
        city_id = request.POST.get("instanceID")
        date = request.POST.get("date")
        total_count = Election.objects.city_total_count(city_id=city_id, date=date)
        if total_count == 0:
            return JsonResponse({"template_content": ""})

        election_group = Election.objects.get_city_percent(city_id=city_id, total_count=total_count, date=date)
        labels = []
        sizes = []
        for item in election_group:
            labels.append(item["candidate__name"])
            sizes.append(item["percent"])
        image = get_pie_chart(labels, sizes)
        template_content = render_to_string("pie_chart.html", {"img_base64": image, "winner_name": election_group[0], "result": election_group[1:]})

        return JsonResponse({"template_content": template_content})


def election_table(request):
    date = request.GET.get("date")
    election_detail = (
        Election.objects.filter(date=date)
        .select_related("city__country")
        .values("city")
        .annotate(
            candidate_total_count=Sum("count"),
            candidate_count=Count("candidate_id"),
            country_name=F("city__country__name"),
            city_name=F("city__name"),
        )
        .order_by("country_name", "city_name")
        .values("country_name", "city_name", "candidate_total_count", "candidate_count", "city_id", "date")
    )
    context = {"election_detail": election_detail, "date": date}
    return render(request, "election_table.html", context)


def election_details(request, city_id):
    date = request.GET.get("date")
    total_count = Election.objects.city_total_count(city_id=city_id, date=date)
    if total_count == 0:
        return JsonResponse({"template_content": ""})

    election_group = Election.objects.get_city_percent(city_id=city_id, total_count=total_count, date=date)
    labels = []
    sizes = []
    for item in election_group:
        labels.append(item["candidate__name"])
        sizes.append(item["percent"])
    image = get_pie_chart(labels, sizes)
    instance = Election.objects.filter(city_id=city_id).order_by("-count").all()[:10]
    context = {"total_count": total_count, "election_group": election_group, "img_base64": image, "winner_name": election_group[0], "result": election_group[1:], "table": instance}
    return render(request, "detail.html", context)
