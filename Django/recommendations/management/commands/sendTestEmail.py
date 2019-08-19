from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("SENDING TEST EMAIL")
        send_mail('Test email', 'Test email', 'noreply@icdrecommender.xyz', [os.environ['DJANGO_TEST_EMAIL']])
