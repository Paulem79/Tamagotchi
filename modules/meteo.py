import random
from config import pression_atmo


def pression():
    global pression_atmo
    
    if pression_atmo < 1000:
        pression_atmo += random.randint(50, 150)
    if pression_atmo > 1000:
        pression_atmo -= random.randint(10, 100)
    if pression_atmo > 900 :
        pression_atmo -= random.randint(10, 100)

    return ("Pression atmosphérique :", pression_atmo)

def temps():
    global pression_atmo
    pression()

    meteo_actuel: str
    
    if pression_atmo > 1000:
        meteo_actuel = "soleil.png"
    elif pression_atmo < 900:
        meteo_actuel = "orage.png"
    else: #elif pression_atmo < 1000:
        meteo_actuel = "pluie.png"

    return ("Temps :", meteo_actuel)
