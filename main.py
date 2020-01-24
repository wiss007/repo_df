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

    # initialisation aux_data_csef et ratios_csef
    if 1:
        aux_data_csef = {}
        ratios_csef = {}

        aux_data_csef['code_insee'] = []
        aux_data_csef['nom'] = []
        aux_data_csef['pop_insee'] = []
        aux_data_csef['regime_fiscal'] = []

        aux_data_csef['PFinh'] = []
        aux_data_csef['PFisch'] = []
        aux_data_csef['BBFB'] = []
        aux_data_csef['BBFNB'] = []
        aux_data_csef['EF'] = []
        aux_data_csef['PFB'] = []
        aux_data_csef['PFNB'] = []
        aux_data_csef['PTH'] = []

        ratios_csef['fprod'] = []
        ratios_csef['fpfcaf'] = []
        ratios_csef['rimpo1'] = []
        ratios_csef['rdgf'] = []
        #! not available in opendata file
        #ratios_csef['rdfctva'] = []
        #ratios_csef['rpserdom'] = []
        ratios_csef['fcharge'] = []
        ratios_csef['fcfcaf'] = []
        ratios_csef['rperso'] = []
        ratios_csef['rachat'] = []
        ratios_csef['rfin'] = []
        ratios_csef['rcont'] = []
        ratios_csef['fres1'] = []
        ratios_csef['frecinv'] = []
        ratios_csef['fdepinv'] = []
        ratios_csef['requip'] = []
        ratios_csef['rremb'] = []
        ratios_csef['fbf1'] = []
        ratios_csef['fbf2'] = []
        ratios_csef['fres2'] = []
        ratios_csef['rcaf'] = []
        ratios_csef['rdette'] = []
        ratios_csef['fdette'] = []
        ratios_csef['rannu'] = []
        ratios_csef['fannu'] = []
        ratios_csef['fpth'] = []
        ratios_csef['fpfb'] = []
        ratios_csef['fpfnb'] = []
        ratios_csef['tth'] = []
        ratios_csef['tfb'] = []
        ratios_csef['tfnb'] = []
    i=0
    ls_avance =[5,10,15,20,25,35]
    # recupération
    for code_insee in insee_classification['insee_csef']:
        i+=1
        aux_data = cf.auxiliary_data(code_insee, aux_coll=aux_collections)
        # Basic info
        aux_data_csef['code_insee'].append(str(code_insee))
        aux_data_csef['nom']. append(aux_data.get_data('2016')['Informations générales - Nom de la commune'].values[0])
        aux_data_csef['pop_insee'].append(aux_data.get_data('2016')['Informations générales - Population INSEE Année N '].values[0])
        aux_data_csef['regime_fiscal'].append(aux_data.get_data('2016')['Informations générales - Régime fiscal EPCI'].values[0])
        # Financial info
        aux_data_csef['PFinh'].append(aux_data.get_data('2016')['Potentiel fiscal et financier des communes - Potentiel financier par habitant'].values[0])
        aux_data_csef['PFisch'].append(aux_data.get_data('2016')['Potentiel fiscal et financier des communes - Potentiel fiscal 4 taxes par habitant'].values[0])
        aux_data_csef['BBFB'].append(aux_data.get_data('2016')['Potentiel fiscal et financier des communes - Bases brutes de FB'].values[0])
        aux_data_csef['BBFNB'].append(aux_data.get_data('2016')['Potentiel fiscal et financier des communes - Bases brutes de FNB'].values[0])
        aux_data_csef['EF'].append(aux_data.get_data('2016')['Effort fiscal - Effort fiscal'].values[0])
        aux_data_csef['PFB'].append(aux_data.get_data('2016')['Effort fiscal - Produit net FB'].values[0])
        aux_data_csef['PFNB'].append(aux_data.get_data('2016')['Effort fiscal - Produit net FNB (hors TAFNB)'].values[0])
        aux_data_csef['PTH'].append(aux_data.get_data('2016')['Effort fiscal - Produit net TH'].values[0])

        section_data = cf.auxiliary_data(code_insee, aux_coll=aux_collections)

        ########################################
        #               Fonctionnement
        ########################################
        # produits = TRRF
        ratios_csef['fprod'].append(aux_data.get_section('2016')['fprod'].values[0])#
        ratios_csef['fpfcaf'].append(aux_data.get_section('2016')['fpfcaf'].values[0])#
        ratios_csef['rimpo1'].append(aux_data.get_section('2016')['rimpo1'].values[0])#
        ratios_csef['rdgf'].append(aux_data.get_section('2016')['rdgf'].values[0])#
        #! no available in opendata file
        #ratios_csef['rdfctva'].append(aux_data.get_section('2016')['rdfctva'].values[0])#
        #ratios_csef['rpserdom'].append(aux_data.get_section('2016')['rpserdom'].values[0])#
        # charges  TDRF
        ratios_csef['fcharge'].append(aux_data.get_section('2016')['fcharge'].values[0])#
        ratios_csef['fcfcaf'].append(aux_data.get_section('2016')['fcfcaf'].values[0])#
        ratios_csef['rperso'].append(aux_data.get_section('2016')['rperso'].values[0])#
        ratios_csef['rachat'].append(aux_data.get_section('2016')['rachat'].values[0])#
        ratios_csef['rfin'].append(aux_data.get_section('2016')['rfin'].values[0])#
        ratios_csef['rcont'].append(aux_data.get_section('2016')['rcont'].values[0])#

        ratios_csef['fres1'].append(aux_data.get_section('2016')['fres1'].values[0])#

        ########################################
        #               Investissement
        ########################################
        # ressources d'investissement = TRRI
        ratios_csef['frecinv'].append(aux_data.get_section('2016')['frecinv'].values[0])#

        # emploi d'investissement = TDRI
        ratios_csef['fdepinv'].append(aux_data.get_section('2016')['fdepinv'].values[0])#
        ratios_csef['requip'].append(aux_data.get_section('2016')['requip'].values[0])#
        ratios_csef['rremb'].append(aux_data.get_section('2016')['rremb'].values[0])#

        ratios_csef['fbf1'].append(aux_data.get_section('2016')['fbf1'].values[0])#
        ratios_csef['fbf2'].append(aux_data.get_section('2016')['fbf2'].values[0])#
        ratios_csef['fres2'].append(aux_data.get_section('2016')['fres2'].values[0])#

        ########################################
        #               Dette
        ########################################
        ratios_csef['fdette'].append(aux_data.get_section('2016')['fdette'].values[0])#
        ratios_csef['rdette'].append(aux_data.get_section('2016')['rdette'].values[0])#
        ratios_csef['rcaf'].append(aux_data.get_section('2016')['rcaf'].values[0])#
        ratios_csef['rannu'].append(aux_data.get_section('2016')['rannu'].values[0])#
        ratios_csef['fannu'].append(aux_data.get_section('2016')['fannu'].values[0])#

        ########################################
        #               Fiscalite
        ########################################
        ratios_csef['fpth'].append(aux_data.get_section('2016')['fpth'].values[0])#
        ratios_csef['fpfb'].append(aux_data.get_section('2016')['fpfb'].values[0])#
        ratios_csef['fpfnb'].append(aux_data.get_section('2016')['fpfnb'].values[0])#
        ratios_csef['tth'].append(aux_data.get_section('2016')['tth'].values[0])#
        ratios_csef['tfb'].append(aux_data.get_section('2016')['tfb'].values[0])#
        ratios_csef['tfnb'].append(aux_data.get_section('2016')['tfnb'].values[0])#

        #display
        if 0:
            if i in ls_avance:
                print((i, ' / ', len(insee_classification['insee_csef']), ' communes requetées'))

    if 1:
        print('')
        print('          Controle des données auxiliaires des CL dans la csef')
        print(("\n          - 'code_insee    :", aux_data_csef['code_insee']))
        print(("\n          - 'nom           :", aux_data_csef['nom']))
        print(("\n          - 'pop_insee     :", aux_data_csef['pop_insee']))
        print(("\n          - 'regime fiscal :", aux_data_csef['regime_fiscal']))
        print(("\n          - 'FPFB          :", ratios_csef['fpfb']))
        print(("\n          - 'FPROD          :", ratios_csef['fprod']))





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

    inverted_notation=['rdette','fdette','rannue','fannue']
    notes_ratios_de_base = {}
    #for key in list(ratios_csef.keys()):
    #    print('')
    #    print('     -', key, '€/hab ', ratios_csef[key])
    for key in list(ratios_csef.keys()):
        print('')
        print('     -', key, ratios_csef[key])
        notes_ratios_de_base[key] = []
        if key in inverted_notation:
            notes_ratios_de_base[str(key)] = nt.notation_ratios(ratios_csef[key], cfg['notation']['note_max'],
                                                                reverse=True)
        else:
            notes_ratios_de_base[str(key)] = nt.notation_ratios(ratios_csef[key], cfg['notation']['note_max'])
        # print '             notes', notes_ratios_de_base[key]




#######################################################
#  Notation par grand theme et selection des champions
#######################################################
if cfg['champions_selection']['use']:
    step += 1
    print('')
    print('\n-------------------------------------------------------------------------------------')
    print(step, ' Regroupement des ratios et selection des champions par grand theme V3')

    notes_themes = {}
    champions = {}
    champions2 = {}


    # selections des champions thématiques (on garde le code_insee c'est plus safe qu'un index):
    #  1- pour chaque theme on ne garde que les collectivités qui présentent la note thématique la plus élevée
    for theme in cfg['champions_selection']['theme']:# Show all themes[0:2]:
        notes_themes[str(theme)] = nt.notation_theme(notes_ratios_de_base, cfg['champions_selection'][theme])

        print('          notes du thème {0}: {1} '.format(theme, notes_themes[str(theme)]))
        # fixme: il faut checker que la notation par grand theme prend bien en compte la ponderation que l'on a mise dans le fichier de config
        # fixme checker where à la place de argwhere

        idx = np.argwhere(notes_themes[theme] == np.amax(notes_themes[theme])).flatten().tolist()
        # champions[str(theme)]= [aux_data_csef['code_insee'][id] for id in idx]
        champions[str(theme)] = {}
        champions[str(theme)]['insee'] = [aux_data_csef['code_insee'][id] for id in idx]
        champions[str(theme)]['nom'] = [aux_data_csef['nom'][id] for id in idx]

        print('       - Champions ', theme, ' : ', champions[str(theme)]['nom'], champions[str(theme)]['insee'], [notes_themes[str(theme)][id] for id in idx])

