from typing import Callable

# Variables importantes du jeu
running: bool = True
ms_ecoule: int = 0
mort: bool = False

def tuer():
  global mort
  mort = True