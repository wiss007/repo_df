Prescription
=========

Requirements
-----------
    * Python 2.7
    * bibliothèques python: requirements.txt
    
Installation:
------------
    Dev station :
    Not done yet !
    * pip install prescription-x.y.z.tar.gz

Test:
-----
    Work in progress
    python -m unittest2 test.py


Data:
-----

2019-communes-criteres-repartition.csv.zip:
 https://www.data.gouv.fr/fr/datasets/criteres-de-repartition-des-dotations-versees-par-letat-aux-collectivites-territoriales/  

comptes_individuels_communes_2020.csv.zip:
https://data.economie.gouv.fr/explore/dataset/comptes-individuels-des-communes/download/?format=csv&refine.an=2018&timezone=Europe/Berlin&use_labels_for_header=true&csv_separator=%3B

Default connexion setting:
-------------------------

    you need to run Simcal and Mongod

    settings = {
        'DOMAIN': 'http://127.0.0.1:8020',
        'API_PREFIX': 'api/v1',
        'TOKEN_TYPE': 'jwt',
        'TOKEN_FORMAT': 'Simco {token}',
        'LOGIN': 'auth/login/',
        'LOGOUT': 'auth/logout/',
    }
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFudGhvbiIsInVzZXJfaWQiOjExLCJlbWFpbCI6IiIsImV4cCI6MTUzNTgwNTI4MX0.jCS2XKVh0zq9zcY-YUBHyWo1pIBflvnk-OqD0tLSY6Y'





Python command line example:
------------

