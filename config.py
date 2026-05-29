import asyncio
import math
from typing import Any, Callable
import sys
import os
import psutil

def jouer():
  """Jouer vraiment, donc plus sur le menu principal"""
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
  """On veut que plus le temps passe, plus la valeur augmente"""
  if not difficile:
    # Très racine carrée, mais au moins ça augmente lentement
    return math.sqrt(math.sqrt(math.sqrt(score_pour_multiplicateur())))
  return math.sqrt(score_pour_multiplicateur())

def multiplicateur_module():
  """On veut que plus le temps passe, plus la valeur diminue (pour rapprocher les exécutions de modules)"""
  if not difficile:
    # Plus c'est proche de 0, plus ça diminue lentement, dcp 0.3 c'est pas trop mal
    puissance = 0.3
    return min(1, 1 / (score_pour_multiplicateur() ** puissance))
  return min(1, 1/score_pour_multiplicateur())

def score_pour_multiplicateur():
  """Score pour multiplier un peu tout sans que ça soit trop agressif, j'ai abouti à ça grâce mon cerveau d'abandonneur de spé maths en première, on fait ce qu'on peut avec ce qu'on a..."""
  return max(1, score / 10)

def lejedupandujaje():
  """Activer le truc méga ultra secret de la mort qui tue (trichez pas monsieur svp)"""
  global lejedupandu
  lejedupandu = fenetre_ouverte

def tuer(raison: str):
  """Tuer le pauvre Poyo, et mettre pourquoi il est mort.
  Il finira par venir se venger à force de se faire maltraiter comme ça"""
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
  """Stopper surtout les modules (main.py)"""
  global jeu_en_cours
  jeu_en_cours = False

def stopper_fenetre():
  """Stopper pygame (game.py)"""
  global fenetre_ouverte
  fenetre_ouverte = False

def stopper_tout():
  """Je pense pas avoir besoin d'expliquer"""
  stopper_jeu()
  stopper_fenetre()


# Variables importantes du jeu
jeu_en_cours: bool = True
fenetre_ouverte: bool = False
# Mode difficile actif ?
difficile: bool = False
# Truc méga ultra secret de la mort qui tue actif ?
lejedupandu: bool = False

# Dans le menu principal ?
pres_jeu: bool = True

# Temps écoulé en ms depuis le début
ms_ecoule: int = 0

mort: bool = False
# Raison de la mort
mort_raison: str = ""

# Résultats des modules de main.py
resultats: dict[str, Any] = {}
# De quand date (ms) la dernière exécution de chaque module
derniere_execution: dict[Callable, int] = {}

# Variables de modules
# DAE
# Si en cours de DAE
dae_en_cours: bool = False
# Si on a actionné le défibrillateur
dae_actionne: bool = False
# Si on attend toujours que le joueur utilise le DAE
demande_defibrillateur: bool = False
# Faim
faim: int = 100
# Eau
eau: int = 50
# Score
score: int = 0
# Sante
malade: bool = False
etat_de_sante: int = 100
# Météo
pression_atmo: int = 1000