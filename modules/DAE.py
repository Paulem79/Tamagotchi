import random

import config
import main


def actionner():
    config.dae_actionne = True

async def DAE() -> bool:
    config.demande_defibrilatteur = True

    temps_depart = config.ms_ecoule
    derniere_seconde_affichee = 0

    while (config.ms_ecoule - temps_depart) < 5000:
        await main.attente_ms()

        temps_actuel_ecoule = config.ms_ecoule - temps_depart
        seconde_actuelle = temps_actuel_ecoule // 1000

        if seconde_actuelle > derniere_seconde_affichee:
            print("Actionne le défibrillateur !")
            derniere_seconde_affichee = seconde_actuelle

        if config.dae_actionne:
            break

    if config.dae_actionne:
        print("Défibrillateur actionné !")
        config.dae_actionne = False
        config.demande_defibrilatteur = False

        if random.randint(0, 100) <= 35:
            config.mort = False
            config.mort_raison = ""
            config.faim = 50
            config.eau = 30
            config.malade = False
            config.etat_de_sante = 30
            print("en vie !")
            return False  # Pas complètement mort
        else:
            print("Échec de la réanimation.")
            return True   # Complètement mort
    else:
        # Les 5 secondes sont passées sans action de l'utilisateur
        config.demande_defibrilatteur = False
        print("Échec (Temps écoulé).")
        return True       # Complètement mort