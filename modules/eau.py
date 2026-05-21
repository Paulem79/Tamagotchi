import random
import config
from jeu.musique import jouer_son


def soif() -> tuple[str, int]:
    config.eau -= 1

    if config.eau < 1:
        config.tuer("Mort de soif")
    if config.eau > 110:
        config.tuer("coma hydraulique")

    return ("Eau :", config.eau)


def boire():
    jouer_son("boire")

    quantite = random.randint(10, 20)

    if config.eau > 60 and config.eau < 100:
        print("Trop bu !")
        config.eau += quantite
        if random.randint(0,1)==0:
            config.malade = True
    if config.eau > 100:
        print("Hic !")
        config.eau -= random.randint(10, 25)
    else:
        config.eau += quantite