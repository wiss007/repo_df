venv:
	# install some software with a dev image here
	python3 -m venv venv
	venv/bin/pip install -U -r requirements.txt
	venv/bin/pip install -e .

data/2019-communes-criteres-repartition.csv:
	curl -L https://www.data.gouv.fr/fr/datasets/r/d9522fde-1aab-4925-a044-92d625b17d1b -o data/2019-communes-criteres-repartition.csv &

data/2018-communes-criteres-repartition.csv:
	curl -L https://www.data.gouv.fr/fr/datasets/r/86a4da6c-71af-4947-b007-85967936da9c -o data/2018-communes-criteres-repartition.csv &

data/comptes_individuels_communes_2020.csv:
	curl 'https://data.economie.gouv.fr/explore/dataset/comptes-individuels-des-communes/download/?format=csv&refine.an=2018&timezone=Europe/Berlin&use_labels_for_header=true&csv_separator=%3B' > data/comptes_individuels_communes_2020.csv &

data/eucircos_regions_departements_circonscriptions_communes_gps_prepared.csv:
	curl -o data/eucircos_regions_departements_circonscriptions_communes_gps_prepared.csv.gz http://www.nosdonnees.fr/wiki/images/b/b5/EUCircos_Regions_departements_circonscriptions_communes_gps.csv.gz && gzip -d data/eucircos_regions_departements_circonscriptions_communes_gps_prepared.csv.gz &

all_data: data/2019-communes-criteres-repartition.csv data/2018-communes-criteres-repartition.csv data/2019-communes-criteres-repartition.csv data/comptes_individuels_communes_2020.csv data/eucircos_regions_departements_circonscriptions_communes_gps_prepared.csv

up: venv all_data
	venv/bin/python3 main.py
