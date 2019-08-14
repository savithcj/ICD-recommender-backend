## Setting up local development server

1. Install the required dependencies
```
pip install -r requirements.txt
```

2. Set up the following environment variables:
Postgres SQL development server settings:
```
RDS_DB_NAME
RDS_USERNAME
RDS_PASSWORD
RDS_HOSTNAME
RDS_PORT
```
Django development server settings:
```
DJANGO_ADMIN_PASSWORD
DJANGO_SECRET_KEY
ICD_DATA_LOCATION
```
The ICD_DATA_LOCATION should only be set to "S3" when deploying to AWS.

3. Create a secret folder under Django/, and copy files for populating database into this directory: 
```
Django/secret/
```
The files should include the following:
- categories.csv
- codedescriptions.txt
- DAD_dx_counts.csv
- DaggerAsterisks.csv
- DaggerAsterisksCodes.csv
- four_digit_rules.csv
- icd10cm_index_2020.xml
- ICDBlocks.txt
- ICDChapters.txt
- keywordTerms.txt
- output_rules_cleaned_shuffled.csv
- output_rules_cleaned_trunc3.csv
- output_rules_cleaned_trunc4.csv
- output_rules_cleaned.csv
- term_preprocessing.py
- three_digit_rules.csv

4. Create a database named icd_recommender, and set the appropriate configurations in Django/website/settings.py that matches what has been set previously inthe environment variables.

5. Open terminal, navigate to Django/, and use the commands below.
Initialize the database:
```
python manage.py makemigrations
python manage.py migrate
```
Create a super user for Django:
```
python manage.py createsuperuser
```
Populating the database:
```
python runScripts.py
```
Finally, start the Django server:
```
python manage.py runserver
```

6. Open browser, and navigate to Django admin, such as:
```
http://localhost:8000/admin/
```
Log in using the super user account that was previously set up in the previous step, and add an OAuth2 application by clicking on the add button next to Applications under DJANGO OAUTH TOOLKIT. The settings should be as the following:
- Client type: Public
- Authorization grant type: Resource owner password-based
Save and close Django admin.
