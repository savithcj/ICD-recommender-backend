from subprocess import call
from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):

    help = 'Initialize project.'

    def handle(self, *args, **kwargs):

        Application.objects.get_or_create(client_id=settings.FRONT_END_OAUTH_CLIENT_ID,
                                          defaults={
                                              "client_type": "Public",
                                              "authorization_grant_type": "password",
                                              "name": "frontend"
                                          })

        call_command("importRules")
        call_command("generateCodeTable")
        call_command("generateTreeCodeTable")
        call_command("generateDaggerAsterisk")
        call_command("setUseNumbers", mode='random')
        call_command("calcBlockUseNumbers")
