from typing import Callable, Any

import modules.eau as eau
import modules.meteo as meteo
import modules.nourriture as nourriture
import modules.pi as pi
import modules.sante as sante
import modules.score as score
import modules.sport as sport

# Tous les modules, et tous les combien de secondes ils s'exécutent
# Les fonctions peuvent retourner ce qu'elles veulent
modules: list[tuple[Callable[[], tuple[str, Any]], int]] = [
  (lambda: nourriture.nourriture(), 1500), # 0.15s
  (lambda: sante.maladie(), 10000), # 10s
  (lambda: pi.pypy(), 5000), # 5s
  (lambda: eau.soif(), 2000), # 2s
  (lambda: sport.sport_decompte(), 5000), # 5s
  (lambda: score.score_decompte(), 1000), #1s
  (lambda: meteo.temps(),10000), #10s
]