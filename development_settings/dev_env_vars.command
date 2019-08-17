#! /bin/bash
echo Loadind development environment variables...
export RDS_DB_NAME=icd_recommender
export RDS_USERNAME=YOUR_POSTGRESQL_DATABASE_USERNAME
export RDS_PASSWORD=""
export RDS_HOSTNAME=127.0.0.1
export RDS_PORT=5432
export DJANGO_ADMIN_PASSWORD=admin
export DJANGO_SECRET_KEY="YOUR_DJANGO_SECRET_KEY"
export ICD_DATA_LOCATION=LOCAL
echo Done!