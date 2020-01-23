#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

################################################################################
# Anthony Guignard 22/01/2020
#
#  Boite à outils personnelle utiliée pour le module d'optimisation
################################################################################

import json
#import inspect

# from fastnumbers import fast_float, fast_int


def clean_json(input_file):
    """
    Permet de lire un fichier de configuration au
    format Json contenant des commentaires signalés par // (norme C)
    :param input_file: fichier json commenté
    :return: un dictionnaire du json
    """
    clean_lines = ''
    with open(input_file, 'r') as f:
        for line in f:
            if '//' not in line:
                clean_lines += line.rstrip()
            else:
                clean_lines += line.split('//')[0].rstrip()
    output_obj = json.loads(clean_lines)
    return output_obj


def find_safe_methods(classe, filter=None):
    """
    Retourne la liste des methodes d'une classe que l'on peut exposer
    :param classe: une classe
    :param filter: la chaine de caractère de qu'on souhaite chercher dans la liste de methodes
    :return: la liste des noms des methodes contenant la chaine de caracteres 'safe'
    """
    names = []
    infos = []
    if filter is None:
        filter = 'get_theme_test'

    for name, data in inspect.getmembers(classe):
        if name in ('__builtins__', '__module__', '__doc__'):
            continue
        if filter in name:
            # info += "<em><b>%s.%s</b></em><br>"%(cls.__name__, name)
            names.append(name)
            infos.append(data)
    return names, infos



def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


cfg = clean_json('config.json') # pour utiliser le fichier de configuration comme une variable globale
                                # apres avoir appeler clean_json dans le main, il suffit de faire from utils.toolbox import cfg
                                # dans les paquet qui nécéssite le fichier de configuration
