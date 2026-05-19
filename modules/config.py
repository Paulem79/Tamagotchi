from typing import Callable, TypeVar, Generic

T = TypeVar('T')

# Variables importantes du jeu
running: bool = True
ms_ecoule: int = 0
mort: bool = False
mort_raison: str = ""
dae_en_cours: bool = False

def tuer(raison: str):
  global mort, mort_raison
  mort = True
  mort_raison = raison