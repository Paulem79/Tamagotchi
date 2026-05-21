import math

# Variables importantes du jeu
jeu_en_cours: bool = True
fenetre_ouverte: bool = False
difficile: bool = False
lejedupandu: bool = False

pres_jeu: bool = True

def jouer():
  global pres_jeu
  pres_jeu = False

ms_ecoule: int = 0
mort: bool = False
mort_raison: str = ""

def multiplicateur_drainage():
  if not difficile:
    return 1
  return math.sqrt(score_pour_multiplicateur())

def multiplicateur_module():
  if not difficile:
    return 1
  return min(1, 1/score_pour_multiplicateur())

def score_pour_multiplicateur():
  return score / 10

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