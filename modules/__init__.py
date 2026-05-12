from typing import Callable
import random
import modules.nourriture as nourriture
import modules.sante as sante
import modules.pi as pi
import modules.eau as eau
import modules.sport as sport
import modules.config as config
import modules.score as score
import modules.meteo as meteo

# Tous les modules, et tous les combien de secondes ils s'exécutent
# Les fonctions peuvent retourner ce qu'elles peuvent, d'où le config.T (type générique)
modules: list[tuple[Callable[[], tuple[str, config.T]], int]] = [
  (lambda: nourriture.nourriture(), 1500), # 0.15s
  (lambda: sante.maladie(), 10000), # 10s
  (lambda: pi.pypy(), 5000), # 5s
  (lambda: eau.soif(), 2000), # 2s
  (lambda: sport.sport_decompte(), 5000), # 5s
  (lambda: score.score_decompte(), 1000), #1s
  (lambda: meteo.temps(),10000), #10s
]