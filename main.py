import time
import asyncio
from typing import Any, Callable

from modules import modules

import modules.DAE as DAE
import modules.commande as commande
import modules.config as config

resultats: dict[str, Any] = {}
derniere_execution: dict[Callable, int] = {}

def obtenir_resultat(nom: str):
    return resultats.get(nom, None)

def executer(module: Callable[[], tuple[str, config.T]], toutes_les: int):
    """
    Exécute un module si l'intervalle 'toutes_les' en ms est dépassé,
    en gérant les sauts de temps causés par la boucle asynchrone.
    """
    # Si jamais executé, on l'initialise
    if module not in derniere_execution:
        derniere_execution[module] = config.ms_ecoule

    # Calcul du temps depuis dernière exécution
    temps_ecoule = config.ms_ecoule - derniere_execution[module]

    # Si plus grand ou égal à intervalle requise
    if temps_ecoule >= toutes_les:
        executé = module()

        # Met à jour le moment de la dernière exécution
        # En soustrayant le "surplus" (temps_ecoule - toutes_les), on reste précis
        # même s'il y a eu un léger retard.
        derniere_execution[module] = config.ms_ecoule - (temps_ecoule % toutes_les)

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

    dernier_temps = time.perf_counter()

    while config.running:
        await asyncio.sleep(0.001)

        # Vrai temps écoulé avec time dcp
        maintenant = time.perf_counter()
        ms_passees = int((maintenant - dernier_temps) * 1000)

        if ms_passees > 0:
            config.ms_ecoule += ms_passees
            dernier_temps = maintenant

            if config.mort:
                completement_mort = await DAE.DAE()
                if completement_mort:
                    if not config.mort_raison == "":
                        print(config.mort_raison)
                    else:
                        print("Mort.")
                    break

            # Exécute les modules chargés
            for fonction, tous_les in modules:
                executer(fonction, tous_les)

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
