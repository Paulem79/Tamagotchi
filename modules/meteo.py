import random

pression_atmo: int = 1000


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
        meteo_actuel = "soleil"
    elif pression_atmo < 900:
        meteo_actuel = "orage"
    else: #elif pression_atmo < 1000:
        meteo_actuel = "pluie"

    return ("Temps :", meteo_actuel)
