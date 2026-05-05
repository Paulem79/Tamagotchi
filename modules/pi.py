import random
import modules.eau as water
import modules.config as config

def pypy():
  eau = water.eau
  if random.randint(0, 10)==0 :
    eau = eau-random.randint(15,20)
  if eau<1:
    config.tuer()
    print("Vous êtes mort de soif !")