import asyncio
import math
from typing import Any, Callable
import sys
import os
import psutil

def jouer():
  global pres_jeu
  pres_jeu = False

def redemarrer():
  """
  Redémarrer le jeu
  Source: https://bobbyhadz.com/blog/how-to-restart-python-script-from-within-itself#restarting-a-python-script-with-psutil
  """
  try:
      process = psutil.Process(os.getpid())

      for handler in process.open_files() + process.connections():
          os.close(handler.fd)
  except Exception as e:
      print(e)

  python = sys.executable
  os.execl(python, python, *sys.argv)

async def attente_ms():
    """Attendre 1 ms pour tout synchroniser jeu + pygame, et libérer de la charge processeur aussi"""
    await asyncio.sleep(0.001)

def multiplicateur_drainage():
  if not difficile:
    # Très racine carrée, mais au moins ça augmente lentement
    return math.sqrt(math.sqrt(math.sqrt(score_pour_multiplicateur())))
  return math.sqrt(score_pour_multiplicateur())

def multiplicateur_module():
  if not difficile:
    # Plus c'est proche de 0, plus ça diminue lentement, dcp 0.3 c'est pas trop mal
    puissance = 0.3
    return min(1, 1 / (score_pour_multiplicateur() ** puissance))
  return min(1, 1/score_pour_multiplicateur())

def score_pour_multiplicateur():
  return max(1, score / 10)

def lejedupandujaje():
  global lejedupandu
  lejedupandu = fenetre_ouverte

def tuer(raison: str):
  global mort, mort_raison
  mort = True
  mort_raison = raison

def activer_difficile():
  global difficile
  if difficile:
    difficile = False
    print("Mode difficile désactivé !")
  else:
    difficile = True
    print("Mode difficile activé !")

def stopper_jeu():
  global jeu_en_cours
  jeu_en_cours = False

def stopper_fenetre():
  global fenetre_ouverte
  fenetre_ouverte = False

def stopper_tout():
  stopper_jeu()
  stopper_fenetre()


# Variables importantes du jeu
jeu_en_cours: bool = True
fenetre_ouverte: bool = False
difficile: bool = False
lejedupandu: bool = False

pres_jeu: bool = True

ms_ecoule: int = 0
mort: bool = False
mort_raison: str = ""

# Main
resultats: dict[str, Any] = {}
derniere_execution: dict[Callable, int] = {}

# Variables de modules
# DAE
dae_en_cours: bool = False
dae_actionne: bool = False
demande_defibrillateur: bool = False
# Faim
faim: int = 100
# Eau
eau: int = 50
# Score
score = 0
# Sante
malade: bool = False
etat_de_sante: int = 100
# Météo
pression_atmo: int = 1000