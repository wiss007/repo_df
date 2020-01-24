#!/usr/bin/python3
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
import numpy as np

import sys
sys.path.append('Utils/')

import prescription.toolbox as tb
import prescription.classification as cf
import prescription.notation as nt

from types import FunctionType



##########################
#    Parameters
##########################
data_path  = 'data/'



print('###################################################################')
print("#                    Module d'Optimisation Budgétaire             #")
print('################################################################### \n')
step = 0

if 0:
    step += 1
    print('     ____________________________________________________________')
    print('     \n          Entrez le code insee de la commune  :           ')
    print('     ____________________________________________________________')
    insee_client = str(eval(input("\n          votre choix >>>  ")))
else:
    insee_client = '77316'


step += 1
print('\n-------------------------------------------------------------------------------------')
print((step, ' Lecture du fichier de configuration'))
cfg = tb.cfg
print(('           - Code INSEE : ', cfg["code_insee"], '\n'))
print(('           - Année de comparaison : ', cfg['year']))

step += 1
print('\n-------------------------------------------------------------------------------------')
print((step, ' Lecture du fichier des comptes aggrégés '))
df_agr_full = pd.read_csv(data_path + 'comptes_individuels_communes_2020.csv', delimiter=';',dtype={'dep':str})# Mixed types: Corse 02A
df_agr_full['dep'] = df_agr_full['dep'].str.replace('^0+', '',regex=True)
dfsections = df_agr_full.loc[df_agr_full['dep']=='77']
df1= dfsections.loc[dfsections['inom']=='MORET-LOING-ET ORVANNE']
# print df1.head()


step += 1
print('\n-------------------------------------------------------------------------------------')
print((step, ' Lecture du fichier de géolocalisation '))
dfgeo = pd.read_csv(data_path + 'eucircos_regions_departements_circonscriptions_communes_gps_prepared.csv', delimiter=";")#',')
# print dfgeo.head()



step += 1
print('\n-------------------------------------------------------------------------------------')
print((step, ' Lecture du fichier de critere répartition '))
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
    print('')
    print('\n-------------------------------------------------------------------------------------')
    print((step, " Selection des collectivités de la CSEF 'classification' "))

    aux_collections = {}
    aux_collections['sections'] = df_agr_full  #dfsections
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
    print('\n-------------------------------------------------------------------------------------')
    print((step, " Récupération des données auxiliaires ('non balances comptables') pour les collectivités de la CSEF  "))
    print("      (ces données sont notamment nécéssaires au calcul des ratios en valeur par habitant)")
    # new way to proceed via the class list_csef
    # todo: generaliser pour recuperer l'ensemble des aux data sous forme de dico

    ratios_csef, aux_data_csef = nt.calcul_ratios(insee_classification['insee_csef'], aux_collections)


        #####################################################
        #
        #     A partir de là on fait du calcul de ratios
        #
        #####################################################

#######################################################
#   Notation des ratios
#######################################################
if cfg['notation']['use']:
    # if 0:
    step += 1
    print('\n-------------------------------------------------------------------------------------')
    print((step, ' Notation des collectivités de la csef sur  chaque  ratios'))

    notes_ratios_de_base = nt.process_ratios(ratios_csef, cfg['notation']['note_max'])


#######################################################
#  Notation par grand theme et selection des champions
#######################################################
if cfg['champions_selection']['use']:
    step += 1
    print('')
    print('\n-------------------------------------------------------------------------------------')
    print(step, ' Regroupement des ratios et selection des champions par grand theme V3')

    champions = nt.champions_selection(notes_ratios_de_base, aux_data_csef, cfg['champions_selection'])

    print(champions)
