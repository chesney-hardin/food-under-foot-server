#!/bin/bash

rm db.sqlite3
rm -rf ./foodunderfootapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations foodunderfootapi
python3 manage.py migrate foodunderfootapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata usability
python3 manage.py loaddata plant_parts
python3 manage.py loaddata wild_plants
python3 manage.py loaddata edible_parts
python3 manage.py loaddata harvest_logs
