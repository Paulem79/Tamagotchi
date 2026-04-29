from typing import Callable

import modules.nourriture as nourriture

# Tous les modules, et tous les combien de secondes ils s'exécutent
modules: list[tuple[Callable[[], None], int]] = [
  (nourriture.nourriture, 1000)
]