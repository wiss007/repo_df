#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# encoding: utf-8

####################################################################################################
# Anthony Guignard 22/01/2020
# ce programme permet de lire:
#  la M14 (en csv)
#  les données auxiliaires (en csv): critères de repartition + géolocalisatio
####################################################################################################


##########################
#       Libraries
##########################
# basics

import warnings
warnings.filterwarnings("ignore")

import os, os.path
import time
import copy
import string

import pandas as pd

import sys
sys.path.append('Utils/')

import toolbox as tb
import classification as cf



from types import FunctionType



##########################
#    Parameters
##########################





print '###################################################################'
print "#                    Module d'Optimisation Budgétaire             #"
print '################################################################### \n'
step = 0

if 0:
    step += 1
    print '     ____________________________________________________________'
    print '     \n          Entrez le code insee de la commune  :           '
    print '     ____________________________________________________________'
    insee_client = str(raw_input("\n          votre choix >>>  "))
else:
    insee_client = '77316'


step += 1
print '\n-------------------------------------------------------------------------------------'
print step, ' Lecture du fichier de configuration'
cfg = tb.cfg
print '           - Code INSEE : ', cfg["code_insee"], '\n'
print '           - Année de comparaison : ', cfg['year']

step += 1
print '\n-------------------------------------------------------------------------------------'
print step, ' Lecture du fichier des comptes aggrégés '
data_path  = '/Users/Anthony/PycharmProjects/data/'
df_agr_full = pd.read_csv(data_path + 'comptes_individuels_communes_2020.csv', delimiter=';',dtype={'dep':str})# Mixed types: Corse 02A
dfsections = df_agr_full.loc[df_agr_full['dep']=='77']
df1= dfsections.loc[dfsections['inom']=='MORET-LOING-ET ORVANNE']
# print df1.head()


step += 1
print '\n-------------------------------------------------------------------------------------'
print step, ' Lecture du fichier de géolocalisation '
data_path  = '/Users/Anthony/PycharmProjects/data/'
dfgeo = pd.read_csv(data_path + 'eucircos_regions_departements_circonscriptions_communes_gps_prepared.csv', delimiter=',')
# print dfgeo.head()



step += 1
print '\n-------------------------------------------------------------------------------------'
print step, ' Lecture du fichier de critere répartition '
data_path  = '/Users/Anthony/PycharmProjects/data/'
df_repart_full = pd.read_csv(data_path + '2019-communes-criteres-repartition.csv', delimiter=',',dtype={'Informations générales - Code département de la commune':str})# Mixed types: Corse 02A
# df = df_agr_full.loc[df_agr_full['dep']=='77']
# df1 = df.loc[df['inom']=='MORET-LOING-ET ORVANNE']
#print df_repart_full.head()
#
#



################################################
#   Appel au module de classification
################################################
if cfg['classification']['use']:
    step += 1
    print ''
    print '\n-------------------------------------------------------------------------------------'
    print step, " Selection des collectivités de la CSEF 'classification' "

    aux_collections = {}
    aux_collections['sections'] = dfsections
    aux_collections['coordonnees_geographiques'] = dfgeo
    aux_collections['criteres_repart'] = df_repart_full

    aux_data = cf.auxiliary_data(insee_client, aux_coll=aux_collections)
    insee_classification = aux_data.find_communes_csef2(cfg['year'])

else:
    insee_classification = {}
    insee_classification['insee_csef'] = liste_clients


###################################################
#  Get Auxillaries data for all that cities
###################################################
if cfg['classification']['use']:
    step += 1
    print '\n-------------------------------------------------------------------------------------'
    print step, " Récupération des données auxiliaires ('non balances comptables') pour les collectivités de la CSEF  "
    print "      (ces données sont notamment nécéssaires au calcul des ratios en valeur par habitant)"
    # new way to proceed via the class list_csef
    # todo: generaliser pour recuperer l'ensemble des aux data sous forme de dico
    aux_data_csef = {}
    aux_data_csef['code_insee'] = []
    aux_data_csef['pop_insee'] = []
    aux_data_csef['voirie'] = []
    aux_data_csef['superficie'] = []
    aux_data_csef['revenus'] = []
    aux_data_csef['regime_fiscal'] = []
    aux_data_csef['categorie'] = []
    aux_data_csef['nom'] = []

    for code_insee in insee_classification['insee_csef']:
        aux_data = cf.auxiliary_data(code_insee, aux_coll=aux_collections)

        #fixme: les dernières données concernent 2016 mais pas au delà


        #fixme: il faudrait creer kes clef de aux_data_csef à partir de la liste des clefs
        aux_data_csef['code_insee'].append(str(code_insee))
        aux_data_csef['pop_insee'].append(aux_data.get_data('2016')[cfg['ratio_calculation']['effectif']])
        aux_data_csef['voirie'].append(aux_data.get_data('2016')['VOIRIE'])
        aux_data_csef['superficie'].append(aux_data.get_data('2016')['SUPERFICIE'])
        aux_data_csef['revenus'].append(aux_data.get_data('2016')['REVENUS'])
        aux_data_csef['regime_fiscal'].append(str(aux_data.get_fisca('2016')['REGIME_FISCAL']))
        aux_data_csef['categorie'].append(aux_data.get_fisca('2016')['CATEGORIE'])
        # aux_data_csef['nom'].append(str(aux_data.get_coord()['NOM']))
        #fixme: probleme avec les accents des noms de villes
        aux_data_csef['nom'].append((aux_data.get_coord()['NOM'].encode('utf8')))
        # aux_data_csef['nom'].append((aux_data.get_coord()['NOM'].encode('ANSI')))

