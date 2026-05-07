from modules.sante import malade
import random, time
import modules.config as config

eau: int = 50



def soif() -> tuple[str, int]:
    global eau
    eau -= 1

    if eau < 1:
          config.tuer("Mort de soif")
    if eau > 120:
          config.tuer("coma hydraulique")

    return ("Eau :", eau)



def boire():
      quantite = random.randint(10, 20)
      global eau

      if eau > 60 and eau < 100 :
          print("Trop bu !")
          eau += quantite
          malade = True
      if eau > 100:
          print("Hic !")
          eau -= random.randint(10, 25)
      else:
          eau += quantite


