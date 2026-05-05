from typing import Callable
import random
import modules.nourriture as nourriture
import modules.sante as sante
import modules.pi as pi
import modules.eau as eau

# Tous les modules, et tous les combien de secondes ils s'exécutent
modules: list[tuple[Callable[[], tuple[str, int]], int]] = [
  (lambda: nourriture.nourriture(), 100),
  (lambda: sante.maladie(),10000),
  (lambda: pi.pypy(),5000),
  (lambda: eau.soif(),2000),
]