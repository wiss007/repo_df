#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
Module qui contient les fonctions mathématiques de base
"""
##########################
#       Libraries
##########################
import inspect
import numpy as np
from math import radians, sin, cos, asin, sqrt


def calcul_distance(lon1, lat1, lon2, lat2):
    """
    Calcul la distance entre de points à partir des coordonnees geographique
    latitude, longitude exprimées en degré decimal
    :param lon1:
    :param lat1:
    :param lon2:
    :param lat2:
    :return: la distance entre les 2 points en km
    """
    # convert decimal degrees to radians
    lon1 = float(lon1)
    lat1 = float(lat1)
    lon2 = float(lon2)
    lat2 = float(lat2)
    if not -999.0 in [lon1, lat1, lon2, lat2]:
        if (-90.< lat1 <90.) and (-90. < lat2 < 90.) and (-180. < lon1 < 180.) and (-180. < lon2 < 180.) :
            lon1, lat1, lon2, lat2 = list(map(radians, [lon1, lat1, lon2, lat2]))
            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            km = 6367. * c
        else:
            km = 100000.
    else:
        km = 1000000.
    return km

def common_elements(*lists):
    inter_list = list()
    for single_list in lists:
        if len(single_list) > 0:
            if len(inter_list) == 0:
                inter_list = single_list
            else:
                inter_list = list(set(inter_list) & set(single_list))
    return inter_list

def mean_mongo_data(collection, var_name, year, insee_list):
    #todo: rajouter un masque au cas ou certaines valeurs seraient manquantes
    #todo la connexion à la bdd sera exportée dans une autre fonction get_data_aux
    var = []
    pond = []
    req = collection.find({'$and': [{'ANNEE': int(year)}, {'INSEE': {'$in': insee_list}}]})
    for data in req:
        print('In fct', data[var_name])
        var.append(data[var_name])
        pond.append(1.)
    pop_tot = np.sum(i for i in pond)
    mean_value = np.sum(var[i]*pond[i] for i in range(len(pond))) / float(pop_tot)
    return mean_value
    del req, mean_value

def pop_ponderate_mean_mongo_data(collection, var_name, year, insee_list):
    #todo: rajouter un masque au cas ou ceratines valeurs seraient manquantes
    # todo la connexion aux bdd seront exportées dans get_data_aux et get_data_m14
    var = []
    pond = []
    req = collection.find({'$and': [{'ANNEE': int(year)}, {'INSEE': {'$in': insee_list}}]})
    for data in req:
        var.append(data[var_name])
        pond.append(data['POP_INSEE'])
    pop_tot = np.sum(i for i in pond)
    mean_value = np.sum(var[i]*pond[i] for i in range(len(pond))) / float(pop_tot)
    return mean_value
    del req, mean_value

def mean_per_inhabitant(numerator_name, denominateor_name, year, insee_list):
    """
    :param numerator_name:
    :param denominateor_name:
    :param year:
    :param insee_list:
    :return: un ratio calculé comme la valeur moyenne par habitant
    """

def reject_outliers(data):
    """
    Remplace les données aberrantes d'une population ainsi que les NaN par la valeur NaN
    Pour cela on suppose:
        - une distribution normale
        - unintervalle de 'confiance' fixé à 2 sigma
    :param data: une liste de valeurs
    :return: une liste de valeurs sans les valeurs aberrantes
    """
    #todo: prendre la mediane au lieu de la moyenne ( = np.median(data))
    m = 2.
    u = np.nanmean(data) #ignore Nan
    s = np.nanstd(data)  #ignore Nan
    filtered = []

    for val in data:
        if (u - m * s < val < u + m * s):
            filtered.append(val)
        else:
            filtered.append(np.nan)
    # todo: voir si on retourne les valeurs rejetés
    rejected = [e for e in data if e not in filtered]
    print('             données rejetées', len(rejected)+data.count(np.nan), '/', len(data), rejected)
    return filtered

def binning(dist,nb_bins):
    """
    Definit le binning à partir des valeurs extremes
    Utilisé lors du calcul des histrogrammes d'une distribution
    :param dist: une liste de valeurs
    :param nb_bins: le nombre de bins (10 ou 20)
    :return: liste des bornes inférieures, liste des bornes supérieures, le pas
    """
    pas = float(np.nanmax(dist) - np.nanmin(dist)) / float(nb_bins)
    bornes_inf = [np.nanmin(dist) + x * pas for x in range(0, nb_bins)]
    bornes_sup = [bornes_inf[x] + pas for x in range(0, nb_bins)]

    return bornes_inf, bornes_sup, pas

def calcul_par_habitant(self, comptes, pop):
    """
    Ramene les montants des différentes comptes valeur par habitant (€/hab)
    Les valeurs au numerateur sont issues des comptes récupérés via la classe SimcalcView
    l'effectif au numérateur est issu de la BDD Mongo locale
    :return: une liste pour comprenat les valeurs par habitant de chaque compte
    """
    # print '     Length()', len(self.comptes)

    self.comptes = comptes
    self.pop = pop
    if self.valeurs_par_habitant is None:
        self.valeurs_par_habitant = {}
        for ic in range(len(self.comptes)):
            # print '     calcul par habitant', self.comptes.keys()[ic], self.comptes.values()[ic]
            # r.append(float(self.comptes.values()[ic]) / float(self.pop))
            self.valeurs_par_habitant[list(self.comptes.keys())[ic]] = float(list(self.comptes.values())[ic]) / float(self.pop)
    return self.valeurs_par_habitant


