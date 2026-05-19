import random

import config


def sport_decompte():
    config.etat_de_sante = config.etat_de_sante - 1
    print("etat de sante :", config.etat_de_sante)


def sport():
    config.etat_de_sante = config.etat_de_sante + random.randint(1, 30)
    config.faim -=random.randint(10, 20)
    config.eau -=random.randint(5, 10)
    
