import random

import config
from jeu.musique import jouer_son


def sport_decompte():
    config.etat_de_sante = config.etat_de_sante - (random.randint(5,20))
    print("etat de sante :", config.etat_de_sante)


def sport():
    config.etat_de_sante = config.etat_de_sante + random.randint(1, 30)
    config.faim -=random.randint(10, 20)
    config.eau -=random.randint(5, 10)
    jouer_son("sport")
    
