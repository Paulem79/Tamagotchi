import random
import modules.sport as sport

malade = False


# fonction de santé
# TODO: Rajouter la possibilité de se soigner
def maladie() -> tuple[str, bool]:
    etat_de_sante = sport.etat_de_sante
    if random.randint(0, etat_de_sante) == 0:
        global malade
        malade = True
    return ("Malade :", malade)


def guerir():
    global malade
    malade = False
