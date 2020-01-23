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

import sys
sys.path.append('Utils/')

import utils.toolbox as tb
import utils.classification as cf



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
dfsections = df_agr_full.loc[df_agr_full['dep']=='77']
df1= dfsections.loc[dfsections['inom']=='MORET-LOING-ET ORVANNE']
# print df1.head()


step += 1
print('\n-------------------------------------------------------------------------------------')
print((step, ' Lecture du fichier de géolocalisation '))
dfgeo = pd.read_csv(data_path + 'eucircos_regions_departements_circonscriptions_communes_gps_prepared.csv', delimiter=',')
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
    aux_data_csef = {}
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

    aux_data_csef['ttt'] = []

    i=0
    ls_avance =[5,10,15,20,25,35]
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
        aux_data_csef['code_insee'].append(str(code_insee))
        aux_data_csef['ttt'].append(aux_data.get_section('2016')['icom'].values[0])

        #display
        if 0:
            if i in ls_avance:
                print(i, ' / ', len(insee_classification['insee_csef']), ' communes requetées')




    #check output
    if 0:
        print('')
        print('          Controle des données auxiliaires des CL dans la csef')
        print("\n          - 'code_insee    :", aux_data_csef['code_insee'])
        print("\n          - 'pop_insee     :", aux_data_csef['pop_insee'])
        print("\n          - 'regime fiscal :", aux_data_csef['regime_fiscal'])
        print("\n          - 'nom           :", aux_data_csef['nom'])
        print("\n          - 'BBFB          :", aux_data_csef['BBFB'])





        #####################################################
        #
        #     A partir de là on fait du calcul de ratios
        #
        #####################################################




#####################################################
#
#           Calcul de ratios
#
#####################################################


#######################################################
#   Pour chaque code insee figurant dans la liste
#    on crée un objet suivant la classe m14_ens
#######################################################
# step += 1
# print '\n-------------------------------------------------------------------------------------'
# print step, ' Récupération des données compta pour l ensemble des collectivités de la CSEF'
#
# m14_ens = ['' for i in range(len(aux_data_csef['code_insee']))]
# m14_ens = []
# ic = 0
# start_time_all = time.time()
# ratios_de_base = {}
#
# for csef in aux_data_csef['code_insee']:
#
#
#     #todo adapter le calcul des ratios  à partir des nouvelles sections et nouveaux élément
#
#     self.ratio_collection
#
#     request = {
#         'base_url': 'http://localhost:8020',
#         'api_prefix': 'api/v1',
#         'api_branch': 'getviewensemble/' + csef + '/',
#         'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhaHBhIiwidXNlcl9pZCI6MSwiZW1haWwiOiJwYWhwYUBvcmFuZ2UuZnIiLCJleHAiOjE1NDQxOTIyNzh9.gbrlQaop293UzzPig1OoaHRwvwk_12mDITBNDj_LoVU'
#     }
#     print '       -Requete Vue Ensemble', csef, id
#     c = simquest.SimQuest(request)
#
#
#         id = aux_data_csef['code_insee'].index(csef)
#         # for csef in ls_csef:
#         ic += 1
#         # m14 = m14_ensemble(cfg['database']['Simcalc']['ensemble_url_prefix'], csef, cfg['year'])
#         # ensemble = SimcalcEnsemble(cfg['database']['Simcalc']['url_prefix_ensemble'], csef, cfg['year'], 1000.)
#
#         #fixme: remplacer aux_data_csef['pop_insee'][0] avec le bon index
#         start_time = time.time()
#         ensemble = SimcalcEnsemble(csef, cfg['year'], aux_data_csef['pop_insee'][id])
#         for key in ensemble.montant.keys():
#             if ic == 1:
#                 ratios_de_base[key] = []
#             ratios_de_base[key].append(ensemble.montant_par_habitant[key])
#         elapsed_time = time.time() - start_time
#
#     elapsed_time = time.time() - start_time_all
#     print '          - la récupération des données pour l ensemble de la csef a pris ', elapsed_time, ' secondes \n'
#     # todo: tester il faut checker qu'on a bien m14_ens[i].insee == ls_csef[i]
#     # print "ratios_de_base['trrf']", ratios_de_base['trrf']

