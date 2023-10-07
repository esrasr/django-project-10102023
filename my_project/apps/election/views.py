from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from apps.election.models import City, Country, Candidates, Election
from django.http import JsonResponse
from django.contrib import messages
from apps.election.utils import get_pie_chart
from django.template.loader import render_to_string


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
        return JsonResponse(list(city.values("id", "name")), safe=False)


def get_chart_ajax(request):
    if request.method == "POST":
        country_id = request.POST.get("instanceID")
        total_count = Election.objects.country_total_count(country_id=country_id)
        if total_count == 0:
            return JsonResponse({"template_content": ""})
        election_group = Election.objects.get_country_percent(country_id=country_id, total_count=total_count)
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
        total_count = Election.objects.city_total_count(city_id=city_id)
        if total_count == 0:
            return JsonResponse({"template_content": ""})

        election_group = Election.objects.get_city_percent(city_id=city_id, total_count=total_count)
        labels = []
        sizes = []
        for item in election_group:
            labels.append(item["candidate__name"])
            sizes.append(item["percent"])
        image = get_pie_chart(labels, sizes)
        template_content = render_to_string("pie_chart.html", {"img_base64": image, "winner_name": election_group[0], "result": election_group[1:]})

        return JsonResponse({"template_content": template_content})


def election_details(request, city_id):
    total_count = Election.objects.city_total_count(city_id=city_id)
    if total_count == 0:
        messages.error(request, "This city does not exist.")
        return HttpResponseRedirect(reverse("election:homepage"))
    election_group = Election.objects.get_city_percent(city_id=city_id, total_count=total_count)
    context = {"total_count": total_count, "election_group": election_group}
    return render(request, "detail.html", context)


def pie_chart(request):
    total_count = Election.objects.country_total_count(country_id=4)

    election_group = Election.objects.get_country_percent(country_id=4, total_count=total_count)
    labels = []
    sizes = []
    for item in election_group:
        labels.append(item["candidate__name"])
        sizes.append(item["percent"])

    image = get_pie_chart(labels, sizes)

    context = {"total_count": total_count, "election_group": election_group, "graphic": image}
    return render(request, "charts.html", context)
