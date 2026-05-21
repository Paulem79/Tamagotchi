import random

import config


# fonction de santé
def maladie() -> tuple[str, bool]:
    if random.randint(0, max(0, config.etat_de_sante)) == 0:
        config.malade = True
    return ("Malade :", config.malade)


def guerir():
    config.malade = False
    config.etat_de_sante = 100
    config.faim -= 30
    config.eau -= 30
    print("Vous avez été soigné !")