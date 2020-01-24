#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

"""
Module qui contient les fonctions nécéssaires à la notation des collectivités
"""
##########################
#       Libraries
##########################
import inspect
import numpy as np
from .maths_functions import binning, reject_outliers
import prescription.classification as cf
import scipy as sp


def calcul_ratios(liste_csef, aux_collections):
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
    # recupération
    #for code_insee in insee_classification['insee_csef']:
    for code_insee in liste_csef:
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

    if 1:
        print('')
        print('          Controle des données auxiliaires des CL dans la csef')
        print(("\n          - 'code_insee    :", aux_data_csef['code_insee']))
        print(("\n          - 'nom           :", aux_data_csef['nom']))
        print(("\n          - 'pop_insee     :", aux_data_csef['pop_insee']))
        print(("\n          - 'regime fiscal :", aux_data_csef['regime_fiscal']))
        print(("\n          - 'FPFB          :", ratios_csef['fpfb']))
        print(("\n          - 'FPROD          :", ratios_csef['fprod']))

    return ratios_csef, aux_data_csef



def process_ratios(ratios_csef, note_max):
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
            notes_ratios_de_base[str(key)] = notation_ratios(ratios_csef[key], note_max, reverse=True)
        else:
            notes_ratios_de_base[str(key)] = notation_ratios(ratios_csef[key], note_max)
        # print '             notes', notes_ratios_de_base[key]
    return notes_ratios_de_base



def notation_ratios(ratios, note_max, reverse=None, filter=None):
    """
    :param ratios: la liste des valeurs du ratio pour chaque ville
    :param note_max: determine le binning
    :param reverse: False = la note croit avec la valeur, True la note est une fonction inverse de la valeur
    :return: les notes de chaque villes
    """
    if not reverse:  reverse= False
    # if not filter:  filter= False
    if not filter:  filter= True
    # fixme: pour le moment on ne filtre pas les donnees car la statistique est trop faible (une quinzaine de clients uniquement)
    # todo: faire une étude de sensibilité sur reject_outliers (nombre de sigma)
    if filter == True:
        filtered_dist = reject_outliers(ratios)
    else:
        filtered_dist = [float(x) for x in ratios]

    bornes_inf, bornes_sup, pas = binning(filtered_dist, note_max)

    notes = np.digitize(filtered_dist, bornes_inf)
    notes = [x for x in notes]
    notes = [notes[x] if not np.isnan(filtered_dist[x]) else 0 for x in range(len(notes))]
    if reverse:
        notes = [note_max+1 - x for x in notes]
    return notes


def notation_theme(notes_ratios, poids_ratios):
    """
    :param notes_ratios: dictionnaires des notes de l'ensemble des ratios
    :param poids_ratios: le poids des différents ratios dans le theme
    :return: la liste des notes des villes pour un theme
    """
    note=[]
    for x in range(0,len(notes_ratios[list(notes_ratios.keys())[0]])):#loop sur les villes
        note.append(np.sum([notes_ratios[key][x]*poids_ratios[key] for key in list(poids_ratios.keys())]))
    return note


def champions_selection(notes_ratios_de_base, aux_data_csef, champions_selection):
    notes_themes = {}
    champions = {}

    # selections des champions thématiques (on garde le code_insee c'est plus safe qu'un index):
    #  1- pour chaque theme on ne garde que les collectivités qui présentent la note thématique la plus élevée
    for theme in champions_selection['theme']:# Show all themes[0:2]:
        notes_themes[str(theme)] = notation_theme(notes_ratios_de_base, champions_selection[theme])

        print('          notes du thème {0}: {1} '.format(theme, notes_themes[str(theme)]))
        # fixme: il faut checker que la notation par grand theme prend bien en compte la ponderation que l'on a mise dans le fichier de config
        # fixme checker where à la place de argwhere

        idx = np.argwhere(notes_themes[theme] == np.amax(notes_themes[theme])).flatten().tolist()
        # champions[str(theme)]= [aux_data_csef['code_insee'][id] for id in idx]
        champions[str(theme)] = {}
        champions[str(theme)]['insee'] = [aux_data_csef['code_insee'][id] for id in idx]
        champions[str(theme)]['nom'] = [aux_data_csef['nom'][id] for id in idx]
        champions[str(theme)]['note'] = [notes_themes[str(theme)][id] for id in idx]

        print('       - Champions ', theme, ' : ', champions[str(theme)]['nom'], champions[str(theme)]['insee'], [notes_themes[str(theme)][id] for id in idx])
    return champions

