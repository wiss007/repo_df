=========
prescription
=========

Requirements
-----------
    * Python 2.7
    * Simquest
    * Simcalc running
    * mongod running with a local mongo 
        database: mydb
        collections: donnee_commune, coordonnee_geographique_commune
    bibliothèques python: requirements.txt
    
Installation:
------------
    Dev station :
    Not done yet !
    * pip install prescription-x.y.z.tar.gz

Test:
-----
    Work in progress
    python -m unittest2 test.py



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

