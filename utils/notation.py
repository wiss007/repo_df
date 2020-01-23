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
from maths_functions import binning, reject_outliers
import scipy as sp



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
    for x in range(0,len(notes_ratios[notes_ratios.keys()[0]])):#loop sur les villes
        note.append(np.sum([notes_ratios[key][x]*poids_ratios[key] for key in poids_ratios.keys()]))
    return note










