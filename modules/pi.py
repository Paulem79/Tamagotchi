import random
import modules.eau as water
import modules.config as config


# fonction de besoin accentu la difficuler et le réalisme
def pypy():
    if random.randint(0, 5) == 0:
        water.eau -= random.randint(15, 20)
        return ("Pipi :", "pipi")
    if water.eau < 1:
        config.tuer("Mort de soif !")