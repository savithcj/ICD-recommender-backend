

#!/bin/bash

echo "Removing existing environment/ directory..."
rm -r environment

echo "Creating new environment at environment/ ..."
python3 -m venv environment/

if [[ "$OSTYPE" == "msys"* ]]
then
	ENVPATH="environment/Scripts/activate"
elif [[ "$OSTYPE" == "cygwin"* ]]
then
	ENVPATH="environment/Scripts/activate"
elif [[ "$OSTYPE" == "win32"* ]]
then
	ENVPATH="environment/Scripts/activate"
else
	ENVPATH="environment/bin/activate"
fi

echo "Installing python packages to environment at $ENVPATH ..."
source $ENVPATH
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
deactivate

echo "Creating activate.sh..."

touch activate.sh
echo >>activate.sh
echo 'source environment/bin/activate'>>activate.sh
echo 'export RDS_DB_NAME=icd_recommender'>>activate.sh
echo 'export RDS_USERNAME=postgres'>>activate.sh
echo 'export RDS_PASSWORD=""'>>activate.sh
echo 'export RDS_HOSTNAME=127.0.0.1'>>activate.sh
echo 'export RDS_PORT=5432'>>activate.sh
echo 'export DJANGO_SECRET_KEY="dt)(9z5cnh@94**+f@j5+v%w-9c&p&@y*!md196p3nk1&*1jqr"'>>activate.sh
echo 'export DJANGO_DEBUG=true'>>activate.sh
echo 'export DJANGO_EMAIL_USERNAME=""'>>activate.sh
echo 'export DJANGO_EMAIL_PASSWORD=""'>>activate.sh
echo 'export DJANGO_HOST_ADDRESS=127.0.0.1'>>activate.sh
echo 'export FRONT_END_BASE_URL=http://localhost:3000'>>activate.sh
echo >>activate.sh

echo 'Finished setting up environment. Please set up environment variables in activate.sh.'
echo 'To activate environment, run `source activate.sh`.'