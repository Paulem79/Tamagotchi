import time
from typing import Callable

from modules import modules

# Variables importantes du jeu
modules_charges: list[tuple[Callable[[], None], int]] = []
running: bool = True
ms_ecoule: int = 0


def initialiser():
    """
    S'exécute une seule fois au début, pour charger tous les modules
    """
    # Charger tous les modules
    for module in modules:
        charger(module[0], module[1])
    # Dire qu'on a fini de tout démarrer
    print("Initialisé !")


def charger(fonction_principale: Callable[[], None], toutes_les_ms: int):
    """
    Charger un module dans le jeu, une fonction qui s'exécute toutes les X ms
    """
    modules_charges.append((fonction_principale, toutes_les_ms))


def executer(module: Callable[[], None], toutes_les: int):
    """
    Simple fonction pour exécuter un module (utilisé dans la boucle principale)
    """
    if ms_ecoule % toutes_les == 0:
        module()


# On ne veut exécuter ceci que si on lance le programme directement
if __name__ == "__main__":
    initialiser()

    # Boucle principale
    while running:
        # On veut attendre 1 ms pour éviter de tout casser
        time.sleep(0.001)
        # On ajoute 1 ms à notre compteur (pour les exécutions de modules)
        ms_ecoule += 1

        # On exécute tous les modules chargés
        for fonction, tous_les in modules_charges:
            executer(fonction, tous_les)
