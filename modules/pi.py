import random
import config

# fonction de besoin accentu la difficuler et le réalisme
# Léo t'étais investi dans le commentaire ahaha (la phrase n'a aucun sens)
def pypy():
    if random.randint(0, 5) == 0:
        config.eau -= random.randint(15, 20)
        return ("Pipi :", "pipi")
    # On gère pas mal de fois mourir de soif dans le code, mais c'est pas un problème
    if config.eau < 1:
        config.tuer("soif")

    # Pipi, on ne renvoit rien
    return None