from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
import os


@receiver(reset_password_token_created)
def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender:
    :param reset_password_token:
    :param args:
    :param kwargs:
    :return:
    """
    print("SENDING PASSWORD EMAIL TO ", reset_password_token.user.email)
    send_mail(
        'Password Reset for ICD Recommender',
        'Click below if you have requested a password reset.\n' +
        os.environ['DJANGO_FRONTEND_HOSTNAME'] + '/reset-password?token=' + reset_password_token.key + '\n',
        'noreply@icdrecommender.xyz',
        [reset_password_token.user.email],
        fail_silently=False,
    )
