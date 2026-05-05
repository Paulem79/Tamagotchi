import time
import asyncio
from typing import Callable

from modules import modules

import modules.commande as commande
import modules.config as config

def executer(module: Callable[[], tuple[str, int]], toutes_les: int):
    """
    Simple fonction pour exécuter un module (utilisé dans la boucle principale)
    """
    if config.ms_ecoule % toutes_les == 0:
        executé = module()
        if executé is not None:
            nom, value = executé
            
            if nom is None:
                nom = "Module inconnu :"
            
            if value is not None:
                print(nom, value)

async def main():
    asyncio.create_task(commande.action()) # ne marche pas : tout le programme attent une reponse à l'input et donc arrete la faim et le tps. je laisse si jamais quelqu'un sait comment resoudre

    # Boucle principale
    while config.running:
        # On veut attendre 1 ms pour éviter de tout casser
        await asyncio.sleep(0.001)
        # On ajoute 1 ms à notre compteur (pour les exécutions de modules)
        config.ms_ecoule += 1

        if config.mort:
            print("Vous êtes mort !")
            return

        # On exécute tous les modules chargés
        for fonction, tous_les in modules:
            executer(fonction, tous_les)

# On ne veut exécuter ceci que si on lance le programme directement
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass