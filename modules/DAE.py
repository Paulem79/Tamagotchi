import main
import modules.config as config
import modules.nourriture as nourriture
import modules.eau as water
import modules.sante as sante
import modules.sport as sport
import random

demande_defibrilatteur: bool = False
actionné: bool = False

def actionner():
    global actionné
    actionné = True

async def DAE() -> bool:
    global demande_defibrilatteur
    global actionné

    demande_defibrilatteur = True

    temps_depart = config.ms_ecoule
    derniere_seconde_affichee = 0

    while (config.ms_ecoule - temps_depart) < 5000:
        await main.attente_ms()

        temps_actuel_ecoule = config.ms_ecoule - temps_depart
        seconde_actuelle = temps_actuel_ecoule // 1000

        if seconde_actuelle > derniere_seconde_affichee:
            print("Actionne le défibrillateur !")
            derniere_seconde_affichee = seconde_actuelle

        if actionné:
            break

    if actionné:
        print("Défibrillateur actionné !")
        actionné = False
        demande_defibrilatteur = False

        if random.randint(0, 100) <= 35:
            config.mort = False
            config.mort_raison = ""
            nourriture.faim = 50
            water.eau = 30
            sante.malade = False
            sport.etat_de_sante = 30
            print("en vie !")
            return False  # Pas complètement mort
        else:
            print("Échec de la réanimation.")
            return True   # Complètement mort
    else:
        # Les 5 secondes sont passées sans action de l'utilisateur
        demande_defibrilatteur = False
        print("Échec (Temps écoulé).")
        return True       # Complètement mort