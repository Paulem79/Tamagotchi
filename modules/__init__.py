from typing import Callable, Any

import modules.eau as eau
import modules.meteo as meteo
import modules.nourriture as nourriture
import modules.pi as pi
import modules.sante as sante
import modules.score as score
import modules.sport as sport
import modules.mort as mort

# Tous les modules, et tous les combien de secondes ils s'exécutent
# Les fonctions peuvent retourner ce qu'elles veulent
# Format: (fonction, intervalle_ms, executer_au_demarrage)
modules: list[tuple[Callable[[], tuple[str, Any]], int, bool]] = [
  (nourriture.nourriture, 1500, False), # 0.15s
  (sport.sport_decompte, 5000, False), # 5s
  (sante.maladie, 10000, False), # 10s
  (pi.pypy, 5000, False), # 5s
  (eau.soif, 2000, False), # 2s
  (score.score_decompte, 1000, False), #1s
  (meteo.temps, 10000, True),
  (mort.mort,100,False),#10s et exécute au démarrage
]