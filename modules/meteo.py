import random
import config
from modules.depression import depression

def pression():
    if config.pression_atmo < 1000:
        config.pression_atmo += random.randint(50, 150)
    if config.pression_atmo > 1000:
        config.pression_atmo -= random.randint(10, 100)
    if config.pression_atmo > 900 :
        config.pression_atmo -= random.randint(10, 100)

    return ("Pression atmosphérique :", config.pression_atmo)

def temps():
    pression()

    meteo_actuel: str
    
    if config.pression_atmo > 1000:
        meteo_actuel = "soleil.png"
    elif config.pression_atmo < 900:
        meteo_actuel = "orage.png"
        depression()
        if random.randint(0,1000)==0:
            config.tuer("mort de la foudre")
    else: #elif config.pression_atmo < 1000:
        meteo_actuel = "pluie.png"

    return ("Temps :", meteo_actuel)
