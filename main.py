import time
import asyncio
from typing import Any, Callable

from modules import modules

import modules.DAE as DAE
import modules.commande as commande
import config

resultats: dict[str, Any] = {}
derniere_execution: dict[Callable, int] = {}

def obtenir_resultat(nom: str):
    return resultats.get(nom, None)

def executer(module: Callable[[], tuple[str, Any]], toutes_les: int, au_demarrage: bool = False):
    """
    Exécute un module si l'intervalle 'toutes_les' en ms est dépassé,
    en gérant les sauts de temps causés par la boucle asynchrone.
    """
    # Si jamais executé, on l'initialise
    if module not in derniere_execution:
        # Si le module doit s'exécuter au démarrage, on force l'exécution immédiate
        if au_demarrage:
            derniere_execution[module] = config.ms_ecoule - toutes_les
        else:
            derniere_execution[module] = config.ms_ecoule

    # Calcul du temps depuis dernière exécution
    temps_ecoule = config.ms_ecoule - derniere_execution[module]

    # Si plus grand ou égal à intervalle requise
    if temps_ecoule >= toutes_les:
        resultat_module = module()

        # Met à jour le moment de la dernière exécution
        # En soustrayant le "surplus" (temps_ecoule - toutes_les), on reste précis
        # même s'il y a eu un léger retard.
        derniere_execution[module] = config.ms_ecoule - (temps_ecoule % toutes_les)

        if resultat_module is not None:
            nom, value = resultat_module

            if nom is None:
                nom = "Module inconnu :"

            if value is not None:
                resultats[nom] = value
                print(nom, value)

async def gerer_fin_dae():
    """
    gérer la fin du DAE en arrière-plan
    """
    completement_mort = await DAE.dae()

    if completement_mort:
        # Print la raison de la mort s'il y en a une
        if config.mort_raison != "":
            print(config.mort_raison)
        else:
            # Sinon, juste mort
            print("Mort.")
        # Arrêter le jeu de manière clean dcp
        config.stopper_jeu()
    config.dae_en_cours = False

async def attente_ms():
    """On veut attendre 1 ms pour éviter de tout casser"""
    await asyncio.sleep(0.001)

async def main():
    _commandes = asyncio.create_task(commande.action())

    dernier_temps = time.perf_counter()

    while config.jeu_en_cours:
        await asyncio.sleep(0.001)

        # Vrai temps écoulé avec time dcp
        maintenant = time.perf_counter()
        ms_passees = int((maintenant - dernier_temps) * 1000)

        if ms_passees <= 0:
            continue
            
        config.ms_ecoule += ms_passees
        dernier_temps = maintenant

        if config.mort and not config.dae_en_cours:
            config.dae_en_cours = True

            # DAE en arrière-plan pour éviter de tout bloquer
            _tache = asyncio.create_task(gerer_fin_dae())

        # Exécute les modules chargés
        for fonction, tous_les, au_demarrage in modules:
            executer(fonction, tous_les, au_demarrage)

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
