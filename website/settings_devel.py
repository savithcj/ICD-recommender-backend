from os import environ

print("WARNING: RUNNING IN DEVELOPEMENT SETTINGS")
SECRET_KEY = environ.get('DJANGO_SECRET_KEY') or "4z^fqzy5wu+#$4u0fpg0y(8nv6sdbvf#yngz&9@u))yhod_q1f"
ALLOWED_HOSTS = [str(environ.get('DJANGO_HOST_ADDRESS')), 'localhost', '127.0.0.1']
CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3000", "http://localhost:3000"]
FRONT_END_BASE_URL = environ.get('FRONT_END_BASE_URL') or "http://localhost:3000"
FRONT_END_OAUTH_CLIENT_ID = environ.get('FRONT_END_OAUTH_CLIENT_ID') or "u8N1bB2nlWTaMsj6qp2Y8f30sU1pFlIeaDuZgV0U"

if FRONT_END_BASE_URL:
    CORS_ALLOWED_ORIGINS.append(FRONT_END_BASE_URL)

SESSION_COOKIE_SECURE = False
# static file storage settings
STATIC_URL = '/static/'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

COGNITO_AWS_REGION = environ.get('COGNITO_AWS_REGION') or 'us-west-2'  # ie:'us-west-2'
COGNITO_USER_POOL = environ.get('COGNITO_USER_POOL') or 'us-west-2_ABCDEFG'  # ie: 'use-west-2_ABCDEFG'
COGNITO_CLIENT_ID = environ.get('COGNITO_CLIENT_ID') or 'my_devel_client_id'
# COGNITO_CLIENT_SECRET = environ.get('COGNITO_CLIENT_SECRET') or 'default_secret_values' # not implemented
EMAIL_HOST_PASSWORD = environ.get('DJANGO_EMAIL_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'OPTIONS': {
            'timeout': 3600,
        }
    }
    # If using postgres for local development:
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': environ.get('RDS_DB_NAME') or "icd_recommender",
    #     'USER': environ.get('RDS_USERNAME') or "postgres",
    #     'PASSWORD': environ.get('RDS_PASSWORD') or "",
    #     'HOST': environ.get('RDS_HOSTNAME') or "127.0.0.1",
    #     'PORT': environ.get('RDS_PORT') or "5432",
    # }
}
