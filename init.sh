#!/bin/sh

# obscure kaggle.json
chmod 600 ./kaggle.json
# download dataset from kaggle
kaggle datasets download -d berkeleyearth/climate-change-earth-surface-temperature-data
# unzip GlobalLandTemperaturesByCity dataset
unzip climate-change-earth-surface-temperature-data.zip "GlobalLandTemperaturesByCity.csv" -d .
# make initial migration for the table
python manage.py makemigrations climate_change
# apply the migration
python manage.py migrate climate_change
# load dataset into postgres
psql -h db -U postgres -p 5432 -c "\COPY global_land_temperatures_by_city(date,average_temperature,average_temperature_uncertainty,city,country,latitude,longitude) FROM './GlobalLandTemperaturesByCity.csv' delimiter ',' CSV HEADER;"
# run server
python manage.py runserver 0.0.0.0:8000
