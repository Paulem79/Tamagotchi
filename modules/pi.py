import random
import config

# fonction de besoin accentu la difficuler et le réalisme
# Léo t'étais investi dans le commentaire ahaha
def pypy():
    if random.randint(0, 5) == 0:
        config.eau -= random.randint(15, 20)
        return ("Pipi :", "pipi")
    if config.eau < 1:
        config.tuer("soif")

    # Pipi, on ne renvoit rien
    return None