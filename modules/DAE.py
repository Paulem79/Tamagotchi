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
  
  for i in range(5000): # 5s
    await main.attente_ms()
    # Toutes les secondes
    if i % 1000 == 0:
      print("Actionne le défibrillateur !")
    
    if actionné:
      print("Défibrillateur actionné !")
      actionné = False
      demande_defibrilatteur = False
      break

  if actionné and random.randint(0,100) <= 35:
    config.mort = False
    config.mort_raison = ""
    nourriture.faim = 50
    water.eau = 30
    sante.malade = False
    sport.etat_de_sante = 30
    print("en vie !")
    return False
  else:
    print("Echec.")
    return True