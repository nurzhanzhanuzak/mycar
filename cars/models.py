from django.db import models
from postgres_copy import CopyManager


class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    make = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    mileage = models.FloatField(null=True)
    engine = models.CharField(max_length=255, null=True)
    transmission = models.CharField(max_length=20, null=True)
    body = models.CharField(max_length=20, null=True)
    drive = models.CharField(max_length=20, null=True)
    color = models.CharField(max_length=20, null=True)
    price = models.FloatField(null=True)

    objects = CopyManager()
