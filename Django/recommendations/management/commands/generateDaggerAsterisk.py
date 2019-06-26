from django.core.management.base import BaseCommand, CommandError
from recommendations.models import DaggerAsterisk
from django.db import transaction
import csv


class Command(BaseCommand):
    help = 'Imports dagger asterisks'

    def handle(self, *args, **options):
        DaggerAsterisk.objects.all().delete()

        with transaction.atomic():
            with open('secret/DaggerAsterisksCodes.csv') as f:
                r = csv.reader(f, delimiter=',')
                i = 0
                for row in r:
                    if i == 0:
                        i += 1
                    else:
                        DaggerAsterisk.objects.create(dagger=row[0], asterisk=row[1]).save()
