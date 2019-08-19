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
    print("SENDING PASSWORD EMAIL")
    send_mail(
        'Subject here',
        'Here is the message.\n' + reset_password_token.key,
        'noreply@icdrecommender.xyz',
        [os.environ['DJANGO_TEST_EMAIL']],
        fail_silently=False,
    )
    # # send an e-mail to the user
    # context = {
    #     'current_user': reset_password_token.user,
    #     'username': reset_password_token.user.username,
    #     # 'email': reset_password_token.user.email,
    #     'email': "eiden.yoshida@ucalgary.ca",
    #     # ToDo: The URL can (and should) be constructed using pythons built-in `reverse` method.
    #     'reset_password_url': "http://some_url/reset/?token={token}".format(token=reset_password_token.key)
    # }

    # # render email text
    # #email_html_message = render_to_string('email/user_reset_password.html', context)
    # email_plaintext_message = token = reset_password_token.key

    # msg = EmailMultiAlternatives(
    #     # title:
    #     _("Password Reset for {title}".format(title="Some website title")),
    #     # message:
    #     email_plaintext_message,
    #     # from:
    #     "noreply@somehost.local",
    #     # to:
    #     [reset_password_token.user.email]
    # )
    # msg.attach_alternative('test alternative', "text/html")
    # #msg.attach_alternative(email_html_message, "text/html")
    # msg.send()
