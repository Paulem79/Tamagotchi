import random

import config


# fonction de santé
def maladie() -> tuple[str, bool]:
    if random.randint(0, max(0, config.etat_de_sante)) == 0:
        config.malade = True
    return ("Malade :", config.malade)


def guerir():
    if config.malade==True:
        config.malade = False
        config.etat_de_sante +=30
        config.faim -= 30
        config.eau -= 30
        print("Vous avez été soigné !")
    else:
        config.malade = True
        config.etat_de_sante = 50
        config.faim -= 30
        config.eau -= 30
        print("Vous avez abusé des médoc !")