from os import environ
import requests

SECRET_KEY = environ["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = [str(environ['DJANGO_HOST_ADDRESS'])]
FRONT_END_BASE_URL = environ['FRONT_END_BASE_URL']
FRONT_END_OAUTH_CLIENT_ID = environ['FRONT_END_OAUTH_CLIENT_ID']

EMAIL_HOST_PASSWORD = environ['DJANGO_EMAIL_PASSWORD']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True      # Request over HTTP are redirected over HTTPS
SESSION_COOKIE_SECURE = True    # Instructs browser to only send cookie over HTTPS
CSRF_COOKIE_SECURE = True       # Instructs browser to send CSRF cookie over HTTPS
CORS_ALLOWED_ORIGINS = [FRONT_END_BASE_URL]

STATIC_URL = '/static/'


try:  # Enabling AWS health-checks
    AWS_LOCAL_IP = requests.get(
        'http://169.254.169.254/latest/meta-data/local-ipv4',
        timeout=0.01
    ).text
    ALLOWED_HOSTS.append(AWS_LOCAL_IP)
except requests.exceptions.RequestException:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ['RDS_DB_NAME'],
        'USER': environ['RDS_USERNAME'],
        'PASSWORD': environ['RDS_PASSWORD'],
        'HOST': environ['RDS_HOSTNAME'],
        'PORT': environ['RDS_PORT'],
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'db.sqlite3',
    #     'OPTIONS': {
    #         'timeout': 3600,
    #     }
    # }
}
