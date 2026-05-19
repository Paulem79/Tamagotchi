pression_atmo: int = 1000

# Variables importantes du jeu
jeu_en_cours: bool = True
fenetre_ouverte: bool = False

ms_ecoule: int = 0
mort: bool = False
mort_raison: str = ""

def tuer(raison: str):
  global mort, mort_raison
  mort = True
  mort_raison = raison

def stopper_tout():
  global jeu_en_cours, fenetre_ouverte
  jeu_en_cours = False
  fenetre_ouverte = False

# Variables de modules
# DAE
dae_en_cours: bool = False
dae_actionne: bool = False
demande_defibrilatteur: bool = False
# Faim
faim: int = 100
# Eau
eau: int = 50
# Score
score = 0
# Sante
malade: bool = False
etat_de_sante: int = 100
