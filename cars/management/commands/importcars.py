from cars.models import Car
from django.core.management.base import BaseCommand
from cars.management.commands._scraper import FIELDS, MODEL_FIELDS, scrape
import tempfile
import csv
import os


class Command(BaseCommand):
    help = 'Imports cars data into db'

    def handle(self, *args, **options):
        car_dicts = scrape(10)
        fd, path = tempfile.mkstemp('.csv', text=True)
        with open(path, 'r+') as f:
            writer = csv.DictWriter(f, FIELDS)
            writer.writeheader()
            writer.writerows(car_dicts)
        Car.objects.all().delete()
        Car.objects.from_csv(path, mapping=dict(zip(MODEL_FIELDS, FIELDS)))
        os.close(fd)
