import random
import config


def soif() -> tuple[str, int]:
    config.eau -= 1

    if config.eau < 1:
          config.tuer("Mort de soif")
    if config.eau > 120:
          config.tuer("coma hydraulique")

    return ("Eau :", config.eau)



def boire():
      quantite = random.randint(10, 20)

      if config.eau > 60 and config.eau < 100 :
          print("Trop bu !")
          config.eau += quantite
          malade = True
      if config.eau > 100:
          print("Hic !")
          config.eau -= random.randint(10, 25)
      else:
          config.eau += quantite


