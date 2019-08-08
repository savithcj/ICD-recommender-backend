from django.core.management.base import BaseCommand, CommandError
from recommendations.models import DaggerAsterisk, Code
from django.db import transaction
import csv


class Command(BaseCommand):
    help = 'Imports dagger asterisks'

    def handle(self, *args, **options):
        # Remove all existing objects before importing
        DaggerAsterisk.objects.all().delete()

        # Transaction.atomic in order to save all of the objects at once at the end
        with transaction.atomic():
            for i, line in enumerate(readFileFromS3("DaggerAsterisks")):
                row = line.split(',')
                # Skip the header
                if i == 0:
                    i += 1
                else:
                    if("-" in row[0]):  # Dagger has a -
                        code = Code.objects.get(code=row[0][:-1])
                        children = code.children.split(",")
                        for child in children:
                            DaggerAsterisk.objects.create(dagger=child, asterisk=row[1]).save()
                    elif("-" in row[1]):  # Asterisk has a -
                        code = Code.objects.get(code=row[1][:-1])
                        children = code.children.split(",")
                        for child in children:
                            DaggerAsterisk.objects.create(dagger=row[0], asterisk=child).save()
                    else:
                        # Create all of the objects
                        DaggerAsterisk.objects.create(dagger=row[0], asterisk=row[1]).save()
