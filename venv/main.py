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

    # print 'Aux coll in main', aux_collections
    # print 'Aux coll critere repart', aux_collections['criteres_repart']
    # print 'Test', aux_collections['criteres_repart']['Informations générales - Code département de la commune']
    # small_df = aux_collections['criteres_repart'].loc[aux_collections['criteres_repart']['Informations générales - Code département de la commune']=='77']
    # print 'small df', small_df.head()

    aux_data = cf.auxiliary_data(insee_client, aux_coll=aux_collections)




    insee_classification = aux_data.find_communes_csef2(cfg['year'])






