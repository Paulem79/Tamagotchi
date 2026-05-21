import random

import config
import main
from jeu.musique import jouer_son


def actionner():
    if config.demande_defibrillateur and config.mort:
        config.dae_actionne = True
        config.demande_defibrillateur = False

def echec():
    config.stopper_jeu()

def reussi():
    config.mort = False
    config.mort_raison = ""
    config.faim = 50
    config.eau = 30
    config.malade = False
    config.etat_de_sante = 30

async def dae() -> bool:
    if not config.jeu_en_cours:
        return False

    config.demande_defibrillateur = True
    config.dae_actionne = False

    temps_depart = config.ms_ecoule
    derniere_seconde_affichee = 0

    try:
        # On a jusqu'à 5 secondes pour actionner le défibrillateur
        while (config.ms_ecoule - temps_depart) < 5000:
            await config.attente_ms()

            # On compare le temps écoulé par rapport à la boucle principale main, asynchrone
            temps_actuel_ecoule = config.ms_ecoule - temps_depart
            seconde_actuelle = temps_actuel_ecoule // 1000

            if seconde_actuelle > derniere_seconde_affichee:
                print("Actionne le défibrillateur !")
                derniere_seconde_affichee = seconde_actuelle
                jouer_son("dae")

            if config.dae_actionne:
                break

        if config.dae_actionne:
            print("Défibrillateur actionné !")

            # 35% de chances de réanimation
            if random.randint(0, 100) <= 35:
                reussi()
                print("En vie !")
                return False  # Pas complètement mort

            echec()
            print("Échec de la réanimation.")
            return True   # Complètement mort

        # Les 5 secondes sont passées
        echec()
        print("Échec (temps écoulé).")
        return True       # Complètement mort
    finally: # reset les variables à chaque fois pour éviter les bugs
        config.dae_actionne = False
        config.demande_defibrillateur = False
