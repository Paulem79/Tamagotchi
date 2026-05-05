import random, time
import modules.config as config

eau = 50

def soif() -> tuple[str, int]:
    global eau
    eau -= 1
    
    if eau < 1:
      config.tuer()
      return eau
    
    return ("Eau :", eau)

def boire():
  quantite = random.randint(10, 20)
  global eau
    
  if eau > 60 and eau < 100 and not malade:
      print("Trop bu !")
      eau += quantite
  if eau > 100:
      print("Hic !")
      eau = eau - random.randint(10, 25)
