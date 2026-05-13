import time
import asyncio
from typing import Callable

from modules import modules

import modules.DAE as DAE
import modules.commande as commande
import modules.config as config

resultats: dict[str, config.T] = {}

def obtenir_resultat(nom: str):
    return resultats.get(nom, None)

def executer(module: Callable[[], tuple[str, config.T]], toutes_les: int):
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
                resultats[nom] = value
                print(nom, value)

async def attente_ms():
    """On veut attendre 1 ms pour éviter de tout casser"""
    await asyncio.sleep(0.001)

async def main():
    asyncio.create_task(commande.action())

    # Boucle principale
    while config.running:
        await attente_ms()
        
        # On ajoute 1 ms à notre compteur (pour les exécutions de modules)
        config.ms_ecoule += 1

        if config.mort:
            completement_mort = await DAE.DAE()
            if completement_mort:
                if not config.mort_raison == "":
                    print(config.mort_raison)
                else:
                    print("Mort.")
                break

        # On exécute tous les modules chargés
        for fonction, tous_les in modules:
            executer(fonction, tous_les)

# On ne veut exécuter ceci que si on lance le programme directement
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass