import random

import config


# fonction de santé
def maladie() -> tuple[str, bool]:
    if random.randint(0, config.etat_de_sante) == 0:
        config.malade = True
    return ("Malade :", config.malade)


def guerir():
    config.malade = False
