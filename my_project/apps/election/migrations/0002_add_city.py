# Generated by Django 4.2.5 on 2023-10-01 09:24

from django.db import migrations
import json
import os


def load_country_and_city(apps, schema_editor):
    fixture_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../fixtures/initial_data.json")
    )
    Country = apps.get_model("election", "Country")
    City = apps.get_model("election", "City")
    with open(fixture_dir, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for country in data["countries"]:
            country_obj, created = Country.objects.get_or_create(name=country["name"])
            for city in country["cities"]:
                City.objects.get_or_create(country=country_obj, name=city)


class Migration(migrations.Migration):
    dependencies = [
        ("election", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_country_and_city)]
