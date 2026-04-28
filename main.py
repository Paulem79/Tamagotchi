import time
from typing import Callable

import communs

modules: list[tuple[Callable[[], None], int]] = []
running: bool = True
ms_ecoule: int = 0


def initialiser():
   charger(communs.test, 1000)
   print("Initialisé !")


def charger(fonction_principale: Callable[[], None], toutes_les_ms: int):
    modules.append((fonction_principale, toutes_les_ms))


def executer(module: Callable[[], None], toutes_les: int):
    if ms_ecoule % toutes_les == 0:
        module()

if __name__ == "__main__":
   initialiser()

   while running:
       time.sleep(0.001)
       ms_ecoule += 1

       for fonction, tous_les in modules:
           executer(fonction, tous_les)
