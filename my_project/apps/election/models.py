from django.db import models
from apps.base.models import BaseModel
from django.db.models.functions import Coalesce


class Country(BaseModel):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)

    class Meta:
        db_table = "country"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class City(BaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = "city"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Candidates(BaseModel):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=20)
    date = models.DateField(default="2023-05-14")
    # image

    class Meta:
        db_table = "candidates"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ElectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=0)

    def country_total_count(self, country_id, date):
        return self.filter(city__country__id=country_id, date=date).aggregate(total_count=Coalesce(models.Sum("count"), 0))["total_count"]

    def city_total_count(self, city_id, date):
        return self.filter(city__id=city_id, date=date).aggregate(total_count=Coalesce(models.Sum("count"), 0))["total_count"]

    def get_country_percent(self, country_id, total_count, date):
        return (
            self.filter(city__country__id=country_id, date=date)
            .select_related("candidate")
            .values("candidate")
            .annotate(
                candidate_total_count=models.Sum("count"),
                total_count=models.Value(total_count),
                percent=models.ExpressionWrapper(
                    (models.F("candidate_total_count") * 100) / models.F("total_count"),
                    output_field=models.DecimalField(),
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

    def get_city_percent(self, city_id, total_count, date):
        return (
            self.filter(city_id=city_id, date=date)
            .select_related("candidate")
            .values("candidate")
            .annotate(
                candidate_total_count=models.Sum("count"),
                total_count=models.Value(total_count),
                percent=models.ExpressionWrapper(
                    (models.F("candidate_total_count") * 100) / models.F("total_count"),
                    output_field=models.DecimalField(),
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


class Election(BaseModel):
    candidate = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    decription = models.CharField(max_length=100)
    count = models.PositiveIntegerField()
    invalid_count = models.PositiveIntegerField(default=0)
    box_number = models.CharField(default="S-000000")
    date = models.DateField(default="2023-05-14")
    objects = ElectionManager()

    class Meta:
        db_table = "election"
