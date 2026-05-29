import random
import config


def depression():
    # Si il fait plutôt pluie, on baisse l'état de santé
    if config.pression_atmo <900:
        config.etat_de_sante = config.etat_de_sante - (random.randint(5,10))
        config.faim -=random.randint(1,10)
        print("etat de sante :", config.etat_de_sante)
