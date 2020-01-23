#!/usr/bin/python2.7
#-*- coding: utf-8 -*-


"""
Anthony Guignard 22/01/2020
Module regroupant les classes et les fonctions nécéssaires à la classification des collectivités
"""


##########################
#       Libraries
##########################
import os.path
import numpy as np
import pandas as pd

from utils import maths_functions as mf
from toolbox import cfg
# from pymongo import MongoClient




class auxiliary_data():
    """
    Les données issues des bases de données auxiliaires (non M14)
    """
    def __init__(self, insee, aux_coll):
        self.insee = insee

        # differentes collections peuvent etre utilisées

        self.aux_collection = aux_coll['criteres_repart']
        self.geo_collection = aux_coll['coordonnees_geographiques']
        self.ratio_collection = aux_coll['sections']

        self.data = None
        self.fisca = None
        self.coord = None

        self.communes_departement = None
        self.communes_regime_fiscal = None
        self.communes_strate = None
        self.communes_proximite = None

        self.classif_insee = {}


    def get_data(self, year):
        """
        Recupère les données_communales (~ fiches DGF)
        :return: data
        """
        if self.data is None:

            self.data = self.aux_collection.loc[self.aux_collection['Informations générales - Code INSEE de la commune'] == int(self.insee)]


            # self.data = self.aux_collection.find({'$and': [{'ANNEE': int(year)}, {'INSEE': self.insee}]})[0]
        return self.data

    def get_coord(self):
        """
        Récupère les coordonnées geographiques (latitude, longitude)
        :return: coord(latitude and longitude en degré décimal)
        """
        # self.geo_collection = geo_collection
        if self.coord is None:
            self.coord= self.geo_collection.find({'$and':[{'ANNEE':2017}, {'INSEE': self.insee}]})[0]
        return self.coord

    def get_fisca(self, year):
        """
        Recupère les données_communales (~ fiches DGF)
        :return: data
        """
        if self.fisca is None:
            self.fisca = self.aux_collection['Informations générales - Régime fiscal EPCI'].loc[self.aux_collection['Informations générales - Code INSEE de la commune'] == int(self.insee)].values[0]
        return self.fisca


    def find_communes_strate(self, year):
        """
        Selectionne les commune de la même strate de population
        :param year:
        :return: liste de codes insee
        """

        strate_thrld = [0, 500, 1000, 2000, 3500, 5000, 7500, 10000, 15000, 20000, 35000, 50000, 75000, 100000, 200000]
        if self.communes_strate is None:
            pop = self.aux_collection['Informations générales - Population INSEE Année N '].loc[self.aux_collection['Informations générales - Code INSEE de la commune'] == int(self.insee)].values[0]

            for i in range(len(strate_thrld)):
                if strate_thrld[i] <= pop < strate_thrld[i + 1]:
                    strate = i
            print '       .les collectivités seront sélectionnées dans la strate', strate_thrld[strate],'-', strate_thrld[strate + 1], 'habitants'

            datas = self.aux_collection.loc[\
                (self.aux_collection['Informations générales - Population INSEE Année N '] >=  strate_thrld[strate]) & \
                (self.aux_collection['Informations générales - Population INSEE Année N '] < strate_thrld[strate+1])]

            self.communes_strate = []
            self.communes_strate = datas['Informations générales - Code INSEE de la commune'].values
        return self.communes_strate.tolist()

    def find_communes_departement(self, year):
        """
        Selectionne les communes du même département
        :param year:
        :return: liste de codes insee
        """

        if self.communes_departement is None:
            print '       .les collectivités seront sélectionnées dans le département ', self.insee[0:2]

            datas = self.aux_collection.loc[self.aux_collection['Informations générales - Code département de la commune'] == str(self.insee[0:2])]
            self.communes_departement = []
            self.communes_departement = datas['Informations générales - Code INSEE de la commune'].values
        return self.communes_departement.tolist()

    def find_communes_regime_fiscal(self, year):
        """
        Selectionne les communes du meme regime fiscal
        :param year:
        :return: liste de codes insee
        """
        if self.communes_regime_fiscal is None:
            fiscalite = self.get_fisca('2017')
            print "       .le regime fiscal que l'on souhaite est ", fiscalite
            datas = self.aux_collection.loc[self.aux_collection['Informations générales - Régime fiscal EPCI'] == self.fisca]
            self.communes_regime_fiscal = []
            self.communes_regime_fiscal = datas['Informations générales - Code INSEE de la commune'].values
        return self.communes_regime_fiscal.tolist()


    def find_communes_proximite(self):
        """
        Selectionne les communes dans un périmètre de 50km (par defaut)
        :return: liste de codes insee
        """
        dist_thrld = cfg['classification']['perimeter']
        print '       .les collectivités seront analysées dans un rayon de {0} km'.format(dist_thrld)

        if self.communes_proximite is None:

            lat = float(self.geo_collection['latitude'].loc[self.geo_collection['code_insee'] == int(self.insee)].values[0])
            lon = float(self.geo_collection['longitude'].loc[self.geo_collection['code_insee'] == int(self.insee)].values[0])

            # préselection des collectivités
            datas = self.geo_collection.loc[ \
                (self.geo_collection['latitude'] >= lat - 1.) & \
                (self.geo_collection['latitude'] < lat + 1.) & \
                (self.geo_collection['longitude'] >= lon - 1.) & \
                (self.geo_collection['longitude'] < lon + 1.)]

            # calcul distance
            self.communes_proximite = []
            for i in range(0,len(datas.latitude)):
                dist = mf.calcul_distance(lon, lat, datas.longitude.values[i], datas.latitude.values[i])
                if dist < dist_thrld:
                    self.communes_proximite.append(datas.code_insee.values[i])
        return self.communes_proximite

    # def find_communes_csef(self,year):
    #     """
    #     - Ajoute les communes du département aux communes des alentours
    #     - Ne retient que les communes de la bonne strate de population
    #     :param year:
    #     :return: liste de codes insee
    #     """
    #     list_geo = set(self.find_communes_departement(year) + self.find_communes_proximite())
    #     liste_strate = self.find_communes_strate(year)
    #     liste_fisca = self.find_communes_regime_fiscal(year)
    #     self.communes_csef  = mf.common_elements(list_geo, liste_strate, liste_fisca)
    #     return self.communes_csef

    def find_communes_csef2(self,year):
        """
        - Ajoute les communes du département aux communes des alentours
        - Ne retient que les communes de la bonne strate de population
        :param year:
        :return: un dictionnaire des communes à comparer
        """
        #fixme: on a pas intégré les données communales pour 2017 2016 etc
        #list_geo = set(self.find_communes_departement(year) + self.find_communes_proximite())

        print '   - find communities same dep'
        liste_departement= self.find_communes_departement(year)
        print '   - find communities same strate'
        liste_strate = self.find_communes_strate(year)
        print '   - find communities same proximity'
        liste_proximite = self.find_communes_proximite()
        print '   - find communities same fisca'
        liste_fisca = self.find_communes_regime_fiscal(year)


        print '\n'
        print '  - liste_strate ', len(liste_strate)
        print '  - liste_departement ', len(liste_departement)
        print '  - liste_proximite ', len(liste_proximite)
        print '  - liste_fisca', len(liste_fisca)

        self.communes_csef  = mf.common_elements(liste_strate, liste_departement, liste_proximite, liste_fisca)

        self.classif_insee['insee_csef'] = self.communes_csef
        self.classif_insee['insee_strate'] = self.communes_strate
        self.classif_insee['insee_departement'] = self.communes_departement
        self.classif_insee['insee_proximite'] = self.communes_proximite
        self.classif_insee['insee_fiscalite'] = self.communes_regime_fiscal

        print '  - liste communes csef', len(self.communes_csef)
        return self.classif_insee


