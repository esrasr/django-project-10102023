from django.db import models
from apps.base.models import BaseModel


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
    # image

    class Meta:
        db_table = "candidates"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Election(BaseModel):
    candidate = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    decription = models.CharField(max_length=100)
    count = models.IntegerField()

    class Meta:
        db_table = "election"
